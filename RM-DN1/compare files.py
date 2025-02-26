def compare_binary_files(file1_path, file2_path):
    with open(file1_path, 'rb') as file1, open(file2_path, 'rb') as file2:
        # Compare files in chunks to avoid loading the entire file into memory
        chunk_size = 4096  # Adjust the chunk size if needed

        while True:
            # Read chunks from both files
            chunk1 = file1.read(chunk_size)
            chunk2 = file2.read(chunk_size)

            # If the chunks differ, files are not the same
            if chunk1 != chunk2:
                return False

            # If both chunks are empty, we've reached the end of both files
            if not chunk1:
                return True


# Example usage
file1_path = 'file1.bin'
file2_path = 'file2.bin'

if compare_binary_files(file1_path, file2_path):
    print("The files are identical.")
else:
    print("The files are different.")
