import argparse
from PIL import Image
import numpy as np
import zlib
import pickle

# Define the constants
sqrt_8_64 = np.sqrt(8 / 64)
sqrt_2_4 = np.sqrt(2 / 4)

# Define the matrix H
H = np.array([
    [sqrt_8_64, sqrt_8_64, 1 / 2, 0, sqrt_2_4, 0, 0, 0],
    [sqrt_8_64, sqrt_8_64, 1 / 2, 0, -sqrt_2_4, 0, 0, 0],
    [sqrt_8_64, sqrt_8_64, -1 / 2, 0, 0, sqrt_2_4, 0, 0],
    [sqrt_8_64, sqrt_8_64, -1 / 2, 0, 0, -sqrt_2_4, 0, 0],
    [sqrt_8_64, -sqrt_8_64, 0, 1 / 2, 0, 0, -sqrt_2_4, 0],
    [sqrt_8_64, -sqrt_8_64, 0, 1 / 2, 0, 0, -sqrt_2_4, 0],
    [sqrt_8_64, -sqrt_8_64, 0, -1 / 2, 0, 0, 0, sqrt_2_4],
    [sqrt_8_64, -sqrt_8_64, 0, -1 / 2, 0, 0, 0, -sqrt_2_4]
])

# Transpose of H
H_transposed = H.T

def cik_cak(matrix):
    rows, cols = matrix.shape
    # result = np.empty(rows * cols, dtype=matrix.dtype)
    result = np.empty(rows * cols, dtype=np.float32)
    index = 0

    for d in range(rows + cols - 1):
        if d % 2 == 0:
            # Even diagonals go bottom-left to top-right
            r = d if d < rows else rows - 1
            c = 0 if d < rows else d - (rows - 1)
            while r >= 0 and c < cols:
                result[index] = matrix[r, c]
                r -= 1
                c += 1
                index += 1
        else:
            # Odd diagonals go top-right to bottom-left
            c = d if d < cols else cols - 1
            r = 0 if d < cols else d - (cols - 1)
            while c >= 0 and r < rows:
                result[index] = matrix[r, c]
                r += 1
                c -= 1
                index += 1
    return result


def inverse_cik_cak(arr, rows, cols):
    matrix = np.zeros((rows, cols), dtype=arr.dtype)
    index = 0

    for d in range(rows + cols - 1):
        if d % 2 == 0:
            # Even diagonals go bottom-left to top-right
            r = d if d < rows else rows - 1
            c = 0 if d < rows else d - (rows - 1)
            while r >= 0 and c < cols:
                matrix[r, c] = arr[index]
                r -= 1
                c += 1
                index += 1
        else:
            # Odd diagonals go top-right to bottom-left
            c = d if d < cols else cols - 1
            r = 0 if d < cols else d - (cols - 1)
            while c >= 0 and r < rows:
                matrix[r, c] = arr[index]
                r += 1
                c -= 1
                index += 1

    return matrix


def combine_blocks(blocks, num_blocks_rows, num_blocks_cols):
    # Calculate the original matrix size
    original_height = num_blocks_rows * 8
    original_width = num_blocks_cols * 8

    # Initialize an empty matrix of the original size
    original_matrix = np.zeros((original_height, original_width), dtype=blocks[0].dtype)

    # Place each block into the correct position in the original matrix
    for i in range(num_blocks_rows):
        for j in range(num_blocks_cols):
            # Calculate the index of the block in the 1D array
            block_index = i * num_blocks_cols + j
            block = blocks[block_index]

            # Calculate the position where this block should go in the original matrix
            start_row = i * 8
            start_col = j * 8

            # Place the block in the corresponding position
            original_matrix[start_row:start_row + 8, start_col:start_col + 8] = block

    return original_matrix

def compress_file(input_file, output_file, threshold):
    with Image.open(input_file) as img:
        # Convert image to numpy array
        data = np.array(img)

    compressed, pad_rows, pad_cols, num_blocks_rows, num_blocks_cols = compress(data, threshold)

    pad_rows &= 0x0F
    pad_cols &= 0x0F
    # Combine pad_rows and pad_cols into a single byte
    combined_byte = (pad_rows << 4) | pad_cols

    # Write compressed data to file
    with open(output_file, "wb") as f:
        f.write(combined_byte.to_bytes(1, byteorder='big'))
        f.write(num_blocks_rows.to_bytes(2, byteorder='big'))
        f.write(num_blocks_cols.to_bytes(2, byteorder='big'))

        f.write(compressed)

