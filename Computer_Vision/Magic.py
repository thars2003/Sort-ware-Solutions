from . import write_csv
from . import magic_read_cards
import requests 
import re
from datetime import datetime

def magic_main(sort_by):
    write_csv.clear_csv("magic")
    write_csv.create_csv("magic")

    setlist=[]
    card_counter=0
    url = f"https://api.scryfall.com/sets"
    response = requests.get(url)
    sets = response.json()
    for s in sets["data"]:
        setlist.append(s["code"])

    for i in range(1, 5):
        card_counter+=1
        text=magic_read_cards.read(f"cam{i}")
        #print(text)
        set_code,col_num=isolate_identifier(text,setlist)
        print(set_code,col_num)
        name,color,type,price=get_parameters(set_code, col_num)

        if len(color) > 1:
            color="Multicolor"
        elif len(color) == 0:
            color="Color-Less"
        elif "U" in color:
            color="Blue"
        elif "W" in color:
            color="White"
        elif "R" in color:
            color="Red"
        elif "B" in color:
            color="Black"
        elif "G" in color:
            color="Green"

        type= type.split("—", 1)[0].strip()

        write_csv.append_csv(name,color,type,price)
        if sort_by=="mtg_price":
            yield from magic_price(name,color,type,price,card_counter)
        elif sort_by=="mtg_color":
            yield from magic_color(name,color,type,price,card_counter)
        elif sort_by=="mtg_type":
            yield from magic_type(name,color,type,price,card_counter)    
        

    return None

def magic_price(name,color,type,price,card_counter):
    yield {
            "card_counter": card_counter,
            "name": name,
            "subtype": "Color",
            "subtype_value": color,
            "type": type,
            "price": price,
            "sort_by": "Price",
            "sort_value": f"${price}"
        }
def magic_color(name,color,type,price,card_counter):
    yield {
            "card_counter": card_counter,
            "name": name,
            "subtype": "Color",
            "subtype_value": color,
            "type": type,
            "price": price,
            "sort_by": "Color",
            "sort_value": color
        }
def magic_type(name,color,type,price,card_counter):
    yield {
            "card_counter": card_counter,
            "name": name,
            "subtype": "Color",
            "subtype_value": color,
            "type": type,
            "price": price,
            "sort_by": "Type",
            "sort_value": type
        }
    
def isolate_identifier(text,setlist, debug=False):

    set_code= "unknown"
    set_index= None

    for i,line in enumerate(reversed(text)):
        if "EN" in line:
            clean= re.sub(r"([^A-Z0-9])","",line.upper()) #keeps letters and digits only
            match= re.search(r"[A-Z0-9]{3}",clean)
            if match:
                candidate= match.group(0).lower()
                if candidate in setlist:
                    set_code= candidate
                else:
                    if debug:
                        print(f"Unknown set code: {candidate}")
                set_index= len(text)-i-1
                break

    col_num= None
    if set_index is not None:
        indexes= [set_index-1, set_index-2, set_index+1, set_index-3, set_index-4, set_index-5]
        for i in indexes:
            if 0<= i< len(text):
                line= text[i].replace("O","0").replace("o","0").replace("l","1")
                match= re.search(r"\b0*(\d{1,4})\b", line)
                if match:
                    candidate= int(match.group(1).lstrip("0") or "0")
                    current_year= datetime.now().year
                    if 1900<= candidate <= current_year+1:
                        if debug:
                            print(f"Skipping year-like number {candidate} at line {i}")
                        continue
                    col_num= candidate
                    if debug:
                        print(f"Found collector number {col_num} at line {i}")
                    break
        
    return set_code, col_num
    


def get_parameters(set_code, col_num):

    if set_code == "unknown" or col_num is None:
        return "unknown", "unknown", "unknown", "unknown"
    
    url = f"https://api.scryfall.com/cards/{set_code}/{col_num}"
    response = requests.get(url)
    card_info = response.json()
    name = card_info["name"]
    color = card_info["color_identity"]
    type = card_info["type_line"]
    price = card_info["prices"]["usd"]

    return name, color, type, price