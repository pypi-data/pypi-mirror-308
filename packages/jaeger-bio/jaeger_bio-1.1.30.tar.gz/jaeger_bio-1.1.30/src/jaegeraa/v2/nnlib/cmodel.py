import tensorflow as tf # type: ignore
import tensorflow.keras as keras  # type: ignore
from tensorflow.keras.layers import InputSpec # type: ignore
import tensorflow.keras.backend as K # type: ignore
from  jaegeraa.utils import recall_m, precision_m

class JaegerModel(tf.keras.Model):
    
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        
        self.step = 0
        self.loss_tracker = tf.keras.metrics.Mean(name="loss")
        self.regularization_loss_tracker = tf.keras.metrics.Mean(name="reg-loss")
        self.precision_tracker = tf.keras.metrics.Mean(name="precision") # keeps track on current precision 
        self.recall_tracker = tf.keras.metrics.Mean(name="recall") # keeps track on current precision 
        self.gradient_tracker = tf.keras.metrics.Mean(name="gradient") # keeps track of train-time gradients 
        
    def compile(self,optimizer, loss_fn, **kwargs):
        super().compile()

        #tf.nn.softmax_cross_entropy_with_logits
        # Prepare the metrics.
        self.loss_fn = loss_fn
        self.precision = precision_m
        self.recall = recall_m
        self.optimizer = optimizer
        #self.arcface = arcface
        
        
    def train_step(self, data):
        
        if len(data) == 3:
            #sample weights is class weights when a dictionary of class weights is provided to .fit
            x, y, sample_weights = data
            #tf.print(sample_weights)
        else:
            sample_weights = None
            x, y = data
            
        #tf.print(data)
        loss = 0
        with tf.GradientTape(persistent=True) as tape:
            y_pred = self(x, training=True)  # Forward pass
            y = tf.cast(y, dtype=y_pred.dtype)
            loss += self.loss_fn(y, y_pred, sample_weights)
            loss +=sum(self.losses)
            loss_scaled = self.optimizer.get_scaled_loss(loss)
   
        
  
        grads = tape.gradient(loss_scaled, self.trainable_variables )

        grads = self.optimizer.get_unscaled_gradients(grads)

        self.optimizer.apply_gradients(zip(grads, self.trainable_variables ))  # Loss scale is updated here

        #custom step tracker
        self.step +=1
        if self.step % 100 == 0:
            self.loss_tracker.reset_state()
            self.gradient_tracker.reset_state()
        self.loss_tracker.update_state(loss)
        self.regularization_loss_tracker.update_state(sum(self.losses))
        
        # avg_grad_norms = []
        for grad, weight in zip(grads, self.trainable_weights):
            # Compute the average gradient norm for the current layer
            norm = tf.norm(grad)
            # norm = tf.clip_by_value(tf.norm(grad), clip_value_min=-1000, clip_value_max=1000)
            # avg_norm = norm / tf.math.reduce_prod(weight.shape)
            self.gradient_tracker.update_state(norm)

        return {"loss": self.loss_tracker.result(),
                "reg-loss": self.regularization_loss_tracker.result(),
                "grad": self.gradient_tracker.result(),
                "lr":self.optimizer.learning_rate}
    
    def test_step(self, data):
        # Unpack the data
        x, y = data
        #tf.print(x)
        y_pred = self(x, training=False)
        y = tf.cast(y, dtype=y_pred.dtype)
        #tf.print(y_pred)
        # Updates the metrics tracking the loss
        loss = self.loss_fn(y, y_pred)

        self.loss_tracker.update_state(loss)
        
        # Compute probabilities from logits 
        y_pred = tf.keras.activations.softmax(y_pred)
        # Update the metrics.
        precision = self.precision(y, y_pred)
        recall = self.recall(y, y_pred)
        self.precision_tracker.update_state(precision)
        self.recall_tracker.update_state(recall)
        
        return {"loss": self.loss_tracker.result(),
                "precision": self.precision_tracker.result(), 
                "recall": self.recall_tracker.result()}
    
    def predict_step(self, data):
        # Unpack the data
        x, y = data[0], data[1:]
        # set model to inference mode
        y_logits = self(x, training=False)
        return {"y_hat": y_logits, "meta": y}
    
    @property
    def metrics(self):
        return [self.loss_tracker,
                self.regularization_loss_tracker,
                self.recall_tracker,
                self.precision_tracker,
                self.gradient_tracker
                ]



