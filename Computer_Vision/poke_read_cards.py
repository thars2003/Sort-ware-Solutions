import cv2
import pytesseract
import re
import os
import numpy as np
folder_path = '/Users/tharshinisubash/Documents/Sort-ware-Solutions/Scanned_Cards/'

def read(i):
    filename = f"cam{i}.jpg"  # adjust extension if needed
    img_path = os.path.join(folder_path, filename)

    # 🔹 Load image
    img = cv2.imread(img_path)
    if img is None:
        print(f"Could not load {img_path}")
        return None

    # 1. Pre-processing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Bilateral filter removes noise but keeps edges
    denoised = cv2.bilateralFilter(gray, 9, 75, 75)
    
    # Boost contrast
    contrast = cv2.convertScaleAbs(denoised, alpha=1.8, beta=-40)

    # 2. OCR with whitelist (numbers and slashes only)
    custom_config = r'--oem 3 --psm 11 -c tessedit_char_whitelist=0123456789/'
    text = pytesseract.image_to_string(contrast, config=custom_config)
    return text