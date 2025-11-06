#read cards using pytesseract and soplits the text into lines List
#read function
#---input parameter: image_name without .png extension
#---returns: List of lines

import pytesseract # type: ignore
from PIL import Image # type: ignore
import re


def read(image_name):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    img = Image.open(rf'C:\Users\thars\Documents\Sort-ware-Solutions\Scanned_Cards\{image_name}.png')
    text = pytesseract.image_to_string(img)
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    return lines
