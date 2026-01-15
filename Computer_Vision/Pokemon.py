from . import write_csv
from . import Read_Cards
import requests # type: ignore
import re
from datetime import datetime

def pokemon_main():
    write_csv.clear_csv("pokemon")
    write_csv.create_csv("pokemon")


    for i in range(23, 31):
        text=Read_Cards.read(f"test{i}")
        print(text)

    return None