def compress(data, threshold):
    # print(input_file, output_file, threshold)

    rows, cols = data.shape
    # Calculate the necessary padding
    pad_rows = (8 - rows % 8) if rows % 8 != 0 else 0
    pad_cols = (8 - cols % 8) if cols % 8 != 0 else 0

    expanded_matrix = np.pad(
        data,
        ((0, pad_rows), (0, pad_cols)),
        mode='constant',
        constant_values=0
    )

    # get blocks of 8x8 matrixes from the image
    blocks = [
        expanded_matrix[i:i + 8, j:j + 8]
        for i in range(0, expanded_matrix.shape[0], 8)
        for j in range(0, expanded_matrix.shape[1], 8)
    ]

    # Number of blocks in the rows direction
    num_blocks_rows = expanded_matrix.shape[0] // 8
    # Number of blocks in the columns direction
    num_blocks_cols = expanded_matrix.shape[1] // 8

    # print(pad_cols, pad_rows)

    # print("Rows:", num_blocks_rows)
    # print("Cols:", num_blocks_cols)
    # print("Expected Blocks Len", num_blocks_rows * num_blocks_cols)
    # print("Blocks Len", len(blocks))
    # print("Split Blocks:\n", blocks[2])

    blocks = [H_transposed @ block @ H for block in blocks]

    # print("Matrix Multiplication:\n", blocks[2])

    arrays = []
    for i in range(len(blocks)):
        arrays.append(cik_cak(blocks[i]))

    # print("Cik-Cak:\n", arrays[2])

    # arrays[arrays < threshold] = 0
    for i in range(len(arrays)):
        arrays[i][arrays[i] < threshold] = 0

    # print("Kvantizacija:\n", arrays[2])

    serialized = pickle.dumps(arrays)

    # Compress with zlib
    compressed = zlib.compress(serialized)

    return compressed, pad_rows, pad_cols, num_blocks_rows, num_blocks_cols

def decompress_file(input_file, output_file):
    with open(input_file, "rb") as f:
        combined_byte = int.from_bytes(f.read(1), byteorder='big')
        pad_rows = (combined_byte >> 4) & 0x0F
        pad_cols = combined_byte & 0x0F
        num_blocks_rows = int.from_bytes(f.read(2), byteorder='big')
        num_blocks_cols = int.from_bytes(f.read(2), byteorder='big')
        compressed = f.read()

    # Decompress
    arrays = pickle.loads(zlib.decompress(compressed))

    expanded_matrix = decompress(arrays, num_blocks_rows, num_blocks_cols, pad_rows, pad_cols)

    # Save the image
    img = Image.fromarray(expanded_matrix)
    img.save(output_file)

    return expanded_matrix


def decompress(arrays, num_blocks_rows, num_blocks_cols, pad_rows, pad_cols):
    # print(arrays[2])

    blocks = [inverse_cik_cak(arr, 8, 8) for arr in arrays]

    blocks = [H @ block @ H_transposed for block in blocks]

    expanded_matrix = combine_blocks(np.array(blocks), num_blocks_rows, num_blocks_cols)

    # Remove padding
    expanded_matrix = expanded_matrix[:(num_blocks_rows*8)-pad_rows, :(num_blocks_cols*8)-pad_cols]
    expanded_matrix = expanded_matrix.round().astype(np.uint8)
    # print(expanded_matrix.shape)
    # print(expanded_matrix)

    return expanded_matrix

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Kompresija ali dekompresija datotek.")
    parser.add_argument('operacija', choices=['c', 'd'], help="Izberite 'c' za kompresijo ali 'd' za dekompresijo.")
    parser.add_argument('vhodna_datoteka', help="Pot do vhodne datoteke.")
    parser.add_argument('izhodna_datoteka', help="Pot do izhodne datoteke.")
    parser.add_argument('threshold', type=int, nargs='?', help="Prag za kompresijo (neobvezno).")

    args = parser.parse_args()

    if args.operacija == 'c':
        if not args.threshold:
            args.threshold = 0

        compress_file(args.vhodna_datoteka, args.izhodna_datoteka, args.threshold)

    elif args.operacija == 'd':
        decompress_file(args.vhodna_datoteka, args.izhodna_datoteka)
