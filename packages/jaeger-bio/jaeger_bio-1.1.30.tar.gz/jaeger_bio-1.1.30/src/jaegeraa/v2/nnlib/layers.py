import tensorflow as tf # type: ignore
import tensorflow.keras as keras  # type: ignore
from tensorflow.keras.layers import InputSpec # type: ignore
import tensorflow.keras.backend as K # type: ignore
from tensorflow.data import Dataset, TextLineDataset, TFRecordDataset  # type: ignore


class MaskedMaxPooling1D(tf.keras.layers.Layer):
    
    def __init__(self, pool_size=2, strides=None, padding='valid', **kwargs):
        super(MaskedMaxPooling1D, self).__init__(**kwargs)
        self.pool_size = pool_size
        self.strides = strides if strides is not None else pool_size
        self.padding = padding.lower()

    def call(self, inputs, mask=None):
        
         # Reshape for MaskedMaxpooling1D
        input_shape = tf.shape(inputs)
        self.input_dtype = inputs.dtype
        batch_size = input_shape[0]
        dim1 = input_shape[1]
        dim2 = input_shape[2]
        dim3 = input_shape[3]
        
        if mask is not None:
            # Expand mask dimensions to match inputs
            mask = tf.cast(mask, dtype=inputs.dtype)
            inputs = inputs *  tf.expand_dims(mask, axis=-1)  # Zero out masked positions
            
        reshaped_inputs = tf.reshape(inputs, (-1, dim2, dim3))
        outputs = tf.nn.max_pool1d(
            reshaped_inputs,
            ksize=self.pool_size,
            strides=self.strides,
            padding=self.padding.upper()
        )

        # Reshape back to the original dimensions
        output_shape = self.compute_output_shape(input_shape)
        outputs = tf.reshape(outputs, output_shape)

        if mask is not None:
            reshaped_mask = tf.reshape(mask, (-1, dim2))
            mask = self.compute_output_mask(reshaped_mask)
            self._output_mask = tf.reshape(mask, output_shape[:-1])

        else:
            self._output_mask = None
            
        return outputs
    
    def compute_mask(self, inputs, mask=None):
        # Return the output mask computed in call()
        if hasattr(self, '_output_mask'):
            return self._output_mask
        else:
            return None
    def compute_output_mask(self, mask=None):
        if mask is None:
            return None
        else:
            mask = tf.cast(mask, dtype=self.input_dtype)
            mask = tf.expand_dims(mask, axis=-1)
   
            pooled_mask = tf.nn.max_pool1d(
                mask,
                ksize=self.pool_size,
                strides=self.strides,
                padding=self.padding.upper()
            )
            pooled_mask = tf.cast(pooled_mask, dtype=tf.bool)
            
            #pooled_mask = tf.squeeze(pooled_mask, axis=-1)
            return pooled_mask
        
    def compute_output_shape(self, input_shape):
        
        # Compute the output shape along the pooling axis
        axis_length = input_shape[2]
        if self.padding == 'valid':
            output_length = (axis_length - self.pool_size) // self.strides + 1
        elif self.padding == 'same':
            output_length = (axis_length + self.strides - 1) // self.strides
        
        # Create the new shape and replace the dimension for the pooled axis
        
        return input_shape[0], input_shape[1], output_length, input_shape[-1]

