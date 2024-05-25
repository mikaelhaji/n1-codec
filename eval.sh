#!/usr/bin/env bash

rm -rf data
unzip data.zip

get_file_size() {
  gfind "$1" -printf "%s\n"
}

total_size_raw=0
encoder_size=$(get_file_size encode)
decoder_size=$(get_file_size decode)
total_size_compressed=$((encoder_size + decoder_size))

for file in data/*
do
  echo "Processing $file"
  compressed_file_path="${file}.brainwire"
  decompressed_file_path="${file}.copy"

  ./encode "$file" "$compressed_file_path"
  ./decode "$compressed_file_path" "$decompressed_file_path"

  file_size=$(get_file_size "$file")
  compressed_size=$(get_file_size "$compressed_file_path")

  if diff -q "$file" "$decompressed_file_path" > /dev/null; then
      echo "${file} losslessly compressed from ${file_size} bytes to ${compressed_size} bytes"
  else
      echo "ERROR: ${file} and ${decompressed_file_path} are different."
      exit 1
  fi

  total_size_raw=$((total_size_raw + file_size))
  total_size_compressed=$((total_size_compressed + compressed_size))
done

compression_ratio=$(echo "scale=2; ${total_size_raw} / ${total_size_compressed}" | bc)

echo "All recordings successfully compressed."
echo "Original size (bytes): ${total_size_raw}"
echo "Compressed size (bytes): ${total_size_compressed}"
echo "Compression ratio: ${compression_ratio}"
