import numcodecs
import numpy as np

def compress_gzip(data, compression_level=9):
    """
    Compress data using GZip.
    """
    codec = numcodecs.gzip.GZip(level=compression_level)
    compressed_data = codec.encode(data.tobytes())
    return compressed_data

def decompress_gzip(compressed_data):
    """
    Decompress data compressed using GZip.
    """
    codec = numcodecs.gzip.GZip()
    decompressed_data = codec.decode(compressed_data)
    return np.frombuffer(decompressed_data, dtype=np.int16)