class MaskedLayerNormalization(tf.keras.layers.Layer):
    def __init__(self, epsilon=1e-3, center=True, scale=True, **kwargs):
        super(MaskedLayerNormalization, self).__init__(**kwargs)
        self.epsilon = epsilon
        self.center = center
        self.scale = scale
        self.supports_masking = True
    def build(self, input_shape):
        param_shape = input_shape[-1:]

        if self.scale:
            self.gamma = self.add_weight(
                name='gamma',
                shape=param_shape,
                initializer='ones',
                trainable=True
            )
        else:
            self.gamma = None

        if self.center:
            self.beta = self.add_weight(
                name='beta',
                shape=param_shape,
                initializer='zeros',
                trainable=True
            )
        else:
            self.beta = None

        super(MaskedLayerNormalization, self).build(input_shape)

    def call(self, inputs, mask=None):
        
        if mask is not None:
            mask = tf.cast(mask, inputs.dtype)
            mask = tf.expand_dims(mask, -1)
            mask = tf.stop_gradient(mask)

            # Compute the mean over unmasked positions
            masked_inputs = inputs * mask
            mask_sum = tf.reduce_sum(mask, axis=[1,2], keepdims=True)
            #tf.print(mask_sum.shape, masked_inputs.shape)
            mean = tf.reduce_sum(masked_inputs, axis=-1, keepdims=True) / (mask_sum + self.epsilon)
            
            # Compute the variance over unmasked positions
            squared_diff = tf.square((inputs - mean) * mask)
            variance = tf.reduce_sum(squared_diff, axis=-1, keepdims=True) / (mask_sum + self.epsilon)
        else:
            mean, variance = tf.nn.moments(inputs, axes=-1, keepdims=True)

        # Normalize the inputs
        normalized = (inputs - mean) / tf.sqrt(variance + self.epsilon)

        # Apply scale and center
        if self.scale:
            normalized = normalized * self.gamma
        if self.center:
            normalized = normalized + self.beta

        # Re-apply the mask to keep masked positions at zero
        if mask is not None:
            normalized = normalized * mask

        return normalized

    def compute_output_shape(self, input_shape):
        return input_shape

    def get_config(self):
        config = super(MaskedLayerNormalization, self).get_config()
        config.update({
            'epsilon': self.epsilon,
            'center': self.center,
            'scale': self.scale,
        })
        return config

class MaskedGlobalAvgPooling(tf.keras.layers.Layer):
    
    def __init__(self, **kwargs):
        super(MaskedGlobalAvgPooling, self).__init__(**kwargs)


    def call(self, inputs, mask=None):
            # Assuming inputs and mask have the same shape (batch_size, height, width, channels)
            if mask is not None:
                mask = tf.cast(mask, inputs.dtype)  # Convert mask to the same dtype as inputs
                mask = tf.expand_dims(mask, axis=-1)
                inputs = inputs * mask  # Zero out masked positions

                # Sum over the spatial dimensions (batch, frames, seq_length, projections)
                masked_sum = tf.reduce_sum(inputs, axis=[1, 2])
                mask_sum = tf.reduce_sum(mask, axis=[1, 2])

                # Avoid division by zero
                mask_sum = tf.maximum(mask_sum, tf.keras.backend.epsilon())

                # Compute the masked average
                return tf.math.divide_no_nan(masked_sum, mask_sum)
            else:
                # Default to regular global average pooling if no mask is provided
                return tf.reduce_mean(inputs, axis=[1, 2])

    def compute_output_shape(self, input_shape):
        return (input_shape[0], input_shape[-1])  # Output shape is (batch_size, num_channels)

