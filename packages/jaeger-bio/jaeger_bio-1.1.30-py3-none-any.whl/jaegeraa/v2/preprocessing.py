import logging
import pyfastx 
import tensorflow as tf
import progressbar
from jaegeraa.utils import signal_l, safe_divide

logger = logging.getLogger("Jaeger")
progressbar.streams.wrap_stderr()



def fasta_gen(file_path,
              fragsize=None,
              stride=None,
              num=None,
              ):
    """
    Generates fragments of DNA sequences from a FASTA file.

    Args:
    ----
        filehandle: File handle for reading DNA sequences.
        fragsize (int, optional): Size of the DNA sequence fragments. Defaults
        to None.
        stride (int, optional): Stride for fragment generation. Defaults to
        None.
        num (int, optional): Total number of sequences to process. Defaults
        to None.
        disable (bool, optional): Flag to disable progress bar. Defaults to
        False.

    Returns:
    -------
        generator: A generator that yields DNA sequence fragments with
        associated information.
    """

    def seqgen():
        # accepts a reference to a file handle
        fa = pyfastx.Fasta(file_path, build_index=False)
        with progressbar.ProgressBar(max_value=num) as pbar:
            for j, record in enumerate(fa):
                pbar.update(j)
                seqlen = len(
                    record[1]
                )  # move size filtering to a separate preprocessing step
                sequence = record[1].strip()
                header = record[0].strip().replace(",", "__")
                # logger.debug(sequence)
                # sequence = str(record[1]).upper()
                # filters the sequence based on size
                if seqlen >= fragsize:
                    # if no fragsize, return the entire sequence
                    if fragsize is None:
                        # sequence and sequence headder
                        yield f"{sequence},{header}"
                    elif fragsize is not None:

                        for i, (l, index) in enumerate(
                            signal_l(
                                range(
                                    0,
                                    seqlen - (fragsize - 1),
                                    fragsize if stride is None else stride,
                                )
                            )
                        ):
                            g = sequence[index: index + fragsize].count("G")
                            c = sequence[index: index + fragsize].count("C")
                            a = sequence[index: index + fragsize].count("A")
                            t = sequence[index: index + fragsize].count("T")
                            gc_skew = safe_divide((g - c), (g + c))
                            # sequnce_fragment, contig_id, index, contig_end, i,
                            # g, c, gc_skew
                            yield f"{sequence[index : index + fragsize]},{header},{index},{l},{i},{seqlen},{g},{c},{a},{t},{gc_skew : .3f}"

    return seqgen


def fasta_gen_lib(filename, fragsize=None, stride=None, num=None):
    """
    Generates fragments of DNA sequences from various input types.

    Args:
    ----
        filehandle: Input source for DNA sequences, can be a file handle,
                    string, list, Seq object, generator, or file object.
        fragsize (int, optional): Size of the DNA sequence fragments.
                                  Defaults to None.
        stride (int, optional): Stride for fragment generation.
                                Defaults to None.
        num (int, optional): Total number of sequences to process.
                             Defaults to None.

    Returns:
    -------
        generator: A generator that yields DNA sequence fragments with
                   associated information.

    Raises:
    ------
        ValueError: If the input type is not supported.
    """

    head = False
    if isinstance(filename, str):
        tmpfn = pyfastx.Fasta(filename, build_index=False)
        head = True
    else:
        raise ValueError("Not a supported input type")

    def seqgen():
        # accepts a reference to a file handle
        for n, record in enumerate(tmpfn):
            if head:
                seqlen = len(
                    record[1]
                )  # move size filtering to a separate preprocessing step
                seq = record[1]
                headder = record[0].replace(",", "__")

            else:
                seqlen = len(record)
                seq = record
                headder = f"seq_{n}"
            # filters the sequence based on size
            if seqlen >= fragsize:
                # if no fragsize, return the entire sequence
                if fragsize is None:
                    yield f"{str(seq)},{str(headder)}"
                elif fragsize is not None:
                    for i, (l, index) in enumerate(
                        signal_l(
                            range(
                                0,
                                seqlen - (fragsize - 1),
                                fragsize if stride is None else stride,
                            )
                        )
                    ):
                        yield f"{str(seq)[index:index + fragsize]},{str(headder)},{str(index)},{str(l)},{str(i)},{str(seqlen)}"

    return seqgen


