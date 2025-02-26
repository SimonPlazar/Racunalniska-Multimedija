from fpdf import FPDF

# Data for the table
header = ["image_file", "thr", "compression_ratio", "psnr", "entropyOriginal", "entropyAltered", "blockinessOriginal", "blockinessAltered"]
data = [
    ["Baboon.bmp", 0, 0.7989788980355018, 29.79198363510271, 7.357877537566567, 7.416950612114, 209, 148],
    ["Baboon.bmp", 25, 2.056662890182443, 29.36894505495614, 7.357877537566567, 7.385441197787244, 209, 219],
    ["Baboon.bmp", 50, 3.6229027596173697, 29.136001497787426, 7.357877537566567, 7.33977389463277, 209, 206],
    ["Baboon.bmp", 100, 6.598861841610469, 28.955621868447952, 7.357877537566567, 7.28132060991703, 209, 115],
    ["Balloons.bmp", 0, 0.9438285392605505, 35.37348940975746, 7.345899563273674, 7.434573943173902, 24, 163],
    ["Balloons.bmp", 25, 6.045948264580577, 34.438849108973955, 7.345899563273674, 7.414144781848348, 24, 108],
    ["Balloons.bmp", 50, 7.506734067521213, 33.948483021325394, 7.345899563273674, 7.401596237130624, 24, 187],
    ["Balloons.bmp", 100, 8.496944926943906, 33.517711528119314, 7.345899563273674, 7.404200388908441, 24, 164],
    ["Barb.bmp", 0, 0.8455664488682004, 31.181345221082264, 7.483804151161467, 7.536171422308805, 142, 120],
    ["Barb.bmp", 25, 2.845222698937313, 30.680678029963133, 7.483804151161467, 7.520909531300132, 142, 42],
    ["Barb.bmp", 50, 4.5540952005432525, 30.349687138757183, 7.483804151161467, 7.49711368799062, 142, 83],
    ["Barb.bmp", 100, 7.250941685267857, 30.08609255797269, 7.483804151161467, 7.472581719404783, 142, 22],
    ["Barbara.bmp", 0, 0.8112504507392123, 30.612706316952213, 7.343768107855501, 7.83296437818259, 242, 250],
    ["Barbara.bmp", 25, 2.2477221686150273, 30.207141639514127, 7.343768107855501, 7.8054745041756455, 242, 147],
    ["Barbara.bmp", 50, 3.447461134467539, 30.006376605736072, 7.343768107855501, 7.792379789779346, 242, 172],
    ["Barbara.bmp", 100, 5.786287397507199, 29.765533200203386, 7.343768107855501, 7.775052961226066, 242, 189],
    ["Bark.bmp", 0, 0.7798754436800408, 28.9568177484041, 7.325036427721887, 7.381192523648539, 59, 225],
    ["Bark.bmp", 25, 1.774486473368074, 28.755945786818003, 7.325036427721887, 7.3408232967062395, 59, 96],
    ["Bark.bmp", 50, 2.9382046301877525, 28.57653122957181, 7.325036427721887, 7.271691179076109, 59, 170],
    ["Bark.bmp", 100, 5.119855286703493, 28.4084568247996, 7.325036427721887, 7.181677583016051, 59, 10],
    ["Bicycle.bmp", 0, 0.8412685729991978, 30.053102531360466, 4.369107314648612, 7.632903978291942, 235, 111],
    ["Bicycle.bmp", 25, 2.2136609815992196, 29.59591389437219, 4.369107314648612, 7.616050364008497, 235, 141],
    ["Bicycle.bmp", 50, 3.21744019752845, 29.426647070068537, 4.369107314648612, 7.593252947940123, 235, 160],
    ["Bicycle.bmp", 100, 5.095375442807643, 29.27808590382392, 4.369107314648612, 7.549024812156635, 235, 128],
    ["Board.bmp", 0, 0.9233000028867142, 33.774659405551674, 6.828014163463392, 6.9666726003362225, 101, 42],
    ["Board.bmp", 25, 4.863077624823101, 33.15573269636675, 6.828014163463392, 6.8689208245610365, 101, 175],
    ["Board.bmp", 50, 6.351357956802004, 32.78472989078773, 6.828014163463392, 6.8740480420103385, 101, 71],
    ["Board.bmp", 100, 8.3725584954291, 32.422628150662966, 6.828014163463392, 6.830114027303432, 101, 217],
    ["Boats.bmp", 0, 0.893249894197285, 32.69508463629244, 7.088123670044042, 7.223050748520196, 106, 41],
    ["Boats.bmp", 25, 4.046932180954606, 32.038698026888795, 7.088123670044042, 7.191280069060551, 106, 84],
    ["Boats.bmp", 50, 5.752282662829948, 31.75765819208044, 7.088123670044042, 7.172378213027146, 106, 5],
    ["Boats.bmp", 100, 7.726576727245698, 31.373304314789596, 7.088123670044042, 7.158927305859876, 106, 85],
    ["Bridge.bmp", 0, 0.830115014301888, 30.079248666113184, 5.705560157916678, 7.708322593455463, 240, 0],
    ["Bridge.bmp", 25, 2.411650449856156, 29.606952144679425, 5.705560157916678, 7.685451039884982, 240, 44],
    ["Bridge.bmp", 50, 4.232137114927005, 29.286004204845952, 5.705560157916678, 7.650166649029171, 240, 83],
    ["Bridge.bmp", 100, 6.953978653703899, 29.065945647969784, 5.705560157916678, 7.61635638189232, 240, 85],
    ["Cameraman.bmp", 0, 0.8545186325444166, 31.77365688252031, 6.9046085178417425, 7.09606417955054, 431416, 408466],
    ["Cameraman.bmp", 25, 2.9750346121209414, 31.263236531201084, 6.9046085178417425, 7.078484146614671, 431416, 408466],
    ["Cameraman.bmp", 50, 3.981522662631309, 31.071612481336923, 6.9046085178417425, 7.070340470623173, 431416, 408466],
    ["Cameraman.bmp", 100, 5.493556263045857, 30.704526828046477, 6.9046085178417425, 7.055225238084073, 431416, 408466],
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

# Output the PDF
pdf.output("table.pdf")