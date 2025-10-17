import csv
import os

csv_path=""

def clear_csv(workplace):
    global csv_path
    csv_path=f"Output_Files/{workplace}.csv"
    if os.path.exists(csv_path):
        os.remove(csv_path)

def create_csv(parameter):
    with open(csv_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", f"{parameter}"])

def append_csv(name,color):
    with open(csv_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, color])
