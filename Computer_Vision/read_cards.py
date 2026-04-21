from pathlib import Path
from PIL import Image
import re

import pytesseract
import shutil
import sys
import os

import cv2

# import camera

# --- Auto-detect Tesseract (cross-platform) ---
tesseract_path = shutil.which("tesseract")

if tesseract_path is not None:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
else:
    if sys.platform.startswith("darwin"):  # macOS
        possible_paths = [
            "/opt/homebrew/bin/tesseract",
            "/usr/local/bin/tesseract"
        ]
    elif sys.platform.startswith("win"):  # Windows
        possible_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        ]
    else:
        possible_paths = []

    for path in possible_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            break


def read(image_name):
    BASE_DIR = Path(__file__).resolve().parent.parent
    SCANNED_CARDS_DIR = BASE_DIR / "Pre-Scanned_Cards"

    img_path = SCANNED_CARDS_DIR / f"{image_name}.jpg"

    if not img_path.exists():
        raise FileNotFoundError(f"Image not found: {img_path}")

    #  # Load and preprocess
    # img = cv2.imread(str(img_path))
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # # Increase contrast
    # gray = cv2.equalizeHist(gray)
    
    # # Threshold to make text pop
    # _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    img = Image.open(img_path)
    text = pytesseract.image_to_string(img)
    # text = pytesseract.image_to_string(thresh)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
   
    return lines


# camera.capture_image()
# print(read("image_capture"))