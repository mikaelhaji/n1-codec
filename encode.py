#!/usr/bin/env python3
import sys
import json
import numpy as np
from scipy.io import wavfile
import algorithms.entropy_coding.huffman
import algorithms.predictive_coding.delta
import algorithms.external_algorithms.zstd
import algorithms.blosc_algorithms.blosc_zstd
import algorithms.blosc_algorithms.blosc_lz4
import algorithms.blosc_algorithms.blosc_lz4hc
import algorithms.blosc_algorithms.blosc_zlib
import algorithms.external_algorithms.gzip_codec
import algorithms.external_algorithms.lzma_codec
import algorithms.external_algorithms.lz4_codec
import algorithms.external_algorithms.lstd_numcodec
import algorithms.external_algorithms.bz2_codec
import algorithms.audio_coding.wavpack_codec
import logging

# Setup logging
logging.basicConfig(filename='logs/compression.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def compress_wav_file(input_file, output_file, tree_file, mode):
    sample_rate, signal = wavfile.read(input_file)
    logging.debug("Pre-compression signal samples (all): %s", signal)  # Log all samples of the signal
    serialized_tree = "{}"  # Default empty JSON object as a string
    encoded_bytes = None  # Initialize encoded_bytes to None or a suitable default
    
    if mode == 'huff':
        encoded_bytes, serialized_tree, padding = algorithms.entropy_coding.huffman.compress_huffman(signal)
    elif mode == 'delta_huff':
        delta_encoded_signal = algorithms.predictive_coding.delta.apply_delta_encoding(signal)
        encoded_bytes, serialized_tree, padding = algorithms.entropy_coding.huffman.compress_huffman(delta_encoded_signal)
    elif mode == 'zstd':
        encoded_bytes = algorithms.external_algorithms.zstd.compress_zstd(signal.tobytes())
        serialized_tree = algorithms.external_algorithms.zstd.serialize_tree()
    elif mode == 'delta_zstd':
        delta_encoded_signal = algorithms.predictive_coding.delta.apply_delta_encoding(signal)
        encoded_bytes = algorithms.external_algorithms.zstd.compress_zstd(delta_encoded_signal.tobytes())
        serialized_tree = algorithms.external_algorithms.zstd.serialize_tree()
    elif mode == 'blosc_zstd':
        encoded_bytes = algorithms.blosc_algorithms.blosc_zstd.compress_blosc_zstd(signal)
        serialized_tree = json.dumps({})  # No tree needed for Blosc-Zstd
    elif mode == 'delta_blosc_zstd':
        delta_encoded_signal = algorithms.predictive_coding.delta.apply_delta_encoding(signal)
        encoded_bytes = algorithms.blosc_algorithms.blosc_zstd.compress_blosc_zstd(delta_encoded_signal)
        serialized_tree = json.dumps({})  # No tree needed for Blosc-Zstd
    elif mode == 'blosc_lz4':
        encoded_bytes = algorithms.blosc_algorithms.blosc_lz4.compress_blosc_lz4(signal)
        serialized_tree = json.dumps({})  # No tree needed for Blosc-Zstd
    elif mode == 'delta_blosc_lz4':
        delta_encoded_signal = algorithms.predictive_coding.delta.apply_delta_encoding(signal)
        encoded_bytes = algorithms.blosc_algorithms.blosc_lz4.compress_blosc_lz4(delta_encoded_signal)
        serialized_tree = json.dumps({})  # No tree needed for Blosc-Zstd
    elif mode == 'blosc_lz4hc':
        encoded_bytes = algorithms.blosc_algorithms.blosc_lz4hc.compress_blosc_lz4hc(signal)
        serialized_tree = json.dumps({})  # No tree needed for Blosc-Zstd
    elif mode == 'delta_blosc_lz4hc':
        delta_encoded_signal = algorithms.predictive_coding.delta.apply_delta_encoding(signal)
        encoded_bytes = algorithms.blosc_algorithms.blosc_lz4hc.compress_blosc_lz4hc(delta_encoded_signal)
        serialized_tree = json.dumps({})  # No tree needed for Blosc-Zstd
    elif mode == 'blosc_zlib':
        encoded_bytes = algorithms.blosc_algorithms.blosc_zlib.compress_blosc_zlib(signal)
        serialized_tree = json.dumps({})  # No tree needed for Blosc-Zstd
    elif mode == 'delta_blosc_zlib':
        delta_encoded_signal = algorithms.predictive_coding.delta.apply_delta_encoding(signal)
        encoded_bytes = algorithms.blosc_algorithms.blosc_zlib.compress_blosc_zlib(delta_encoded_signal)
        serialized_tree = json.dumps({})  # No tree needed for Blosc-Zstd
    elif mode == 'gzip':
        encoded_bytes = algorithms.external_algorithms.gzip_codec.compress_gzip(signal)
        serialized_tree = json.dumps({})  # No tree needed for GZip
    elif mode == 'delta_gzip':
        delta_encoded_signal = algorithms.predictive_coding.delta.apply_delta_encoding(signal)
        encoded_bytes = algorithms.external_algorithms.gzip_codec.compress_gzip(delta_encoded_signal)
        serialized_tree = json.dumps({})  # No tree needed for GZip
    elif mode == 'lzma':
        encoded_bytes = algorithms.external_algorithms.lzma_codec.compress_lzma(signal)
        serialized_tree = json.dumps({})  # No tree needed for LZMA
    elif mode == 'delta_lzma':
        delta_encoded_signal = algorithms.predictive_coding.delta.apply_delta_encoding(signal)
        encoded_bytes = algorithms.external_algorithms.lzma_codec.compress_lzma(delta_encoded_signal)
        serialized_tree = json.dumps({})  # No tree needed for LZMA
    elif mode == 'lz4':
        encoded_bytes = algorithms.external_algorithms.lz4_codec.compress_lz4(signal)
        serialized_tree = json.dumps({})  # No tree needed for LZMA
    elif mode == 'delta_lz4':
        delta_encoded_signal = algorithms.predictive_coding.delta.apply_delta_encoding(signal)
        encoded_bytes = algorithms.external_algorithms.lz4_codec.compress_lz4(delta_encoded_signal)
        serialized_tree = json.dumps({})  # No tree needed for LZMA
    elif mode == 'lstd_numcodec':
        encoded_bytes = algorithms.external_algorithms.lstd_numcodec.compress_lstd_numcodec(signal)
        serialized_tree = json.dumps({})  # No tree needed for LZMA
    elif mode == 'delta_lstd_numcodec':
        delta_encoded_signal = algorithms.predictive_coding.delta.apply_delta_encoding(signal)
        encoded_bytes = algorithms.external_algorithms.lstd_numcodec.compress_lstd_numcodec(delta_encoded_signal)
        serialized_tree = json.dumps({})  
    elif mode == 'bz2':
        encoded_bytes = algorithms.external_algorithms.bz2_codec.compress_bz2(signal)
        serialized_tree = json.dumps({})  
    elif mode == 'delta_bz2':
        delta_encoded_signal = algorithms.predictive_coding.delta.apply_delta_encoding(signal)
        encoded_bytes = algorithms.external_algorithms.bz2_codec.compress_bz2(delta_encoded_signal)
        serialized_tree = json.dumps({})  
    elif mode == 'wavpack':
        encoded_bytes = algorithms.audio_coding.wavpack_codec.compress_wavpack(signal)
        serialized_tree = json.dumps({}) 
    elif mode == 'delta_wavpack':
        delta_encoded_signal = algorithms.predictive_coding.delta.apply_delta_encoding(signal)
        encoded_bytes = algorithms.audio_coding.wavpack_codec.compress_wavpack(delta_encoded_signal)
        serialized_tree = json.dumps({})  
    else:
        print("Invalid mode:", mode)
        return
    
    with open(tree_file, 'w') as file:
        file.write(serialized_tree)
    
    sample_rate_bytes = sample_rate.to_bytes(4, byteorder='big')
    original_length_bytes = len(signal).to_bytes(4, byteorder='big')
    first_sample_bytes = int(signal[0]).to_bytes(2, byteorder='big', signed=True)
    compressed_data_with_metadata = sample_rate_bytes + original_length_bytes + first_sample_bytes + encoded_bytes
    
    with open(output_file, 'wb') as file:
        file.write(compressed_data_with_metadata)

def main(input_file, compressed_file, tree_file, mode):
    compress_wav_file(input_file, compressed_file, tree_file, mode)

# if __name__ == '__main__':
#     # mode = sys.argv[3]  # Now expecting mode as third argument
#     mode = 'blosc_lz4'  # Change this to 'huff' or 'delta_huff' as needed
#     input_file = sys.argv[1]
#     compressed_file = sys.argv[2]
#     tree_file = sys.argv[2] + "_tree.json"
#     main(input_file, compressed_file, tree_file, mode)


if __name__ == '__main__':
    # mode = sys.argv[3]  # Now expecting mode as third argument
    mode = "bz2"
    input_file = sys.argv[1]
    compressed_file = sys.argv[2]
    tree_file = sys.argv[2] + "_tree.json"
    main(input_file, compressed_file, tree_file, mode)

