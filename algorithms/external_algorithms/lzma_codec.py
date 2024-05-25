import numcodecs
import numpy as np

def compress_lzma(data, compression_level=9):
    """
    Compress data using LZMA.
    """
    codec = numcodecs.lzma.LZMA(preset=compression_level)
    compressed_data = codec.encode(data.tobytes())
    return compressed_data

def decompress_lzma(compressed_data):
    """
    Decompress data compressed using LZMA.
    """
    codec = numcodecs.lzma.LZMA()
    decompressed_data = codec.decode(compressed_data)
    return np.frombuffer(decompressed_data, dtype=np.int16)