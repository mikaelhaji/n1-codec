import numcodecs
import numpy as np

def compress_lz4(data, acceleration=9):
    """
    Compress data using LZ4.
    """
    codec = numcodecs.lz4.LZ4(acceleration=acceleration)
    compressed_data = codec.encode(data.tobytes())
    return compressed_data

def decompress_lz4(compressed_data):
    """
    Decompress data compressed using LZ4.
    """
    codec = numcodecs.lz4.LZ4()
    decompressed_data = codec.decode(compressed_data)
    return np.frombuffer(decompressed_data, dtype=np.int16)