# Second generation preprocessing code
CODONS = [
    "TTT",
    "TTC",
    "TTA",
    "TTG",
    "CTT",
    "CTC",
    "CTA",
    "CTG",
    "ATT",
    "ATC",
    "ATA",
    "ATG",
    "GTT",
    "GTC",
    "GTA",
    "GTG",
    "TCT",
    "TCC",
    "TCA",
    "TCG",
    "CCT",
    "CCC",
    "CCA",
    "CCG",
    "ACT",
    "ACC",
    "ACA",
    "ACG",
    "GCT",
    "GCC",
    "GCA",
    "GCG",
    "TAT",
    "TAC",
    "TAA",
    "TAG",
    "CAT",
    "CAC",
    "CAA",
    "CAG",
    "AAT",
    "AAC",
    "AAA",
    "AAG",
    "GAT",
    "GAC",
    "GAA",
    "GAG",
    "TGT",
    "TGC",
    "TGA",
    "TGG",
    "CGT",
    "CGC",
    "CGA",
    "CGG",
    "AGT",
    "AGC",
    "AGA",
    "AGG",
    "GGT",
    "GGC",
    "GGA",
    "GGG",
]

AMINO = [
    "F",
    "F",
    "L",
    "L",
    "L",
    "L",
    "L",
    "L",
    "I",
    "I",
    "I",
    "M",
    "V",
    "V",
    "V",
    "V",
    "S",
    "S",
    "S",
    "S",
    "P",
    "P",
    "P",
    "P",
    "T",
    "T",
    "T",
    "T",
    "A",
    "A",
    "A",
    "A",
    "Y",
    "Y",
    "*",
    "*",
    "H",
    "H",
    "Q",
    "Q",
    "N",
    "N",
    "K",
    "K",
    "D",
    "D",
    "E",
    "E",
    "C",
    "C",
    "*",
    "W",
    "R",
    "R",
    "R",
    "R",
    "S",
    "S",
    "R",
    "R",
    "G",
    "G",
    "G",
    "G",
]


PC2 = {
    "I": "A",
    "V": "A",
    "L": "A",
    "F": "A",
    "Y": "A",
    "W": "A",
    "H": "B",
    "K": "B",
    "R": "B",
    "D": "B",
    "E": "B",
    "G": "A",
    "A": "A",
    "C": "A",
    "S": "A",
    "T": "A",
    "M": "A",
    "Q": "B",
    "N": "B",
    "P": "A",
}

PC2_NUM = [
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    0,
    0,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    1,
    1,
    0,
    1,
    2,
    2,
    2,
    2,
    1,
    1,
    2,
    2,
    1,
    1,
    1,
    1,
]

MURPHY10 = {
    "A": "A",
    "C": "C",
    "G": "G",
    "H": "H",
    "P": "P",
    "L": "L",
    "V": "L",
    "I": "L",
    "M": "L",
    "S": "S",
    "T": "S",
    "F": "F",
    "Y": "F",
    "W": "F",
    "E": "E",
    "D": "E",
    "N": "E",
    "Q": "E",
    "K": "K",
    "R": "K",
}

PC5 = {
    "I": "A",
    "V": "A",
    "L": "A",
    "F": "R",
    "Y": "R",
    "W": "R",
    "H": "R",
    "K": "C",
    "R": "C",
    "D": "C",
    "E": "C",
    "G": "T",
    "A": "T",
    "C": "T",
    "S": "T",
    "T": "D",
    "M": "D",
    "Q": "D",
    "N": "D",
    "P": "D",
}

