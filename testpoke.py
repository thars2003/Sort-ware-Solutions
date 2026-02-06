import cv2
import pytesseract
import re
import os
import numpy as np

folder_path = '/Users/tharshinisubash/Documents/Sort-ware-Solutions/Scanned_Cards/'
debug_folder = os.path.join(folder_path, 'debug_outputs')
os.makedirs(debug_folder, exist_ok=True) 

debug_folder = os.path.join(folder_path, 'debug_outputs')
for i in range(5, 9):
    filename = f"cam{i}.jpg"  # or .png depending on your files
    img_path = os.path.join(folder_path, filename)

    # 🔹 LOAD IMAGE (THIS WAS MISSING)
    img = cv2.imread(img_path)  

    # 1. Pre-processing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Bilateral filter removes the grainy "noise" but keeps text edges sharp
    denoised = cv2.bilateralFilter(gray, 9, 75, 75)
    
    # Boost contrast (Makes black text darker and background lighter)
    contrast = cv2.convertScaleAbs(denoised, alpha=1.8, beta=-40)

    # 2. SAVE THE IMAGE 
    # This allows you to open the file and see what the OCR sees
    debug_name = f"processed_{filename}"
    cv2.imwrite(os.path.join(debug_folder, debug_name), contrast)

    # 3. OCR with Whitelist (Numbers and slashes only)
    custom_config = r'--oem 3 --psm 11 -c tessedit_char_whitelist=0123456789/'
    text = pytesseract.image_to_string(contrast, config=custom_config)

    # 4. Extract
    match = re.search(r'(\d{1,3})/(\d{3})', text)
    result = match.group(0) if match else "Not found"

    print(f"Check debug_outputs/{debug_name} | Found: {result}")