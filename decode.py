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
logging.basicConfig(filename='logs/decompression.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def decompress_wav_file(input_file, output_file, tree_file, mode):
    with open(input_file, 'rb') as file:
        compressed_data_with_metadata = file.read()
    
    sample_rate = int.from_bytes(compressed_data_with_metadata[:4], byteorder='big')
    original_length = int.from_bytes(compressed_data_with_metadata[4:8], byteorder='big')
    first_sample = int.from_bytes(compressed_data_with_metadata[8:10], byteorder='big', signed=True)
    encoded_bytes = compressed_data_with_metadata[10:]


    with open(tree_file, 'r') as file:
        serialized_tree = file.read()

    if mode == 'huff':
        canonical_codes = {int(k): v for k, v in json.loads(serialized_tree).items()}
        root = algorithms.entropy_coding.huffman.deserialize_huffman_tree(canonical_codes)
        decoded_signal = algorithms.entropy_coding.huffman.decompress_huffman(encoded_bytes, root, original_length)
    elif mode == 'delta_huff':
        canonical_codes = {int(k): v for k, v in json.loads(serialized_tree).items()}
        root = algorithms.entropy_coding.huffman.deserialize_huffman_tree(canonical_codes)
        decoded_deltas = algorithms.entropy_coding.huffman.decompress_huffman(encoded_bytes, root, original_length)
        decoded_signal = algorithms.predictive_coding.delta.apply_delta_decoding(decoded_deltas, first_sample)
    elif mode == 'zstd':
        decoded_bytes = algorithms.external_algorithms.zstd.decompress_zstd(encoded_bytes)
        decoded_signal = np.frombuffer(decoded_bytes, dtype=np.int16)
    elif mode == 'delta_zstd':
        decoded_bytes = algorithms.external_algorithms.zstd.decompress_zstd(encoded_bytes)
        decoded_deltas = np.frombuffer(decoded_bytes, dtype=np.int16)
        decoded_signal = algorithms.predictive_coding.delta.apply_delta_decoding(decoded_deltas, first_sample)
    elif mode == 'blosc_zstd':
        decoded_signal = algorithms.blosc_algorithms.blosc_zstd.decompress_blosc_zstd(encoded_bytes)
    elif mode == 'delta_blosc_zstd':
        decoded_bytes = algorithms.blosc_algorithms.blosc_zstd.decompress_blosc_zstd(encoded_bytes)
        decoded_signal = algorithms.predictive_coding.delta.apply_delta_decoding(decoded_bytes, first_sample)
    elif mode == 'blosc_lz4':
        decoded_signal = algorithms.blosc_algorithms.blosc_lz4.decompress_blosc_lz4(encoded_bytes)
    elif mode == 'delta_blosc_lz4':
        decoded_bytes = algorithms.blosc_algorithms.blosc_lz4.decompress_blosc_lz4(encoded_bytes)
        decoded_signal = algorithms.predictive_coding.delta.apply_delta_decoding(decoded_bytes, first_sample)
    elif mode == 'blosc_lz4hc':
        decoded_signal = algorithms.blosc_algorithms.blosc_lz4hc.decompress_blosc_lz4hc(encoded_bytes)
    elif mode == 'delta_blosc_lz4hc':
        decoded_bytes = algorithms.blosc_algorithms.blosc_lz4hc.decompress_blosc_lz4hc(encoded_bytes)
        decoded_signal = algorithms.predictive_coding.delta.apply_delta_decoding(decoded_bytes, first_sample)
    elif mode == 'blosc_zlib':
        decoded_signal = algorithms.blosc_algorithms.blosc_zlib.decompress_blosc_zlib(encoded_bytes)
    elif mode == 'delta_blosc_zlib':
        decoded_bytes = algorithms.blosc_algorithms.blosc_zlib.decompress_blosc_zlib(encoded_bytes)
        decoded_signal = algorithms.predictive_coding.delta.apply_delta_decoding(decoded_bytes, first_sample)
    elif mode == 'gzip':
        decoded_signal = algorithms.external_algorithms.gzip_codec.decompress_gzip(encoded_bytes)
    elif mode == 'delta_gzip':
        decoded_bytes = algorithms.external_algorithms.gzip_codec.decompress_gzip(encoded_bytes)
        decoded_signal = algorithms.predictive_coding.delta.apply_delta_decoding(decoded_bytes, first_sample)
    elif mode == 'lzma':
        decoded_signal = algorithms.external_algorithms.lzma_codec.decompress_lzma(encoded_bytes)
    elif mode == 'delta_lzma':
        decoded_bytes = algorithms.external_algorithms.lzma_codec.decompress_lzma(encoded_bytes)
        decoded_signal = algorithms.predictive_coding.delta.apply_delta_decoding(decoded_bytes, first_sample)
    elif mode == 'lz4':
        decoded_signal = algorithms.external_algorithms.lz4_codec.decompress_lz4(encoded_bytes)
    elif mode == 'delta_lz4':
        decoded_bytes = algorithms.external_algorithms.lz4_codec.decompress_lz4(encoded_bytes)
        decoded_signal = algorithms.predictive_coding.delta.apply_delta_decoding(decoded_bytes, first_sample)
    elif mode == 'lstd_numcodec':
        decoded_signal = algorithms.external_algorithms.lstd_numcodec.decompress_lstd_numcodec(encoded_bytes)
    elif mode == 'delta_lstd_numcodec':
        decoded_bytes = algorithms.external_algorithms.lstd_numcodec.decompress_lstd_numcodec(encoded_bytes)
        decoded_signal = algorithms.predictive_coding.delta.apply_delta_decoding(decoded_bytes, first_sample)
    elif mode == 'bz2':
        decoded_signal = algorithms.external_algorithms.bz2_codec.decompress_bz2(encoded_bytes)
    elif mode == 'delta_bz2':
        decoded_bytes = algorithms.external_algorithms.bz2_codec.decompress_bz2(encoded_bytes)
        decoded_signal = algorithms.predictive_coding.delta.apply_delta_decoding(decoded_bytes, first_sample)
    elif mode == 'wavpack':
        decoded_signal = algorithms.audio_coding.wavpack_codec.decompress_wavpack(encoded_bytes)
    elif mode == 'delta_wavpack':
        decoded_bytes = algorithms.audio_coding.wavpack_codec.decompress_wavpack(encoded_bytes)
        decoded_signal = algorithms.predictive_coding.delta.apply_delta_decoding(decoded_bytes, first_sample)

    # Print first 10 samples of the decoded signal
    # print("Post-decompression signal samples (first 10):", decoded_signal[:10])
    logging.debug("Post-decompression signal samples (all): %s", decoded_signal)  # Log all samples of the signal

    wavfile.write(output_file, sample_rate, np.array(decoded_signal, dtype=np.int16))

def main(compressed_file, decompressed_file, tree_file, mode):
    decompress_wav_file(compressed_file, decompressed_file, tree_file, mode)

if __name__ == '__main__':
    mode = sys.argv[3]
    # mode = "blosc_lz4" 
    compressed_file = sys.argv[1]
    decompressed_file = sys.argv[2]
    tree_file = sys.argv[1] + "_tree.json"
    main(compressed_file, decompressed_file, tree_file, mode)