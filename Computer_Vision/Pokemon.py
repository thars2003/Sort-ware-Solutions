from turtle import color
from . import write_csv
from . import poke_read_cards
import requests # type: ignore
import re
from datetime import datetime
from . import stream
from . import sorting

# from turtle import color
# import write_csv
# import poke_read_cards
# import requests # type: ignore
# import re
# from datetime import datetime
# import Bin_Movement
# import stream
bin_mapping= [0]*9


def pokemon_main(sort_by):
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
            yield from sorting.price(name,"Category",category,type,price,card_counter)
        elif sort_by=="pokemon_category":
            yield from sorting.pokemon_category(name,"Category",category,type,price,card_counter)
        elif sort_by=="pokemon_type":
            yield from sorting.pokemon_type(name,"Category",category,type,price,card_counter)

    return None


###### HELPER FUNCTIONS #####
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


    category = card_info.get("category")
    # Category (Pokemon, Trainer, Energy)
    if category == "Pokemon":
        None  # pick first type
    elif category == "Trainer":
        category = card_info.get("trainerType")       # Item, Supporter, Stadium
    else:
        category = "Unknown"

    # Determine type
    type = card_info.get("types", [None])[0]  # pick first type
  

    # Price in USD from TCGplayer
    price = None
    pricing = card_info.get("pricing", {})
    tcg = pricing.get("tcgplayer", {})
    if "normal" in tcg and tcg["normal"]:
        price = tcg["normal"].get("marketPrice")

    return name, category, type, price

