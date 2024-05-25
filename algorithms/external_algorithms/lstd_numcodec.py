import numcodecs
import numpy as np

def compress_lstd_numcodec(data, compression_level=22):
    """
    Compress data using Zstandard through numcodecs.
    """
    codec = numcodecs.zstd.Zstd(level=compression_level)
    compressed_data = codec.encode(data.tobytes())
    return compressed_data

def decompress_lstd_numcodec(compressed_data):
    """
    Decompress data compressed using Zstandard through numcodecs.
    """
    codec = numcodecs.zstd.Zstd()
    decompressed_data = codec.decode(compressed_data)
    return np.frombuffer(decompressed_data, dtype=np.int16)




# CR = 2.41