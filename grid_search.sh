#!/usr/bin/env bash

rm -rf data
unzip data.zip

get_file_size() {
  gfind "$1" -printf "%s\n"
}

echo "mode,total_original_size_bytes,total_compressed_size_bytes,compression_ratio,average_compression_speed_xRT,average_decompression_speed_xRT" >> compression_results.csv

total_size_raw=0
total_size_compressed=0
total_duration_seconds=0
total_compression_time=0
total_decompression_time=0

mode='bz2'

for file in data/*
do
  echo "Processing $file"
  compressed_file_path="${file}.brainwire"
  decompressed_file_path="${file}.copy"

  file_size=$(get_file_size "$file")
  
  # Use mediainfo as an alternative to ffprobe to get duration in seconds
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

echo "Compression process completed."
echo "Mode: $mode"
echo "Total Original size (bytes): $total_size_raw"
echo "Total Compressed size (bytes): $total_size_compressed"
echo "Final Compression Ratio: $final_compression_ratio"
echo "Average Compression Speed (xRT): $average_compression_speed_xRT"
echo "Average Decompression Speed (xRT): $average_decompression_speed_xRT"
