import csv
import os
import time
from datetime import datetime

csv_path=""

def clear_csv(workplace):
    global csv_path
    csv_path=f"Output_Files/{workplace}.csv"
    if os.path.exists(csv_path):
        os.remove(csv_path)

def create_csv(game):
    global csv_path
    csv_path=f"Output_Files/sortware_export.csv"
    with open(csv_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Game", f"{game}"])

def append_csv(name,color,type,price):
    with open(csv_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, color, type, price])
