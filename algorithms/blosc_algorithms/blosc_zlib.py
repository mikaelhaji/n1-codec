import numcodecs
import numpy as np

def compress_blosc_zlib(data, compression_level=9):
    """
    Compress data using Blosc with the zlib compressor.
    """
    # Create a Blosc codec instance with zlib
    codec = numcodecs.blosc.Blosc(cname='zlib', clevel=compression_level, shuffle=numcodecs.blosc.SHUFFLE)
    compressed_data = codec.encode(data.tobytes())
    return compressed_data

def decompress_blosc_zlib(compressed_data):
    """
    Decompress data compressed using Blosc with the zlib compressor.
    """
    # Create a Blosc codec instance with zlib
    codec = numcodecs.blosc.Blosc(cname='zlib')
    decompressed_data = codec.decode(compressed_data)
    return np.frombuffer(decompressed_data, dtype=np.int16)