AMINO_NUM = [
    1,
    1,
    2,
    2,
    2,
    2,
    2,
    2,
    3,
    3,
    3,
    4,
    5,
    5,
    5,
    5,
    6,
    6,
    6,
    6,
    7,
    7,
    7,
    7,
    8,
    8,
    8,
    8,
    9,
    9,
    9,
    9,
    10,
    10,
    0,
    0,
    11,
    11,
    12,
    12,
    13,
    13,
    14,
    14,
    15,
    15,
    16,
    16,
    17,
    17,
    0,
    18,
    19,
    19,
    19,
    19,
    6,
    6,
    19,
    19,
    20,
    20,
    20,
    20,
]
BIAS_NUM = [
    1,
    2,
    1,
    2,
    3,
    4,
    5,
    6,
    1,
    2,
    3,
    1,
    1,
    2,
    3,
    4,
    1,
    2,
    3,
    4,
    1,
    2,
    3,
    4,
    1,
    2,
    3,
    4,
    1,
    2,
    3,
    4,
    1,
    2,
    1,
    2,
    1,
    2,
    1,
    2,
    1,
    2,
    1,
    2,
    1,
    2,
    1,
    2,
    1,
    2,
    1,
    2,
    1,
    2,
    3,
    4,
    5,
    6,
    5,
    6,
    1,
    2,
    3,
    4,
]

MURPHY10_NUM = [
    1,
    1,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    3,
    3,
    3,
    3,
    4,
    4,
    4,
    4,
    3,
    3,
    3,
    3,
    5,
    5,
    5,
    5,
    1,
    1,
    0,
    0,
    6,
    6,
    7,
    7,
    7,
    7,
    8,
    8,
    7,
    7,
    7,
    7,
    9,
    9,
    0,
    1,
    8,
    8,
    8,
    8,
    3,
    3,
    8,
    8,
    10,
    10,
    10,
    10,
]

PC5_NUM= [
    1,
    1,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    3,
    2,
    2,
    2,
    2,
    4,
    4,
    4,
    4,
    3,
    3,
    3,
    3,
    3,
    3,
    3,
    3,
    4,
    4,
    4,
    4,
    1,
    1,
    0,
    0,
    1,
    1,
    3,
    3,
    3,
    3,
    5,
    5,
    5,
    5,
    5,
    5,
    4,
    4,
    0,
    1,
    5,
    5,
    5,
    5,
    4,
    4,
    5,
    5,
    4,
    4,
    4,
    4,
]

CODONS_NUM = list(range(65))

MAPS = {
"AMINO" : AMINO_NUM,
"CODONS": CODONS_NUM,
"MURPHY10": MURPHY10_NUM,
"PC2": PC2_NUM,
"PC5": PC5_NUM,
"BIAS" : BIAS_NUM
}

# map codons to amino acids
def codon_mapper(map="murphy10"):
    """
    Creates a static hash table for mapping codons to standard amino acid or
    reduced amino acid alphabets

    Args:
    ----
    maps_to (string) : one of murphy10, pc5, pc2, amino, bias or codon

    Returns:
    -------
        tf.lookup.StaticHashTable: A static hash table for codon mapping.
    """
    map = map.upper() 
    if map in MAPS:
        map = MAPS[map]

    keys = tf.constant(CODONS)
    values = tf.constant(map)
    hash_init = tf.lookup.KeyValueTensorInitializer(keys, values)
    return tf.lookup.StaticHashTable(hash_init, default_value=-1), max(map)+1

# convert to complement
def complement_mapper():
    """
    Creates a static hash table for mapping nucleotides to their complements.

    Returns:
    -------
        tf.lookup.StaticHashTable: A static hash table for nucleotide
                                   complement mapping.
    """

    keys = tf.constant([b"A", b"T", b"G", b"C", b"a", b"t", b"g", b"c"])
    vals = tf.constant([b"T", b"A", b"C", b"G", b"t", b"a", b"c", b"g"])
    hash_init = tf.lookup.KeyValueTensorInitializer(keys, vals)
    return tf.lookup.StaticHashTable(hash_init, default_value="N")


