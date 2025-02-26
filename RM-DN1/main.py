import sys
import os

def bytes_to_bits(byte_data):
    """Convert bytes to a binary string (8 bits for each byte)."""
    return ''.join(f'{byte:08b}' for byte in byte_data)

def bits_to_bytes(bit_string):
    """Convert a binary string back to bytes."""
    return bytes(int(bit_string[i:i+8], 2) for i in range(0, len(bit_string), 8))

def find_occurrences(bit_data, search_bits):
    """Find and print all non-overlapping occurrences of a bit sequence."""
    search_pos = bit_data.find(search_bits, 0)
    while search_pos != -1:
        print(search_pos, end=" ")
        search_pos = bit_data.find(search_bits, search_pos + len(search_bits))
    print()  # Newline after printing positions

def search_and_replace_bits(bit_data, search_bits, replace_bits):
    """Search for and replace all occurrences of a bit sequence."""
    return bit_data.replace(search_bits, replace_bits)

def read_binary_file(filename):
    """Read the entire binary file and return its content as bytes."""
    with open(filename, 'rb') as file:
        return file.read()

def write_binary_file(filename, data):
    """Write bytes data back into a binary file."""
    with open(filename, 'wb') as file:
        file.write(data)

if __name__ == '__main__':
    # Check if the number of arguments is correct
    if len(sys.argv) < 4:
        print("Usage: python main.py <filename> <option> <data1> [<data2>]")
        sys.exit(1)

    # Get filename and options from arguments
    filename = sys.argv[1]
    option = sys.argv[2]
    data1 = sys.argv[3]
    data2 = sys.argv[4] if len(sys.argv) == 5 else None

    # Ensure file exists
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    # Read the binary file
    byte_data = read_binary_file(filename)

    # Convert byte data to bit string
    bit_data = bytes_to_bits(byte_data)
    #bit_data = "01000001010000100100001101000100"

    # Handle different options
    if option == "f":
        # Find only, print all occurrences
        find_occurrences(bit_data, data1)

    elif option == "fr":
        if not data2:
            print("Error: 'fr' option requires both <data1> and <data2>.")
            sys.exit(1)

        # Search and replace bit sequences
        modified_bit_data = search_and_replace_bits(bit_data, data1, data2)

        # Convert back to bytes
        new_byte_data = bits_to_bytes(modified_bit_data)

        # Write the result to a new file
        output_filename = "output." + filename.split(".")[-1]
        write_binary_file(output_filename, new_byte_data)
        print(f"Modified file written to '{output_filename}'")
        #print(modified_bit_data)

    else:
        print(f"Error: Invalid option '{option}'. Valid options are 'f' or 'fr'.")
        sys.exit(1)
