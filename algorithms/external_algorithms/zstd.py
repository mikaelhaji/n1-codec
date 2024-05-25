import zstandard as zstd
import json

def compress_zstd(data, compression_level=22):
    """
    Compress data using Zstandard with an optional higher compression level.
    Level 22 is typically the highest predefined level in Zstandard.
    """
    cctx = zstd.ZstdCompressor(level=compression_level)
    compressed_data = cctx.compress(data)
    return compressed_data

def decompress_zstd(compressed_data):
    dctx = zstd.ZstdDecompressor()
    decompressed_data = dctx.decompress(compressed_data)
    return decompressed_data

def serialize_tree():
    # Zstandard does not use a tree like Huffman, so we return an empty JSON
    return json.dumps({})

def deserialize_tree(serialized_tree):
    # Zstandard does not use a tree, so this function does nothing
    pass