def nucleotide_mapper():
    """
    Creates a static hash table for mapping nucleotides to their numerical
    encodings.

    Returns:
    -------
        tf.lookup.StaticHashTable: A static hash table for nucleotide encoding
                                   mapping.
    """

    keys = tf.constant([b"A", b"G", b"C", b"T", b"a", b"g", b"c", b"t"])
    vals = tf.constant([0, 1, 2, 3, 0, 1, 2, 3])
    hash_init = tf.lookup.KeyValueTensorInitializer(keys, vals)
    return tf.lookup.StaticHashTable(hash_init, default_value=-1)


def process_string(
    map="codon",
    crop_size=1024,
    timesteps=False,
    num_time=None,
    fragsize=200,
    mutate=False,
    mutation_rate=0.1,
):
    """
    Processes a DNA sequence string by mapping codons, nucleotides, and codon
    biases.

    Args:
    ----
        onehot (bool, optional): Flag to indicate one-hot encoding. Defaults
                                 to True.
        crop_size (int, optional): Size for cropping the sequence. Defaults
                                   to 1024.
        maxval (int, optional): Maximum value for mutation. Defaults to 400.
        timesteps (bool, optional): Flag to reshape output for time steps.
                                    Defaults to False.
        num_time (int, optional): Number of time steps. Defaults to None.
        fragsize (int, optional): Size of the DNA sequence fragments. Defaults
                                  to 200.
        mutate (bool, optional): Flag to enable mutation. Defaults to False.
        mutation_rate (float, optional): Probability of mutation. Defaults
                                         to 0.1.

    Returns:
    -------
        function: A function that processes a DNA sequence string and returns
        mapped codons, nucleotides, and codon biases.
    """

    @tf.function
    def p(string):

        CODON_MAPPER, DEPTH = codon_mapper(map=map)
        COMPLEMENT_MAPPER = complement_mapper()
        NUCLEOTIDE_MAPPER = nucleotide_mapper()

        x = tf.strings.split(string, sep=",")

        if (crop_size % 3) == 0:
            offset = -2
        elif (crop_size % 3) == 1:
            offset = -1
        elif (crop_size % 3) == 2:
            offset = 0

        forward_strand = tf.strings.bytes_split(x[0])[:crop_size]

        if mutate:
            # Probability of mutation (adjust as needed)
            mutation_prob = mutation_rate
            # Minimum possible value for mutation
            min_value = 0
            # Maximum possible value for mutation
            max_value = 4

            alphabet = tf.constant(["A", "T", "G", "C", "N"], dtype=tf.string)

            mask = (
                tf.random.uniform(
                    shape=tf.shape(forward_strand), minval=0.0, maxval=1.0
                )
                < mutation_prob
            )
            mutation_values = tf.random.uniform(
                shape=tf.shape(forward_strand),
                minval=min_value,
                maxval=max_value,
                dtype=tf.int32,
            )
            selected_strings = tf.gather(alphabet, mutation_values)
            forward_strand = tf.where(mask, selected_strings, forward_strand)

        # generate the reverse strand for the mutated forward strand
        reverse_strand = COMPLEMENT_MAPPER.lookup(forward_strand[::-1])

        nuc1 = NUCLEOTIDE_MAPPER.lookup(forward_strand[:])
        nuc2 = NUCLEOTIDE_MAPPER.lookup(reverse_strand[:])

        tri_forward = tf.strings.ngrams(forward_strand,
                                        ngram_width=3,
                                        separator="")
        tri_reverse = tf.strings.ngrams(reverse_strand,
                                        ngram_width=3,
                                        separator="")

        f1 = CODON_MAPPER.lookup(tri_forward[: -3 + offset: 3])
        f2 = CODON_MAPPER.lookup(tri_forward[1: -2 + offset: 3])
        f3 = CODON_MAPPER.lookup(tri_forward[2: -1 + offset: 3])

        r1 = CODON_MAPPER.lookup(tri_reverse[: -3 + offset: 3])
        r2 = CODON_MAPPER.lookup(tri_reverse[1: -2 + offset: 3])
        r3 = CODON_MAPPER.lookup(tri_reverse[2: -1 + offset: 3])

        if timesteps:
            f1 = tf.reshape(f1, (num_time, fragsize))
            f2 = tf.reshape(f2, (num_time, fragsize))
            f3 = tf.reshape(f3, (num_time, fragsize))
            r1 = tf.reshape(r1, (num_time, fragsize))
            r2 = tf.reshape(r2, (num_time, fragsize))
            r3 = tf.reshape(r3, (num_time, fragsize))
            seq = tf.stack([f1, f2, f3, r1, r2, r3], 1)
        else:
            seq = tf.stack([f1, f2, f3, r1, r2, r3], 0)
            nuc = tf.stack([nuc1,nuc2],0)
            # code = tf.stack([fb1,fb2,fb3,rb1,rb2,rb3],0) # codon bias encoder

        return (
            {
                "translated": tf.one_hot(
                    seq, depth=DEPTH, dtype=tf.float32, on_value=1, off_value=0
                ),
                'nucleotide': tf.one_hot(
                    nuc, depth=4, dtype=tf.float32, on_value=1, off_value=0
                )
            },
            x[1],
            x[2],
            x[3],
            x[4],
            x[5],
            x[6],
            x[7],
            x[8],
            x[9],
            x[10],
        )
        # 'nucleotide': tf.one_hot(nuc, depth=4, dtype=tf.float32, on_value=1,\
        # off_value=0)},

    return p


