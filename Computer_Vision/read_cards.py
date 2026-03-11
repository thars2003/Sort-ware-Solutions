from pathlib import Path
from PIL import Image
import re

import pytesseract
import shutil
import sys
import os

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

    img = Image.open(img_path)
    text = pytesseract.image_to_string(img)
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    return lines