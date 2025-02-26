import argparse
import pickle
import zlib
import random
from PIL import Image
import numpy as np
import pywt


def cik_cak(matrix):
    rows, cols = matrix.shape
    result = np.empty(rows * cols, dtype=matrix.dtype)
    # result = np.empty(rows * cols, dtype=np.float32)
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

    original_matrix = np.zeros((original_height, original_width), dtype=blocks[0].dtype)

    for i in range(num_blocks_rows):
        for j in range(num_blocks_cols):
            # Calculate the index of the block in the 1D array
            block_index = i * num_blocks_cols + j
            block = blocks[block_index]

            start_row = i * 8
            start_col = j * 8

            original_matrix[start_row:start_row + 8, start_col:start_col + 8] = block

    return original_matrix


def embed_message(arrays, message_bytes, N, M):
    binary_message = ''.join(f'{byte:08b}' for byte in message_bytes)
    message_index = 0

    random.seed(N * M)

    used_blocks = set()
    for block_index, array in enumerate(arrays):
        if message_index >= len(binary_message):
            break  # Stop if the entire message is embedded

        if block_index in used_blocks:
            continue
        used_blocks.add(block_index)

        # Define range of coefficients
        start_index = 4
        end_index = min(32, 64 - N)
        coefficients = list(range(start_index, end_index))

        triplets = []
        count = 0
        while len(triplets) < M:
            start = random.choice(coefficients[:-2])  # Pick a start index, ensuring space for three consecutive numbers
            triplet = [start, start + 1, start + 2]
            if all(not set(triplet).intersection(set(t)) for t in triplets):
                triplets.append(triplet)
            else:
                count += 1
                if count > 1000:
                    break

        # Embed binary message in the selected block
        for triplet in triplets:
            if message_index >= len(binary_message) - 1:
                break

            AC1_idx, AC2_idx, AC3_idx = triplet
            C1, C2, C3 = array[AC1_idx] % 2, array[AC2_idx] % 2, array[AC3_idx] % 2

            x1 = int(binary_message[message_index])
            x2 = int(binary_message[message_index + 1])
            message_index += 2

            if x1 == (C1 ^ C2) and x2 == (C2 ^ C3):
                continue  # No change
            elif x1 != (C1 ^ C2) and x2 == (C2 ^ C3):
                array[AC1_idx] ^= 1  # Negate LSB of AC1
            elif x1 == (C1 ^ C2) and x2 != (C2 ^ C3):
                array[AC3_idx] ^= 1  # Negate LSB of AC3
            elif x1 != (C1 ^ C2) and x2 != (C2 ^ C3):
                array[AC2_idx] ^= 1  # Negate LSB of AC2

    return arrays


def retrieve_message(arrays, N, M):
    extracted_bits = []
    message_length = None
    total_bits_to_extract = 4 * 8  # 4 bytes = 32 bits

    random.seed(N * M)

    used_blocks = set()
    for block_index, array in enumerate(arrays):
        if block_index in used_blocks:
            continue
        used_blocks.add(block_index)

        # Define range of coefficients
        start_index = 4
        end_index = min(32, 64 - N)
        coefficients = list(range(start_index, end_index))

        triplets = []
        count = 0
        while len(triplets) < M:
            start = random.choice(coefficients[:-2])
            triplet = [start, start + 1, start + 2]
            if all(not set(triplet).intersection(set(t)) for t in triplets):
                triplets.append(triplet)
            else:
                count += 1
                if count > 1000:
                    break

        # Extract binary message from the selected block
        for triplet in triplets:
            if total_bits_to_extract and len(extracted_bits) >= total_bits_to_extract:
                break

            AC1_idx, AC2_idx, AC3_idx = triplet
            C1, C2, C3 = array[AC1_idx] % 2, array[AC2_idx] % 2, array[AC3_idx] % 2

            x1 = C1 ^ C2
            x2 = C2 ^ C3

            extracted_bits.append(x1)
            extracted_bits.append(x2)

            # Check if the first 4 bytes have been read
            if message_length is None and len(extracted_bits) >= 32:
                # Convert first 4 bytes to message length
                length_bytes = bytearray()
                for i in range(0, 32, 8):
                    byte = 0
                    for bit_index in range(8):
                        byte = (byte << 1) | extracted_bits[i + bit_index]
                    length_bytes.append(byte)
                message_length = int.from_bytes(length_bytes, byteorder='big')
                total_bits_to_extract = 32 + message_length * 8  # Update total bits to extract (length + message)

        if total_bits_to_extract and len(extracted_bits) >= total_bits_to_extract:
            break

    extracted_bytes = bytearray()
    for i in range(0, len(extracted_bits), 8):
        byte = 0
        for bit_index in range(8):
            if i + bit_index < len(extracted_bits):
                byte = (byte << 1) | extracted_bits[i + bit_index]
        extracted_bytes.append(byte)

    if message_length is None:
        raise ValueError("Message length could not be determined.")
    actual_message_bytes = extracted_bytes[4:4 + message_length]

    # Decode and return the message
    return actual_message_bytes.decode('utf-8')