def process_string_textline(map="codon", numclasses=4, crop_size=1024):
    """
    Processes a DNA sequence textline (CSV file) by mapping codons and nucleotides.

    Args:
    ----
        onehot (bool, optional): Flag to indicate one-hot encoding.
                                 Defaults to True.
        label_onehot (bool, optional): Flag to indicate one-hot encoding
                                       for labels. Defaults to True.
        numclasses (int, optional): Number of classes for label encoding.
                                    Defaults to 4.

    Returns:
    -------
        function: A function that processes a DNA sequence text line and
                  returns mapped codons, nucleotides, and labels.
    """

    def p(string):

        if (crop_size % 3) == 0:
            offset = -2
        elif (crop_size % 3) == 1:
            offset = -1
        elif (crop_size % 3) == 2:
            offset = 0

        CODON_MAPPER, DEPTH = codon_mapper()
        COMPLEMENT_MAPPER = complement_mapper()
        NUCLEOTIDE_MAPPER = nucleotide_mapper()
        x = tf.strings.split(string, sep=",")

        label = tf.strings.to_number(x[0], tf.int32)
        label = tf.cast(label, dtype=tf.int32)

        forward_strand = tf.strings.bytes_split(x[1])
        reverse_strand = COMPLEMENT_MAPPER.lookup(forward_strand[::-1])

        nuc1 = NUCLEOTIDE_MAPPER.lookup(forward_strand[:])
        nuc2 = NUCLEOTIDE_MAPPER.lookup(reverse_strand[:])

        tri_forward = tf.strings.ngrams(forward_strand,
                                        ngram_width=3,
                                        separator="")
        tri_reverse = tf.strings.ngrams(reverse_strand,
                                        ngram_width=3,
                                        separator="")

        f1 = CODON_MAPPER.lookup(tri_forward[: -3 + offset: 3])
        f2 = CODON_MAPPER.lookup(tri_forward[1: -2 + offset: 3])
        f3 = CODON_MAPPER.lookup(tri_forward[2: -1 + offset: 3])

        r1 = CODON_MAPPER.lookup(tri_reverse[: -3 + offset: 3])
        r2 = CODON_MAPPER.lookup(tri_reverse[1: -2 + offset: 3])
        r3 = CODON_MAPPER.lookup(tri_reverse[2: -1 + offset: 3])

        seq = tf.stack([f1, f2, f3, r1, r2, r3], 0)
        nuc = tf.stack([nuc1,nuc2], 0)


        label = tf.one_hot(
                label,
                depth=numclasses,
                dtype=tf.float32,
                on_value=1,
                off_value=0
            )

        return {
                "translated": tf.one_hot(
                    seq, depth=DEPTH, dtype=tf.float32, on_value=1, off_value=0
                ),
                'nucleotide': tf.one_hot(
                    nuc, depth=4, dtype=tf.float32, on_value=1, off_value=0
                )
            }, label

    return p