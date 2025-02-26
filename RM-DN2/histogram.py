import numpy as np
import pywt
from PIL import Image
import matplotlib.pyplot as plt
from main import hide_message, extract_message

def plot_histogram(original_img_data, decompressed_img_data):
    # Prikaz histograma pred in po kompresiji
    plt.figure(figsize=(12, 6))

    # Histogram za originalne slike
    plt.subplot(1, 2, 1)
    plt.hist(original_img_data.flatten(), bins=256, color='blue', alpha=0.7, label='Original Image')
    plt.title('Histogram Pred Kompresijo')
    plt.xlabel('Intenziteta')
    plt.ylabel('Število pikslov')

    # Histogram za dekompresirane slike
    plt.subplot(1, 2, 2)
    plt.hist(decompressed_img_data.flatten(), bins=256, color='red', alpha=0.7, label='Decompressed Image')
    plt.title('Histogram Po Dekompresiji')
    plt.xlabel('Intenziteta')
    plt.ylabel('Število pikslov')

    plt.tight_layout()
    # plt.show()

    # Save the figure to the specified output path
    plt.savefig("histogram.png")
    print(f"Histogram saved")
    plt.close()


def main():
    image_path = "slike/Baboon.bmp"  # Poti do vaše slike
    N = 20  # Prilagodite glede na vaše potrebe
    M = 3  # Prilagodite glede na vaše potrebe

    # Skrij sporočilo v sliko
    compressed_path = 'compressed.bin'  # Poti do vaše kompresirane slike
    hide_message(image_path, 'sporocilo.txt', N, M, compressed_path)

    with Image.open(image_path) as img:
        # Convert image to numpy array
        original_img_data = np.array(img)

    # Izvleči sporočilo iz slike
    decompressed_path = 'decompressed.bmp'  # Poti do vaše dekompresirane slike
    decompressed_img_data = extract_message(compressed_path, 'sporocilo_out.txt', N, M, decompressed_path)

    # Prikaz histogramov
    plot_histogram(original_img_data, decompressed_img_data)

if __name__ == "__main__":
    main()
