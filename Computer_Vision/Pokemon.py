from turtle import color
from . import write_csv
from . import poke_read_cards
import requests # type: ignore
import re
from datetime import datetime
from . import Bin_Movement
from . import stream

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
            yield from pokemon_price(name,category,type,price,card_counter)
        elif sort_by=="pokemon_category":
            yield from pokemon_category(name,category,type,price,card_counter)
        elif sort_by=="pokemon_type":
            yield from pokemon_type(name,category,type,price,card_counter)

    return None

def pokemon_price(name,category,type,price,card_counter):
    global bin_mapping
    if card_counter==1:
        bin_mapping= [0]*9

    if price=="unknown":
        bin_mapping[8]=bin_mapping[8]+1
        yield from stream.live_log(card_counter, name, category, type, price, "Price", "unknown",9,bin_mapping)
        Bin_Movement.move_bin(9)
    elif float(price) < 0.25:
        bin_mapping[0]=bin_mapping[0]+1
        yield from stream.live_log(card_counter, name, category, type, price, "Price", f"${price}",1,bin_mapping)
        Bin_Movement.move_bin(1)
    elif 0.25 <= float(price) < 1:
        bin_mapping[1]=bin_mapping[1]+1
        yield from stream.live_log(card_counter, name, category, type, price, "Price", f"${price}",2,bin_mapping)
        Bin_Movement.move_bin(2)
    elif 1 <= float(price) <2.5:
        bin_mapping[2]=bin_mapping[2]+1
        yield from stream.live_log(card_counter, name, category, type, price, "Price", f"${price}",3,bin_mapping)
        Bin_Movement.move_bin(3)
    elif 2.5 <= float(price) <5:
        bin_mapping[3]=bin_mapping[3]+1
        yield from stream.live_log(card_counter, name, category, type, price, "Price", f"${price}",4,bin_mapping)
        Bin_Movement.move_bin(4)
    elif 5 <= float(price) <10:
        bin_mapping[4]=bin_mapping[4]+1
        yield from stream.live_log(card_counter, name, category, type, price, "Price", f"${price}",5,bin_mapping)
        Bin_Movement.move_bin(5)
    elif 10 <= float(price) <20:
        bin_mapping[5]=bin_mapping[5]+1
        yield from stream.live_log(card_counter, name, category, type, price, "Price", f"${price}",6,bin_mapping)
        Bin_Movement.move_bin(6)
    elif 20 <= float(price) <50:
        bin_mapping[6]=bin_mapping[6]+1
        yield from stream.live_log(card_counter, name, category, type, price, "Price", f"${price}",7,bin_mapping)
        Bin_Movement.move_bin(7)
    elif float(price) >= 50:
        bin_mapping[7]=bin_mapping[7]+1
        yield from stream.live_log(card_counter, name, category, type, price, "Price", f"${price}",8,bin_mapping)
        Bin_Movement.move_bin(8)
        
def pokemon_category(name,category,type,price,card_counter):
    global bin_mapping
    if card_counter==1:
        bin_mapping= [0]*9
    
    if category=="unknown":
        bin_mapping[8]=bin_mapping[8]+1
        yield from stream.live_log(card_counter, name, category, type, price, "Category", category,9,bin_mapping)
        Bin_Movement.move_bin(9)
    elif category=="Pokemon":
        bin_mapping[0]=bin_mapping[0]+1
        yield from stream.live_log(card_counter, name, category, type, price, "Category", category,1,bin_mapping)
        Bin_Movement.move_bin(1)
    elif category=="Item":
        bin_mapping[1]=bin_mapping[1]+1
        yield from stream.live_log(card_counter, name, category, type, price, "Category", category,2,bin_mapping)
        Bin_Movement.move_bin(2)
    elif category=="Supporter":
        bin_mapping[2]=bin_mapping[2]+1
        yield from stream.live_log(card_counter, name, category, type, price, "Category", category,3,bin_mapping)
        Bin_Movement.move_bin(3)
    elif category=="Stadium":
        bin_mapping[3]=bin_mapping[3]+1
        yield from stream.live_log(card_counter, name, category, type, price, "Category", category,4,bin_mapping)
        Bin_Movement.move_bin(4)
    elif category=="null":
        bin_mapping[4]=bin_mapping[4]+1
        yield from stream.live_log(card_counter, name, category, type, price, "Category", category,5,bin_mapping)
        Bin_Movement.move_bin(5)
    # BIN 6,7,8 is empty for maybe overflow and unknown categories

def pokemon_type(name,category,type,price,card_counter): #grass, fire, water, lightning, psychic, fighting, darkness, colorless
    global bin_mapping
    if card_counter==1:
        bin_mapping= [0]*9
        
    if type=="unknown" or type == "Metal" or type == "Fairy" or type == "Dragon" or type == "null":
        bin_mapping[8]=bin_mapping[8]+1
        yield from stream.live_log(card_counter, name, category, type, price, "Type", type,9,bin_mapping)
        Bin_Movement.move_bin(9)
    elif type=="Grass":
        bin_mapping[0]=bin_mapping[0]+1
        yield from stream.live_log(card_counter, name, category, type, price, "Type", type,1,bin_mapping)
        Bin_Movement.move_bin(1)
    elif type=="Fire":
        bin_mapping[1]=bin_mapping[1]+1
        yield from stream.live_log(card_counter, name, category, type, price, "Type", type,2,bin_mapping)
        Bin_Movement.move_bin(2)
    elif type=="Water":
        bin_mapping[2]=bin_mapping[2]+1
        yield from stream.live_log(card_counter, name, category, type, price, "Type", type,3,bin_mapping)
        Bin_Movement.move_bin(3)
    elif type=="Lightning":
        bin_mapping[3]=bin_mapping[3]+1
        yield from stream.live_log(card_counter, name, category, type, price, "Type", type,4,bin_mapping)
        Bin_Movement.move_bin(4)
    elif type=="Psychic":
        bin_mapping[4]=bin_mapping[4]+1
        yield from stream.live_log(card_counter, name, category, type, price, "Type", type,5,bin_mapping)
        Bin_Movement.move_bin(5)
    elif type=="Fighting":
        bin_mapping[5]=bin_mapping[5]+1
        yield from stream.live_log(card_counter, name, category, type, price, "Type", type,6,bin_mapping)
        Bin_Movement.move_bin(6)
    elif type=="Darkness":
        bin_mapping[6]=bin_mapping[6]+1
        yield from stream.live_log(card_counter, name, category, type, price, "Type", type,7,bin_mapping)
        Bin_Movement.move_bin(7)
    elif type=="Colorless":
        bin_mapping[7]=bin_mapping[7]+1
        yield from stream.live_log(card_counter, name, category, type, price, "Type", type,8,bin_mapping)
        Bin_Movement.move_bin(8)
   

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

