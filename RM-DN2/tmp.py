from fpdf import FPDF

# Data for the table
header = ["image_file", "message_file", "n", "m", "compression_ratio", "psnr", "entropyOriginal", "entropyAltered",
          "blockinessOriginal", "blockinessAltered"]
data = [
    ["Baboon.bmp", "sporocilo1.txt", 1, 1, 1.13, 30.11, 7.36, 7.16, 1895635, 2189631],
    ["Baboon.bmp", "sporocilo1.txt", 1, 3, 1.13, 30.11, 7.36, 7.16, 1895635, 2189633],
    ["Baboon.bmp", "sporocilo1.txt", 1, 5, 1.13, 30.11, 7.36, 7.16, 1895635, 2189630],
    ["Baboon.bmp", "sporocilo1.txt", 20, 1, 1.52, 29.55, 7.36, 7.02, 1895635, 2151749],
    ["Baboon.bmp", "sporocilo1.txt", 20, 3, 1.52, 29.55, 7.36, 7.02, 1895635, 2151743],
    ["Baboon.bmp", "sporocilo1.txt", 20, 5, 1.52, 29.55, 7.36, 7.02, 1895635, 2151746],
    ["Baboon.bmp", "sporocilo1.txt", 40, 1, 2.55, 29.08, 7.36, 6.77, 1895635, 2015838],
    ["Baboon.bmp", "sporocilo1.txt", 40, 3, 2.55, 29.08, 7.36, 6.77, 1895635, 2015848],
    ["Baboon.bmp", "sporocilo1.txt", 40, 5, 2.55, 29.08, 7.36, 6.77, 1895635, 2015844],
    ["Baboon.bmp", "sporocilo2.txt", 1, 1, 1.13, 30.11, 7.36, 7.16, 1895635, 2189646],
    ["Baboon.bmp", "sporocilo2.txt", 1, 3, 1.13, 30.11, 7.36, 7.16, 1895635, 2189649],
    ["Baboon.bmp", "sporocilo2.txt", 1, 5, 1.13, 30.11, 7.36, 7.16, 1895635, 2189627],
    ["Baboon.bmp", "sporocilo2.txt", 20, 1, 1.52, 29.55, 7.36, 7.02, 1895635, 2151748],
    ["Baboon.bmp", "sporocilo2.txt", 20, 3, 1.52, 29.55, 7.36, 7.02, 1895635, 2151745],
    ["Baboon.bmp", "sporocilo2.txt", 20, 5, 1.52, 29.55, 7.36, 7.02, 1895635, 2151732],
    ["Baboon.bmp", "sporocilo2.txt", 40, 1, 2.55, 29.08, 7.36, 6.77, 1895635, 2015895],
    ["Baboon.bmp", "sporocilo2.txt", 40, 3, 2.55, 29.08, 7.36, 6.77, 1895635, 2015834],
    ["Baboon.bmp", "sporocilo2.txt", 40, 5, 2.55, 29.08, 7.36, 6.77, 1895635, 2015834],
    ["Balloons.bmp", "sporocilo1.txt", 1, 1, 1.48, 30.14, 7.35, 6.92, 1018612, 1496227],
    ["Balloons.bmp", "sporocilo1.txt", 1, 3, 1.48, 30.14, 7.35, 6.92, 1018612, 1496230],
    ["Balloons.bmp", "sporocilo1.txt", 1, 5, 1.48, 30.14, 7.35, 6.92, 1018612, 1496235],
    ["Balloons.bmp", "sporocilo1.txt", 20, 1, 1.83, 30.07, 7.35, 6.82, 1018612, 1493550],
    ["Balloons.bmp", "sporocilo1.txt", 20, 3, 1.83, 30.07, 7.35, 6.82, 1018612, 1493550],
    ["Balloons.bmp", "sporocilo1.txt", 20, 5, 1.83, 30.07, 7.35, 6.82, 1018612, 1493545],
    ["Balloons.bmp", "sporocilo1.txt", 40, 1, 2.79, 29.79, 7.35, 6.68, 1018612, 1482827],
    ["Balloons.bmp", "sporocilo1.txt", 40, 3, 2.79, 29.79, 7.35, 6.68, 1018612, 1482823],
    ["Balloons.bmp", "sporocilo1.txt", 40, 5, 2.79, 29.79, 7.35, 6.68, 1018612, 1482823],
    ["Balloons.bmp", "sporocilo2.txt", 1, 1, 1.48, 30.14, 7.35, 6.92, 1018612, 1496250],
    ["Balloons.bmp", "sporocilo2.txt", 1, 3, 1.48, 30.14, 7.35, 6.92, 1018612, 1496228],
    ["Balloons.bmp", "sporocilo2.txt", 1, 5, 1.48, 30.14, 7.35, 6.92, 1018612, 1496245],
    ["Balloons.bmp", "sporocilo2.txt", 20, 1, 1.83, 30.07, 7.35, 6.82, 1018612, 1493568],
    ["Balloons.bmp", "sporocilo2.txt", 20, 3, 1.83, 30.07, 7.35, 6.82, 1018612, 1493541],
    ["Balloons.bmp", "sporocilo2.txt", 20, 5, 1.83, 30.07, 7.35, 6.82, 1018612, 1493565],
    ["Balloons.bmp", "sporocilo2.txt", 40, 1, 2.79, 29.79, 7.35, 6.68, 1018612, 1482802],
    ["Balloons.bmp", "sporocilo2.txt", 40, 3, 2.79, 29.79, 7.35, 6.68, 1018612, 1482819],
    ["Balloons.bmp", "sporocilo2.txt", 40, 5, 2.79, 29.79, 7.35, 6.68, 1018612, 1482824]
]

# Create PDF document
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Set font for header and data
pdf.set_font("Arial", 'B', 5)

# Header
for col in header:
    pdf.cell(40 if col == header[0] else 15, 10, col, border=1, align='C')
pdf.ln()

# Data
pdf.set_font("Arial", '', 10)
for row in data:
    for i, item in enumerate(row):
        # Set the width for the first column, others are smaller
        cell_width = 40 if i == 0 else 15
        # Round numerical values to 2 decimal places
        if isinstance(item, float):
            item = f"{item:.2f}"
        pdf.cell(cell_width, 10, str(item), border=1, align='C')
    pdf.ln()

# Add a new page if needed for the image
# pdf.add_page()

# Add image to the PDF (at the end of the document)
image_path = "histogram.png"  # Specify the path to your image
pdf.image(image_path, x=10, y=pdf.get_y(), w=180)  # Add image, adjust the position as needed


# Output the PDF
pdf.output("table.pdf")
