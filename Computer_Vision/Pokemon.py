from . import write_csv
from . import poke_read_cards
import requests # type: ignore
import re
from datetime import datetime

def pokemon_main(sort_by):
    write_csv.clear_csv("pokemon")
    write_csv.create_csv("pokemon")

    card_counter=0
    for i in range(1, 11):
        card_counter+=1
        text=poke_read_cards.read(i)
        col_num=isolate_identifier(text)
        print(col_num)
        name,category,type,price=get_parameters("swsh11", col_num)
        write_csv.append_csv(name,category,type,price)

        if sort_by=="pokemon_price":
            yield from pokemon_price(name,category,type,price,card_counter)
        elif sort_by=="pokemon_category":
            yield from pokemon_category(name,category,type,price,card_counter)
        elif sort_by=="pokemon_type":
            yield from pokemon_type(name,category,type,price,card_counter)

    return None

def pokemon_price(name,category,type,price,card_counter):
    yield {
            "card_counter": card_counter,
            "name": name,
            "subtype": "Category",
            "subtype_value": category,
            "type": type,
            "price": price,
            "sort_by": "Price",
            "sort_value": f"${price}"
        }
def pokemon_category(name,category,type,price,card_counter):
    yield {
            "card_counter": card_counter,
            "name": name,
            "subtype": "Category",
            "subtype_value": category,
            "type": type,
            "price": price,
            "sort_by": "Category",
            "sort_value": category
        }
def pokemon_type(name,category,type,price,card_counter):
    yield {
            "card_counter": card_counter,
            "name": name,
            "subtype": "Category",
            "subtype_value": category,
            "type": type,
            "price": price,
            "sort_by": "Type",
            "sort_value": type
        }

def isolate_identifier(text):
    match = re.search(r'(\d{1,3})/(\d{3})', text)
    result = match.group(0) if match else "Not found"
    col_num= result.split("/", 1)[0].strip()
    return col_num

def get_parameters(set_code, col_num):
    if set_code == "unknown" or col_num == "Not found":
        return "unknown", "unknown", "unknown", "unknown"
    
    url = f"https://api.tcgdex.net/v2/en/cards/{set_code}-{col_num}"
 
    response = requests.get(url)
    card_info = response.json()
    name = card_info.get("name")

    # Category (Pokemon, Trainer, Energy)
    category = card_info.get("category")

    # Determine type
    if category == "Pokemon":
        type = card_info.get("types", [None])[0]  # pick first type
    elif category == "Trainer":
        type = card_info.get("trainerType")       # Item, Supporter, Stadium
    else:
        type = "Unknown"

    # Price in USD from TCGplayer
    price = None
    pricing = card_info.get("pricing", {})
    tcg = pricing.get("tcgplayer", {})
    if "normal" in tcg and tcg["normal"]:
        price = tcg["normal"].get("marketPrice")

    return name, category, type, price