class GeLU(keras.layers.Layer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Signal that the layer is safe for mask propagation
        self.supports_masking = True

    def call(self, inputs):
        return tf.nn.gelu(inputs)

import tensorflow as tf

class MaskedBatchNorm(tf.keras.layers.Layer):
    def __init__(self, epsilon=1e-5, momentum=0.9, **kwargs):
        super(MaskedBatchNorm, self).__init__( **kwargs)
        self.epsilon = epsilon
        self.momentum = momentum
        self.supports_masking = True

    def build(self, input_shape):
        # Trainable parameters: gamma (scale) and beta (shift)
        self.gamma = self.add_weight(shape=input_shape[-1:], initializer='ones', trainable=True, name='gamma')
        self.beta = self.add_weight(shape=input_shape[-1:], initializer='zeros', trainable=True, name='beta')

        # Running mean and variance (used during inference)
        self.moving_mean = self.add_weight(shape=input_shape[-1:], initializer='zeros', trainable=False, name='moving_mean')
        self.moving_variance = self.add_weight(shape=input_shape[-1:], initializer='ones', trainable=False, name='moving_variance')

    def call(self, inputs, mask=None, training=False):
        
        input_shape = tf.shape(inputs)
        batch_size = input_shape[0]
        dim1 = input_shape[1]
        dim2 = input_shape[2]
        dim3 = input_shape[3]
        
        if mask is not None:
            mask = tf.cast(mask, inputs.dtype)  # Ensure mask is the same type as inputs
            mask = tf.expand_dims(mask, axis=-1)  # Broadcast mask to have the same number of channels as inputs
            valid_elements = tf.reduce_sum(mask, axis=[0, 1, 2])  # Count valid elements per feature map

            # Apply mask to inputs to ignore padded elements
            masked_inputs = inputs * mask

            # Calculate mean and variance only over valid elements
            mean = tf.reduce_sum(masked_inputs, axis=[0, 1, 2]) / valid_elements
            variance = tf.reduce_sum(mask * tf.square(masked_inputs - mean), axis=[0, 1, 2]) / valid_elements

        else:
            # Standard batch normalization when no mask is provided
            mean, variance = tf.nn.moments(inputs, axes=[0, 1, 2])

        if training:
            # Update moving averages of mean and variance during training
            new_moving_mean = self.moving_mean * self.momentum + mean * (1.0 - self.momentum)
            new_moving_variance = self.moving_variance * self.momentum + variance * (1.0 - self.momentum)
            self.moving_mean.assign(new_moving_mean)
            self.moving_variance.assign(new_moving_variance)

        else:
            # Use moving mean and variance during inference
            mean = self.moving_mean
            variance = self.moving_variance

        # Normalize the inputs
        normalized_inputs = (inputs - mean) / tf.sqrt(variance + self.epsilon)

        # Scale and shift (gamma and beta)
        output = self.gamma * normalized_inputs + self.beta

        # Return the result, applying the mask again to keep padded areas unchanged (optional)
        if mask is not None:
            return output * mask  # Optionally, apply mask to retain padding
        else:
            return output

def mlp(x, hidden_units, dropout_rate=0.1):
    for units in hidden_units:
        x = tf.keras.layers.Dense(units, activation=keras.activations.gelu, use_bias=False)(x)
        x = tf.keras.layers.Dropout(dropout_rate)(x)
    return x

class ScaledDotProductAttention(tf.keras.layers.Layer):
    def __init__(self, units=128, **kwargs):
        super(ScaledDotProductAttention, self).__init__( **kwargs)
        
        self.supports_masking = True
        
#        self.W_q = tf.keras.layers.Dense(units,
#                                           use_bias=False)  # Linear layer for the query
#         self.W_k = tf.keras.layers.Dense(units,
#                                          use_bias=False)  # Linear layer for the key
                                      
#         self.W_v = tf.keras.layers.Dense(units,
#                                          use_bias=False)  # Linear layer for the key
    def call(self, inputs, mask=None):
        """
        Compute the scaled dot-product attention.
        
        Args:
        query: Tensor of shape (batch_size, num_heads, seq_len_q, depth)
        key: Tensor of shape (batch_size, num_heads, seq_len_k, depth)
        value: Tensor of shape (batch_size, num_heads, seq_len_v, depth)
        mask: (Optional) mask to ignore certain positions (e.g., padding positions)
        
        Returns:
        output: Tensor of shape (batch_size, num_heads, seq_len_q, depth)
        attention_weights: Tensor of shape (batch_size, num_heads, seq_len_q, seq_len_k)
        """
        input_shape = tf.shape(inputs)
        batch_size = input_shape[0]
        dim1 = input_shape[1]
        dim2 = input_shape[2]
        dim3 = input_shape[3]
        
        reshaped_inputs = tf.reshape(inputs, (-1, dim2, dim3)) #(batch*6, steps, features)
        query = reshaped_inputs #self.W_k(reshaped_inputs)
        key = reshaped_inputs #self.W_v(reshaped_inputs)
        
        
        if mask is not None:
            mask = tf.expand_dims(tf.reshape(mask, (-1, dim2)), axis=-1)
            query = query * tf.cast(mask, query.dtype)
            key = key * tf.cast(mask, key.dtype)
            # value = value * tf.cast(mask, key.dtype)
        value = key    
        # Dot product between query and key (sequence with itself)
        # matmul_qk = tf.matmul(reshaped_inputs, reshaped_inputs, transpose_b=True) 
        matmul_qk = tf.matmul(query, key, transpose_b=True)  # (batch_size, seq_len_q, seq_len_k)
        # Scale the dot products by sqrt(d_k)
        dk = tf.cast(tf.shape(query)[-1], inputs.dtype)
        scaled_attention_logits = matmul_qk / tf.math.sqrt(dk)  # (batch_size, seq_len_q, seq_len_k)


        if mask is not None:
            max_value = 6.55e4 if scaled_attention_logits.dtype == "float16" else 1.0e9
            mask_ = tf.logical_not(mask)
            mask_ = tf.cast(mask_, scaled_attention_logits.dtype)  # Convert mask to the same dtype as inputs
            # scaled_attention_logits = tf.cast(scaled_attention_logits, tf.float32)
            scaled_attention_logits += (mask_ * -max_value)  # Masking positions with a very large negative number

        # Softmax to get attention weights
        attention_weights = tf.nn.softmax(scaled_attention_logits, axis=-1)  # (batch_size, seq_len_q, seq_len_k)
        attention_weights = tf.cast(attention_weights, reshaped_inputs.dtype)
       
        
        # Multiply the attention weights with the value matrix
        output = tf.matmul(attention_weights, value)  # (batch_size, seq_len_q, features)
        output = tf.reshape(output * tf.cast(mask, output.dtype), input_shape)
        
        #tf.print(mask_.shape, scaled_attention_logits.shape, output.shape,output, attention_weights.shape)
        
        return output, attention_weights

class Add(tf.keras.layers.Layer):
    def __init__(self, **kwargs):
        super(Add, self).__init__( **kwargs)
        self.supports_masking = True
        self.add = tf.keras.layers.Add()
        
    def call(self, inputs, mask=None):
        
        mask = tf.cast(mask, inputs[0].dtype)
        input1 = inputs[0] * tf.expand_dims(mask[0], -1)
        input2 = inputs[1] * tf.expand_dims(mask[1], -1)
        return self.add([input1, input2])


class MaskedConv1D(tf.keras.layers.Layer):
    def __init__(self,
                 filters,
                 kernel_size,
                 strides=1,
                 axis=-1,
                 padding='valid',
                 dilation_rate=1,
                 activation=None,
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 bias_initializer='zeros',
                 kernel_regularizer=None,
                 **kwargs):
        super(MaskedConv1D, self).__init__(**kwargs)
        self.axis = axis
        self.filters = filters
        self.kernel_size = kernel_size
        self.strides = strides
        self.padding = padding.upper()
        self.dilation_rate = dilation_rate
        self.activation = tf.keras.activations.get(activation)
        self.use_bias = use_bias
        self.kernel_initializer = tf.keras.initializers.get(kernel_initializer)
        self.bias_initializer = tf.keras.initializers.get(bias_initializer)
        self.kernel_regularizer = kernel_regularizer

    def build(self, input_shape):
        channel_axis = self.axis
        input_dim = input_shape[channel_axis]
        kernel_shape = (self.kernel_size, int(input_dim), self.filters)

        self.kernel = self.add_weight(shape=kernel_shape,
                                      initializer=self.kernel_initializer,
                                      regularizer=self.kernel_regularizer,
                                      name='kernel',
                                      trainable=True)
        if self.use_bias:
            self.bias = self.add_weight(shape=(self.filters,),
                                        initializer=self.bias_initializer,
                                        name='bias',
                                        trainable=True)
        else:
            self.bias = None
        super(MaskedConv1D, self).build(input_shape)

    def call(self, inputs, mask=None):
        
        if mask is not None:
            # Expand mask dimensions to match inputs
            mask = tf.cast(mask, dtype=inputs.dtype)
            inputs = inputs *  tf.expand_dims(mask, axis=-1)  # Zero out masked positions
            

        # Reshape for Conv1D
        input_shape = tf.shape(inputs)
        batch_size = input_shape[0]
        dim1 = input_shape[1]
        dim2 = input_shape[2]
        dim3 = input_shape[3]
        
        reshaped_inputs = tf.reshape(inputs, (-1, dim2, dim3)) # batch*6, len, features
        # Perform convolution
        outputs = tf.nn.conv1d(
            input=reshaped_inputs,
            filters=self.kernel,
            stride=self.strides,
            padding=self.padding,
            dilations=self.dilation_rate,
            data_format='NWC'  # (batch, width, channels)
        )
        
        if self.use_bias:
            outputs = tf.nn.bias_add(outputs, self.bias, data_format='NWC')

        if self.activation is not None:
            outputs = self.activation(outputs)
        
         # Reshape back to the original dimensions
        output_shape = self.compute_output_shape(input_shape)
       
        
        if mask is not None:
            
            # Compute new mask after convolution
            reshaped_mask = tf.reshape(mask, (-1, dim2))
            output_mask = self.compute_output_mask(reshaped_mask)
            
            # apply mask to the outputs
            # outputs = outputs * tf.expand_dims(tf.cast(output_mask, dtype=outputs.dtype), axis=-1)
            
            # Set the mask for subsequent layers
            output_mask = tf.reshape(output_mask, output_shape[:-1]) # bactch, 6, len
            self._output_mask = output_mask

        else:
            output_mask = None


        outputs = tf.reshape(outputs, output_shape) # bactch, 6, len, features
        

        return outputs 

    def compute_output_mask(self, input_mask):
        # Compute the mask for the outputs
        kernel_size = self.kernel_size
        strides = self.strides

        # Convolve the mask with a kernel of ones
        mask = tf.expand_dims(input_mask, axis=-1)

        kernel = tf.ones((kernel_size, 1, 1), dtype=mask.dtype)
        output_mask = tf.nn.conv1d(
            input=mask,
            filters=kernel,
            stride=strides,
            padding=self.padding,
            dilations=self.dilation_rate,
            data_format='NWC'
        )

        # If all positions covered by the kernel are valid (sum equals kernel_size), output is valid
        output_mask = tf.cast(tf.equal(output_mask, kernel_size), dtype=tf.bool)
        output_mask = tf.squeeze(output_mask, axis=-1)
        
        return output_mask

    def compute_mask(self, inputs, mask=None):
        # Return the output mask computed in call()
        if hasattr(self, '_output_mask'):
            return self._output_mask
        else:
            return None

    def get_config(self):
        config = super(MaskedConv1D, self).get_config()
        config.update({
            'filters': self.filters,
            'kernel_size': self.kernel_size,
            'strides': self.strides,
            'padding': self.padding.lower(),
            'dilation_rate': self.dilation_rate,
            'activation': tf.keras.activations.serialize(self.activation),
            'use_bias': self.use_bias,
            'kernel_initializer': tf.keras.initializers.serialize(self.kernel_initializer),
            'bias_initializer': tf.keras.initializers.serialize(self.bias_initializer),
        })
        return config

    def compute_output_shape(self, input_shape):
        length = input_shape[2]
        if self.padding == 'SAME':
            out_length = tf.math.ceil(length / self.strides)
        elif self.padding == 'VALID':
            out_length = tf.math.ceil(
                (length - self.dilation_rate * (self.kernel_size - 1)) / self.strides
            )
        else:
            raise ValueError('Invalid padding type.')
        return (input_shape[0], input_shape[1], int(out_length), self.filters)

class ResidualBlock(tf.keras.layers.Layer): 
    """The Residual block of ResNet models."""
    def __init__(self, num_channels, kernel_size=5, dilation_rate=1, use_1x1conv=False, strides=1, **kwargs):
        super(ResidualBlock, self).__init__(**kwargs)
        self.supports_masking = True
        self.conv1 = MaskedConv1D(num_channels,
                                  padding='same',
                                  use_bias=False,
                                  kernel_size=kernel_size,
                                  dilation_rate=dilation_rate,
                                  strides=strides,
                                  kernel_initializer=tf.keras.initializers.HeUniform()
                                 )
        self.conv2 = MaskedConv1D(num_channels,
                                  kernel_size=kernel_size,
                                  dilation_rate=dilation_rate,
                                  use_bias=False,
                                  padding='same',
                                  kernel_initializer=tf.keras.initializers.HeUniform()
                                 )
        self.conv3 = None
        if use_1x1conv or strides > 1:
            self.conv3 = MaskedConv1D(num_channels,
                                      use_bias=False,
                                      kernel_size=1,
                                      strides=strides)
        self.ln1 = MaskedBatchNorm()
        self.ln2 = MaskedBatchNorm()
        self.activation = GeLU()
        
    def call(self, inputs, mask=None):
        x = self.activation(self.ln1(self.conv1(inputs)))
        x = self.ln2(self.conv2(x))
        if self.conv3 is not None:
            inputs = self.conv3(inputs)
        inputs += x
        return self.activation(inputs)
    
    # Todo: implement output mask computation

# To do: implement a method to set epsilon considering the data type of the tensors passed to the layers
# if not implemented correctly, this can lead to overflow/underflow issues. 
def create_simple_model(input_shape,
                        embed_dim=16,
                        name="translated",
                        ):
    
    inputs = tf.keras.Input(shape=input_shape, name=name)
    masked_inputs = tf.keras.layers.Masking(name="mask")(inputs)
    if name == "translated":
        x = tf.keras.layers.Dense(embed_dim,
                                  name='embedding',
                                  use_bias=False,
                                  kernel_initializer=keras.initializers.Orthogonal())(masked_inputs)
    elif name == "nucleotide":
        x = masked_inputs
    else:
        raise ValueError(f"{name} is invalid")
        
    x = MaskedConv1D(filters=128,
                     kernel_size=7,
                     strides=1,
                     dilation_rate=1,
                     use_bias=False,
                     name="maskedconv1d-1",
                     activation = tf.nn.gelu,
                     kernel_regularizer=tf.keras.regularizers.L2(1e-4),
                     kernel_initializer=tf.keras.initializers.HeUniform())(x)
    
    # using batchnorm here gives a big advantage. You get a model that can work well with different input size.
    # infact the accuracy increase with the increasing input size.
    x = MaskedBatchNorm(name=f"batchnorm-1")(x)
    x = MaskedConv1D(filters=128,
                     kernel_size=5,
                     strides=1,
                     dilation_rate=1,
                     use_bias=False,
                     name="maskedconv1d-2",
                     kernel_regularizer=tf.keras.regularizers.L2(1e-4),
                     activation = tf.nn.gelu,
                     kernel_initializer=tf.keras.initializers.HeUniform())(x)
    x = MaskedBatchNorm(name=f"batchnorm-2")(x)
    x = ResidualBlock(128)(x)
    x = MaskedConv1D(filters=128,
                     kernel_size=5,
                     strides=1,
                     dilation_rate=1,
                     use_bias=False,
                     name="maskedconv1d-3",
                     activation = tf.nn.gelu,
                     kernel_regularizer=tf.keras.regularizers.L2(1e-4),
                     kernel_initializer=tf.keras.initializers.HeUniform())(x)
    x = MaskedBatchNorm(name=f"batchnorm-3")(x)
    x = ResidualBlock(128, dilation_rate=3)(x)
    x = MaskedConv1D(filters=128,
                     kernel_size=5,
                     strides=2,
                     dilation_rate=1,
                     use_bias=False,
                     name="maskedconv1d-4",
                     activation = tf.nn.gelu,
                     kernel_initializer=tf.keras.initializers.HeUniform())(x)
    x = MaskedBatchNorm(name=f"batchnorm-4")(x)
    x = ResidualBlock(128)(x)
    x = MaskedConv1D(filters=128,
                     kernel_size=5,
                     strides=2,
                     dilation_rate=1,
                     use_bias=False,
                     name="maskedconv1d-5",
                     activation = tf.nn.gelu,
                     kernel_initializer=tf.keras.initializers.HeUniform())(x)
    x = MaskedBatchNorm(name=f"batchnorm-5")(x)
    x = ResidualBlock(128, dilation_rate=3)(x)
    x = tf.keras.layers.GlobalMaxPooling2D()(x)
    # batch-norm and dropout do not play nicely together https://doi.org/10.48550/arXiv.1801.05134
    x = tf.keras.layers.Dense(128,
                              activation=tf.nn.gelu,
                              name='augdense-1',
                              kernel_regularizer=tf.keras.regularizers.L2(1e-4),
                              use_bias=False)(x)
    x = tf.keras.layers.Dropout(0.2)(x)
    out = tf.keras.layers.Dense(128,
                                activation=tf.nn.gelu,
                                kernel_regularizer=tf.keras.regularizers.L2(1e-4),
                                name='augdense-2',
                                use_bias=False,
                                dtype='float32')(x)

    return inputs, out
  

class ArcFaceLoss(tf.keras.layers.Layer):
    def __init__(self, num_classes, embedding_dim, margin=0.5, scale=30.0, onehot=True, **kwargs):
        """
        Initialize the ArcFaceLoss layer for supervised metric learning.

        :param num_classes: Number of classes.
        :param margin: Angular margin to add.
        :param scale: Scaling factor for the logits.
        :param kwargs: Additional keyword arguments.
        """
        super(ArcFaceLoss, self).__init__(**kwargs)
        self.num_classes = num_classes
        self.margin = margin
        self.scale = scale
        self.embedding_dim = embedding_dim
        #self.eps = 1e-7  # Small value to avoid division by zero
        self.onehot = onehot
        # Initialize class weights for the final fully connected layer
        self.class_weights = self.add_weight(name='class_weights',
                                             shape=(self.num_classes, self.embedding_dim),
                                             initializer='glorot_uniform',
                                             trainable=True)

    def call(self, labels, embeddings):
        """
        Compute the ArcFace loss.

        :param embeddings: Embeddings from the model (batch_size, embedding_dim).
        :param labels: True labels (batch_size,).
        :return: Computed ArcFace loss.
        """
        eps = 6.55e-4 if embeddings.dtype == "float16" else 1.0e-9
        # Normalize embeddings and class weights
        embeddings = tf.nn.l2_normalize(embeddings, axis=1)
        class_weights = tf.nn.l2_normalize(self.class_weights, axis=1)
        class_weights = tf.cast(class_weights, dtype=embeddings.dtype)
        # Compute cosine similarity between embeddings and class weights
        cosine = tf.matmul(embeddings, class_weights, transpose_b=True)
        
        # Convert labels to one-hot encoding
        if self.onehot:
            labels_one_hot = tf.cast(labels, dtype=cosine.dtype)
            
        else:
            labels_one_hot = tf.squeeze(tf.one_hot(labels, depth=self.num_classes, axis=-1), axis=1)
        
        
        # Compute the angle (theta) and add margin
        theta = tf.acos(tf.clip_by_value(cosine, -1.0 + eps, 1.0 - eps))
        target_logits = tf.cos(theta + self.margin)

        # Construct logits
        logits = cosine * (1 - labels_one_hot) + target_logits * labels_one_hot

        # Apply scaling
        logits *= self.scale

        # Compute softmax cross-entropy loss
        loss = tf.nn.softmax_cross_entropy_with_logits(labels=labels_one_hot, logits=logits)
        
        return tf.reduce_mean(loss)