import numcodecs
import numpy as np

def compress_blosc_lz4hc(data, compression_level=9):
    """
    Compress data using Blosc with the lz4hc compressor.
    """
    # Create a Blosc codec instance with lz4hc
    codec = numcodecs.blosc.Blosc(cname='lz4hc', clevel=compression_level, shuffle=numcodecs.blosc.SHUFFLE)
    compressed_data = codec.encode(data.tobytes())
    return compressed_data

def decompress_blosc_lz4hc(compressed_data):
    """
    Decompress data compressed using Blosc with the lz4hc compressor.
    """
    # Create a Blosc codec instance with lz4hc
    codec = numcodecs.blosc.Blosc(cname='lz4hc')
    decompressed_data = codec.decode(compressed_data)
    return np.frombuffer(decompressed_data, dtype=np.int16)