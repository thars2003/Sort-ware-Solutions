#read cards using pytesseract and soplits the text into lines List
#read function
#---input parameter: image_name without .png extension
#---returns: List of lines

# import pytesseract # type: ignore
# from PIL import Image # type: ignore
# import re


# def read(image_name):
#     pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#     img = Image.open(rf'C:\Users\thars\Documents\Sort-ware-Solutions\Scanned_Cards\{image_name}.png')
#     text = pytesseract.image_to_string(img)
#     lines = [line.strip() for line in text.splitlines() if line.strip()]

#     return lines

import cv2
import numpy as np
from PIL import Image
import pytesseract

def read(image_name):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    path = rf'C:\Users\thars\Documents\Sort-ware-Solutions\Scanned_Cards\{image_name}.png'
    # 1. Load with OpenCV
    img = cv2.imread(path)
    if img is None:
        return ["Error: Image not found"]

    # 2. Pre-processing for small text
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Increase contrast and sharpen (Binarization)
    # This makes the background white and text black
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    # 3. Scale up (Tesseract likes text to be at least 30px high)
    resized = cv2.resize(thresh, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # 4. Run OCR with Page Segmentation Mode 6 (Assume a block of text)
    text = pytesseract.image_to_string(resized, config='--psm 6')
    
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines