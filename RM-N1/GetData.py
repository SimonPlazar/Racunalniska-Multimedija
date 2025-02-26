import os
import time
from main import compress_file, decompress_file

# Paths for the input and output directories
input_folder = "Testne Datoteke"
compressed_folder = "Files/compressed"
decompressed_folder = "Files/decompressed"

# Make sure the output directories exist
os.makedirs(compressed_folder, exist_ok=True)
os.makedirs(decompressed_folder, exist_ok=True)


# Function to compress all files in the input folder
def compress_all_files():
    for filename in os.listdir(input_folder):
        input_file = os.path.join(input_folder, filename)

        # Check if it's a file (ignore directories)
        if os.path.isfile(input_file):
            output_file = os.path.join(compressed_folder, f"{filename}.compressed")

            # Get original file size
            original_size = os.path.getsize(input_file)

            # Start timing compression
            start_time = time.time()

            # Compress the file
            compress_file(input_file, output_file, stevilo_bitov=32)  # Assuming 8 bits

            # End timing compression
            compression_time = time.time() - start_time

            # Get compressed file size
            compressed_size = os.path.getsize(output_file)

            # Calculate compression ratio
            compression_ratio = original_size / compressed_size if compressed_size != 0 else 0

            # Print results for the file
            print(f"Compressed {filename}:")
            print(f"  Original Size: {original_size} bytes")
            print(f"  Compressed Size: {compressed_size} bytes")
            print(f"  Compression Ratio: {compression_ratio:.2f}")
            print(f"  Time taken: {compression_time:.4f} seconds\n")


# Function to decompress all files in the compressed folder
def decompress_all_files():
    for filename in os.listdir(compressed_folder):
        input_file = os.path.join(compressed_folder, filename)

        # Check if it's a file (ignore directories)
        if os.path.isfile(input_file):
            # Remove the ".compressed" extension from the filename
            original_filename = filename.replace(".compressed", "")
            output_file = os.path.join(decompressed_folder, original_filename)

            # Start timing decompression
            start_time = time.time()

            # Decompress the file
            decompress_file(input_file, output_file)

            # End timing decompression
            decompression_time = time.time() - start_time

            # Print decompression time for the file
            print(f"Decompressed {filename}:")
            print(f"  Time taken: {decompression_time:.4f} seconds\n")


if __name__ == "__main__":
    print("Starting compression process...\n")
    compress_all_files()

    print("\nStarting decompression process...\n")
    decompress_all_files()
