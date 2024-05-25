from wavpack_numcodecs import WavPack
import numpy as np

def compress_wavpack(data, level=4):
    """
    Compress data using WavPack.
    """
    try:
        wv_compressor = WavPack(level=level)
        # Ensure data is a NumPy array with a dtype attribute
        if not isinstance(data, np.ndarray):
            data = np.array(data)
        compressed_data = wv_compressor.encode(data)
        return compressed_data
    except AssertionError as e:
        print(f"Assertion error during WavPack compression: {e}")
        raise
    except Exception as e:
        print(f"General error during compression: {e}")
        raise

def decompress_wavpack(compressed_data):
    """
    Decompress data compressed using WavPack.
    """
    try:
        wv_compressor = WavPack()
        decompressed_data = wv_compressor.decode(compressed_data)
        return np.frombuffer(decompressed_data, dtype=np.int16)
    except Exception as e:
        print(f"Error during decompression: {e}")
        raise