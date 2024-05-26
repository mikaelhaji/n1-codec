import os
from scipy.io import wavfile

def get_metadata_size(wav_path):
    """
    Reads a WAV file and returns the size of its metadata.
    Metadata considered here: sample rate, original length, and first sample.
    """
    sample_rate, signal = wavfile.read(wav_path)
    metadata = sample_rate.to_bytes(4, byteorder='big') + len(signal).to_bytes(4, byteorder='big') + int(signal[0]).to_bytes(2, byteorder='big', signed=True)
    return len(metadata)

def main(directory):
    """
    Process all WAV files in the given directory and print their metadata size.
    Check if all metadata sizes are 10 bytes and count the files.
    """
    file_count = 0
    consistent_size = True
    for filename in os.listdir(directory):
        if filename.endswith(".wav"):
            file_count += 1
            wav_path = os.path.join(directory, filename)
            metadata_size = get_metadata_size(wav_path)
            if metadata_size != 10:
                consistent_size = False
            print(f"Metadata size for {filename}: {metadata_size} bytes")

    print(f"Total WAV files processed: {file_count}")
    print("All metadata sizes are 10 bytes:" if consistent_size and file_count == 743 else "Metadata size inconsistency or file count mismatch.")

if __name__ == "__main__":
    directory = "data"
    main(directory)

