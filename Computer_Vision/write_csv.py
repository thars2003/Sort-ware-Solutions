import csv
import os
import time
from datetime import datetime

csv_path=""

# def clear_csv(workplace):
#     global csv_path
#     csv_path=f"Output_Files/{workplace}.csv"
#     if os.path.exists(csv_path):
#         os.remove(csv_path)

def create_csv(game):
    global csv_path
    epoch_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_path=f"Output_Files/{game}-{current_time}.csv"
    with open(csv_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", f"{game}"])

def append_csv(name,color,type,price):
    with open(csv_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, color, type, price])