class MetricModel(tf.keras.Model):
    
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        
        self.step = 0
        self.loss_tracker = tf.keras.metrics.Mean(name="loss")
        self.regularization_loss_tracker = tf.keras.metrics.Mean(name="reg-loss")
        self.precision_tracker = tf.keras.metrics.Mean(name="precision") # keeps track on current precision 
        self.recall_tracker = tf.keras.metrics.Mean(name="recall") # keeps track on current precision 
        self.gradient_tracker = tf.keras.metrics.Mean(name="gradient") # keeps track of train-time gradients 
        
    def compile(self,optimizer, loss_fn, arcface=None,**kwargs):
        super().compile()

        #tf.nn.softmax_cross_entropy_with_logits
        # Prepare the metrics.
        self.loss_fn = loss_fn
        self.precision = precision_m
        self.recall = recall_m
        self.optimizer = optimizer
        #self.arcface = arcface
        
        
    def train_step(self, data):
        
        if len(data) == 3:
            #sample weights is class weights when a dictionary of class weights is provided to .fit
            x, y, sample_weights = data
            #tf.print(sample_weights)
        else:
            sample_weights = None
            x, y = data
            
        #tf.print(data)
        loss = 0
        with tf.GradientTape(persistent=True) as tape:
            y_pred = self(x, training=True)  # Forward pass

            loss += tf.cast(self.loss_fn([y, y_pred]), y.dtype)
            #loss += self.loss_fn(y, y_pred, sample_weights)
            loss += sum(self.losses)
            loss_scaled = self.optimizer.get_scaled_loss(loss)
   
        
  
        grads = tape.gradient(loss_scaled, self.trainable_variables )
        grads_B = tape.gradient(loss_scaled, self.loss_fn.trainable_variables)
        
        grads = self.optimizer.get_unscaled_gradients(grads)
        grads_B = self.optimizer.get_unscaled_gradients(grads_B)
        self.optimizer.apply_gradients(zip(grads, self.trainable_variables ))  # Loss scale is updated here
        self.optimizer.apply_gradients(zip(grads_B, self.loss_fn.trainable_variables))

        #custom step tracker
        self.step +=1
        if self.step % 100 == 0:
            self.loss_tracker.reset_state()
            self.gradient_tracker.reset_state()
        self.loss_tracker.update_state(loss)
        self.regularization_loss_tracker.update_state(sum(self.losses))
        
        # avg_grad_norms = []
        for grad, weight in zip(grads, self.trainable_weights):
            # Compute the average gradient norm for the current layer
            norm = tf.norm(grad)
            # norm = tf.clip_by_value(tf.norm(grad), clip_value_min=-1000, clip_value_max=1000)
            # avg_norm = norm / tf.math.reduce_prod(weight.shape)
                
            self.gradient_tracker.update_state(norm)

        return {"loss": self.loss_tracker.result(),
                "reg-loss": self.regularization_loss_tracker.result(),
                "grad": self.gradient_tracker.result(),
                "lr":self.optimizer.learning_rate}
    
    def test_step(self, data):
        # Unpack the data
        x, y = data

        y_pred = self(x, training=False)
        y = tf.cast(y, dtype=y_pred.dtype)
        # Updates the metrics tracking the loss
        loss = self.loss_fn([y, y_pred])

        self.loss_tracker.update_state(loss)

        return {"loss": self.loss_tracker.result()}

    @property
    def metrics(self):
        return [self.loss_tracker,
                self.regularization_loss_tracker,
                self.recall_tracker,
                self.precision_tracker,
                self.gradient_tracker
                ]
