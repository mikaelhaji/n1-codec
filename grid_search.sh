#!/usr/bin/env bash

rm -rf data
unzip data.zip

get_file_size() {
  gfind "$1" -printf "%s\n"
}

echo "mode,total_original_size_bytes,total_compressed_size_bytes,compression_ratio,average_compression_speed_xRT,average_decompression_speed_xRT" >> "$PWD/tests/compression_results.csv"

total_size_raw=0
total_size_compressed=0
total_duration_seconds=0
total_compression_time=0
total_decompression_time=0

# Define all modes from encode.py
modes=('huff' 'delta_huff' 'zstd' 'delta_zstd' 'blosc_zstd' 'delta_blosc_zstd' 'blosc_lz4' 'delta_blosc_lz4' 'blosc_lz4hc' 'delta_blosc_lz4hc' 'blosc_zlib' 'delta_blosc_zlib' 'gzip' 'delta_gzip' 'lzma' 'delta_lzma' 'lz4' 'delta_lz4' 'lstd_numcodec' 'delta_lstd_numcodec' 'bz2' 'delta_bz2' 'wavpack' 'delta_wavpack')

for mode in "${modes[@]}"
do
  echo "Testing mode: $mode"
  for file in data/*
  do
    echo "Processing $file"
    compressed_file_path="${file}.brainwire"
    decompressed_file_path="${file}.copy"

    file_size=$(get_file_size "$file")
    
    # Use mediainfo to get duration in seconds
    duration_seconds=$(mediainfo --Inform="General;%Duration%" "$file" | awk '{print $1/1000}')

    # Measure compression time
    start_time=$(date +%s.%N)
    ./encode "$file" "$compressed_file_path" "$mode"
    end_time=$(date +%s.%N)
    compression_time=$(echo "$end_time - $start_time" | bc)

    # Measure decompression time
    start_time=$(date +%s.%N)
    ./decode "$compressed_file_path" "$decompressed_file_path" "$mode"
    end_time=$(date +%s.%N)
    decompression_time=$(echo "$end_time - $start_time" | bc)

    compressed_size=$(get_file_size "$compressed_file_path")

    if diff -q "$file" "$decompressed_file_path" > /dev/null; then
        echo "${file} losslessly compressed from ${file_size} bytes to ${compressed_size} bytes"
    else
        echo "ERROR: ${file} and ${decompressed_file_path} are different."
        exit 1
    fi

    total_size_raw=$((total_size_raw + file_size))
    total_size_compressed=$((total_size_compressed + compressed_size))
    total_duration_seconds=$(echo "$total_duration_seconds + $duration_seconds" | bc)
    total_compression_time=$(echo "$total_compression_time + $compression_time" | bc)
    total_decompression_time=$(echo "$total_decompression_time + $decompression_time" | bc)
  done

  final_compression_ratio=$(echo "scale=2; $total_size_raw / $total_size_compressed" | bc)
  average_compression_speed_xRT=$(echo "scale=2; $total_compression_time / $total_duration_seconds" | bc)
  average_decompression_speed_xRT=$(echo "scale=2; $total_decompression_time / 10" | bc) # Assuming all files together represent 10s of audio

  echo "$mode,$total_size_raw,$total_size_compressed,$final_compression_ratio,$average_compression_speed_xRT,$average_decompression_speed_xRT" >> compression_results.csv

  # Reset totals for the next mode
  total_size_raw=0
  total_size_compressed=0
  total_duration_seconds=0
  total_compression_time=0
  total_decompression_time=0
done

echo "Compression process completed."