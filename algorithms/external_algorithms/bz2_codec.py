import numcodecs
import numpy as np

def compress_bz2(data, compression_level=9):
    """
    Compress data using BZ2.
    """
    codec = numcodecs.bz2.BZ2(level=compression_level)
    compressed_data = codec.encode(data.tobytes())
    return compressed_data

def decompress_bz2(compressed_data):
    """
    Decompress data compressed using BZ2.
    """
    codec = numcodecs.bz2.BZ2()
    decompressed_data = codec.decode(compressed_data)
    return np.frombuffer(decompressed_data, dtype=np.int16)





# 8 => 3.11
# 9 => 3.11