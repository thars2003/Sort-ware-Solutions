
import pytesseract # type: ignore
from PIL import Image # type: ignore
import re
def read(image_name):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    img = Image.open(rf'C:\Users\thars\Documents\Sort-ware-Solutions\Scanned_Cards\{image_name}.png')
    text = pytesseract.image_to_string(img)
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    return lines

    
    # if len(lines[-1].strip()) < 3:
    #     line2=lines[-2].strip()
    #     line1 = lines[-3].strip()
    # else:
    #     line2=lines[-1].strip()
    #     line1 = lines[-2].strip()

    # print(line1,line2)
    # if line1[0].isalpha():
    #     Collector_num = int(line1[1:5])
    # else:
    #     Collector_num = int(line1[:3])

    # set_code = line2[:3]
   
    # print(set_code)
    # print(Collector_num)
    