def hide_message(image_path, message_path, N, M, output_path="Compressed.bin"):
    with open(message_path, 'r', encoding='utf-8') as file:
        content = file.read()  # Preberi vsebino datoteke
    text_length = len(content)
    length_bytes = text_length.to_bytes(4, byteorder='big')
    message_bytes = length_bytes + content.encode('utf-8')
    # print(message_bytes)

    with Image.open(image_path) as img:
        data = np.array(img)

    rows, cols = data.shape
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

    num_blocks_rows = expanded_matrix.shape[0] // 8
    num_blocks_cols = expanded_matrix.shape[1] // 8

    # Izvedi 2D Haarovo transformacijo
    # blocks = [pywt.dwt2(block, 'haar') for block in blocks]
    for i in range(len(blocks)):
        LL, (LH, HL, HH) = pywt.dwt2(blocks[i], 'haar')
        blocks[i] = np.vstack((
            np.hstack((LL, LH)),
            np.hstack((HL, HH))
        ))

    # print(blocks[0])

    arrays = [cik_cak(block) for block in blocks]

    # print(arrays[0])

    for i in range(len(arrays)):
        for j in range((len(arrays[i])) - N, len(arrays[i])):
            arrays[i][j] = 0

    arrays = [np.round(array).astype(np.uint8) for array in arrays]

    # print(arrays[0])

    # F5 steganografija
    arrays = embed_message(arrays, message_bytes, N, M)

    # print(arrays[0])

    serialized = pickle.dumps(arrays)
    # Compress with zlib
    compressed = zlib.compress(serialized)

    pad_rows &= 0x0F
    pad_cols &= 0x0F
    combined_byte = (pad_rows << 4) | pad_cols

    # Write compressed data to file
    with open(output_path, "wb") as f:
        f.write(combined_byte.to_bytes(1, byteorder='big'))
        f.write(num_blocks_rows.to_bytes(2, byteorder='big'))
        f.write(num_blocks_cols.to_bytes(2, byteorder='big'))

        f.write(compressed)


def extract_message(image_path, message_path, N, M, output_path="Decompressed.bmp"):
    with open(image_path, "rb") as f:
        combined_byte = int.from_bytes(f.read(1), byteorder='big')
        pad_rows = (combined_byte >> 4) & 0x0F
        pad_cols = combined_byte & 0x0F
        num_blocks_rows = int.from_bytes(f.read(2), byteorder='big')
        num_blocks_cols = int.from_bytes(f.read(2), byteorder='big')
        compressed = f.read()

    # Decompress
    arrays = pickle.loads(zlib.decompress(compressed))
    arrays = [np.array(array, dtype=np.int8) for array in arrays]

    # reverse f5 steganografija
    try:
        message_string = retrieve_message(arrays, N, M)
    except ValueError:
        pass
    if message_string is None:
        message_string = "Sporocilo ni bilo najdeno."

    blocks = [inverse_cik_cak(arr, 8, 8) for arr in arrays]

    for i in range(len(blocks)):
        LL = blocks[i][:4, :4]
        HH = blocks[i][4:, 4:]

        LH = blocks[i][:4, 4:]
        HL = blocks[i][4:, :4]
        # LH = blocks[i][4:8, :4]
        # HL = blocks[i][:4, 4:8]

        blocks[i] = pywt.idwt2((LL, (LH, HL, HH)), 'haar')
        # for j in range(len(blocks[i])):
        #     blocks[i][j] = (blocks[i][j] + 120) % 256

        blocks[i] = [(element + 120) % 256 for element in blocks[i]]


    expanded_matrix = combine_blocks(np.array(blocks), num_blocks_rows, num_blocks_cols)
    expanded_matrix = expanded_matrix[:(num_blocks_rows * 8) - pad_rows, :(num_blocks_cols * 8) - pad_cols]
    expanded_matrix = expanded_matrix.round().astype(np.uint8)

    # Save the image
    img = Image.fromarray(expanded_matrix)
    img.save(output_path)

    with open(message_path, 'w', encoding='utf-8') as file:
        file.write(message_string)

    return expanded_matrix


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Skrivanje ali ekstrakcija sporocila.")
    parser.add_argument('vhodna_datoteka', help="Pot do poljubne slike.")
    parser.add_argument('operacija', choices=['h', 'e'],
                        help="Izberite 'h' za skrivanje sporocila ali 'e' za ekstrakcijo sporocila.")
    parser.add_argument('vhodno_izhodno_sporocilo', help="Pot do vhodnega/izhodnega tekstovnega sporočila.")
    parser.add_argument('N', type=int, help="Prag pri kompresiji.")
    parser.add_argument('M', type=int,
                        help="Stevilo unikatnih mnozic trojic koeficientov, ki se uporabijo v F5 steganografiji.")

    args = parser.parse_args()

    if args.operacija == 'h':
        hide_message(args.vhodna_datoteka, args.vhodno_izhodno_sporocilo, args.N, args.M)


    elif args.operacija == 'e':
        extract_message(args.vhodna_datoteka, args.vhodno_izhodno_sporocilo, args.N, args.M)
