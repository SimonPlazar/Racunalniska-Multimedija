import os
from main import *


def GetPSNR(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    if mse == 0:
        return 100
    max_pixel = 255.0
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    return psnr


# Shannonova entropija med originalno in kompresirano sliko
def GetShannonovaEntropija(image):
    # Find the frequency of each pixel value
    histogram = np.bincount(image.flatten(), minlength=256)
    # Normalize the histogram
    histogram = histogram / np.sum(histogram)
    # Calculate the Shannon entropy
    entropy = -np.sum([p * np.log2(p) for p in histogram if p > 0])
    return entropy


def GetBlokovnost(image):
    image = image.astype(np.int32)
    M, N = image.shape
    B = 0

    # Prvi del formule (vertikalne razlike med zaporednimi vrsticami)
    for i in range(0, M - 8, 8):
        for j in range(N):
            B += abs(image[i, j] - image[i + 8, j])

    # Drugi del formule (horizontalne razlike med zaporednimi stolpci)
    for j in range(0, N - 8, 8):
        for i in range(M):
            B += abs(image[i, j] - image[i, j + 8])

    return B


if __name__ == '__main__':
    # Define the threshold values
    N = [1, 20, 40]
    M = [1, 3, 5]

    # Path for input and output folders
    input_folder = "slike"
    output_folder = "Data"

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get the first 10 images in the "slike" folder
    image_files = sorted([f for f in os.listdir(input_folder) if f.endswith(('.bmp'))])[:2]
    message_files = sorted([f for f in os.listdir(input_folder) if f.endswith(('.txt'))])[:2]


    # Loop through the images
    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        for message_file in message_files:
            message_path = os.path.join(input_folder, message_file)

            # Loop through the threshold values
            for n in N:
                for m in M:
                    # Create output filenames
                    compressed_filename = f"{os.path.splitext(image_file)[0]}_{os.path.splitext(message_file)[0]}_compressed_N{n}_M{m}.bin"
                    decompressed_filename = f"{os.path.splitext(image_file)[0]}_{os.path.splitext(message_file)[0]}_decompressed_N{n}_M{m}.bmp"
                    extracted_message_filename = f"{os.path.splitext(image_file)[0]}_{os.path.splitext(message_file)[0]}_extracted_N{n}_M{m}.txt"

                    # Save the compressed and decompressed images to the Data folder
                    compressed_path = os.path.join(output_folder, compressed_filename)
                    decompressed_path = os.path.join(output_folder, decompressed_filename)
                    extracted_message_path = os.path.join(output_folder, extracted_message_filename)

                    hide_message(image_path, message_path, n, m, compressed_path)
                    with Image.open(image_path) as img:
                        # Convert image to numpy array
                        OriginalImg = np.array(img)
                    AlteredImg = extract_message(compressed_path, extracted_message_path, n, m, decompressed_path)

                    # Get compression ratio
                    original_size = os.path.getsize(image_path)
                    compressed_size = os.path.getsize(compressed_path)
                    compression_ratio = original_size / compressed_size
                    compression_ratio = round(compression_ratio, 2)

                    # Calculate the PSNR
                    psnr = GetPSNR(OriginalImg, AlteredImg)
                    psnr = round(psnr, 2)
                    # Calculate the Shannon entropy
                    entropyOriginal = GetShannonovaEntropija(OriginalImg)
                    entropyOriginal = round(entropyOriginal, 2)
                    entropyAltered = GetShannonovaEntropija(AlteredImg)
                    entropyAltered = round(entropyAltered, 2)
                    # Calculate the blockiness
                    blockinessOriginal = GetBlokovnost(OriginalImg)
                    blockinessOriginal = round(blockinessOriginal, 2)
                    blockinessAltered = GetBlokovnost(AlteredImg)
                    blockinessAltered = round(blockinessAltered, 2)

                    # write data to file
                    with open('data.txt', 'a') as f:
                        f.write(
                                f"[{image_file}, {message_file}, {n}, {m}, {compression_ratio}, {psnr}, {entropyOriginal}, {entropyAltered}, {blockinessOriginal}, {blockinessAltered}],\n")

                    print(f"Processed {image_file} hidden {message_file} with N={n}, M={m}: Saved to {compressed_path} and {decompressed_path}")
