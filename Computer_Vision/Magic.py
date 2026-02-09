from . import write_csv
from . import magic_read_cards
from . import Bin_Movement
from . import stream
import requests 
import re
from datetime import datetime

bin_mapping= [0]*9

def magic_main(sort_by):
    write_csv.create_csv("magic")

    setlist=[]
    card_counter=0
    url = f"https://api.scryfall.com/sets"
    response = requests.get(url)
    sets = response.json()
    for s in sets["data"]:
        setlist.append(s["code"])

    for i in range(1, 11):
        card_counter+=1
        text=magic_read_cards.read(f"mtg{i}")
        #print(text)
        set_code,col_num=isolate_identifier(text,setlist)
        print(set_code,col_num)
        name,color,type,price=get_parameters(set_code, col_num)

        if len(set(color)) > 1:
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
    global bin_mapping

    if price=="unknown":
        bin_mapping[8]=bin_mapping[8]+1
        yield from stream.live_log(card_counter, name, color, type, price, "Price", "unknown",9,bin_mapping)
        Bin_Movement.move_bin9()
    elif float(price) < 0.25:
        bin_mapping[0]=bin_mapping[0]+1
        yield from stream.live_log(card_counter, name, color, type, price, "Price", f"${price}",1,bin_mapping)
        Bin_Movement.move_bin1()
    elif 0.25 <= float(price) < 1:
        bin_mapping[1]=bin_mapping[1]+1
        yield from stream.live_log(card_counter, name, color, type, price, "Price", f"${price}",2,bin_mapping)
        Bin_Movement.move_bin2()
    elif 1 <= float(price) <2.5:
        bin_mapping[2]=bin_mapping[2]+1
        yield from stream.live_log(card_counter, name, color, type, price, "Price", f"${price}",3,bin_mapping)
        Bin_Movement.move_bin3()
    elif 2.5 <= float(price) <5:
        bin_mapping[3]=bin_mapping[3]+1
        yield from stream.live_log(card_counter, name, color, type, price, "Price", f"${price}",4,bin_mapping)
        Bin_Movement.move_bin4()
    elif 5 <= float(price) <10:
        bin_mapping[4]=bin_mapping[4]+1
        yield from stream.live_log(card_counter, name, color, type, price, "Price", f"${price}",5,bin_mapping)
        Bin_Movement.move_bin5()
    elif 10 <= float(price) <20:
        bin_mapping[5]=bin_mapping[5]+1
        yield from stream.live_log(card_counter, name, color, type, price, "Price", f"${price}",6,bin_mapping)
        Bin_Movement.move_bin6()
    elif 20 <= float(price) <50:
        bin_mapping[6]=bin_mapping[6]+1
        yield from stream.live_log(card_counter, name, color, type, price, "Price", f"${price}",7,bin_mapping)
        Bin_Movement.move_bin7()
    elif float(price) >= 50:
        bin_mapping[7]=bin_mapping[7]+1
        yield from stream.live_log(card_counter, name, color, type, price, "Price", f"${price}",8,bin_mapping)
        Bin_Movement.move_bin8()

def magic_color(name,color,type,price,card_counter):
    global bin_mapping
    if color=="unknown":
        bin_mapping[8]=bin_mapping[8]+1
        yield from stream.live_log(card_counter, name, color, type, price, "Color", color,9,bin_mapping)
        Bin_Movement.move_bin9()
    elif color=="White":
        bin_mapping[0]=bin_mapping[0]+1
        yield from stream.live_log(card_counter, name, color, type, price, "Color", color,1,bin_mapping)
        Bin_Movement.move_bin1()
    elif color=="Blue":
        bin_mapping[1]=bin_mapping[1]+1
        yield from stream.live_log(card_counter, name, color, type, price, "Color", color,2,bin_mapping)
        Bin_Movement.move_bin2()
    elif color=="Black":
        bin_mapping[2]=bin_mapping[2]+1
        yield from stream.live_log(card_counter, name, color, type, price, "Color", color,3,bin_mapping)
        Bin_Movement.move_bin3()
    elif color=="Red":
        bin_mapping[3]=bin_mapping[3]+1
        yield from stream.live_log(card_counter, name, color, type, price, "Color", color,4,bin_mapping)
        Bin_Movement.move_bin4()
    elif color=="Green":
        bin_mapping[4]=bin_mapping[4]+1
        yield from stream.live_log(card_counter, name, color, type, price, "Color", color,5,bin_mapping)
        Bin_Movement.move_bin5()
    elif color=="Multicolor":
        bin_mapping[5]=bin_mapping[5]+1
        yield from stream.live_log(card_counter, name, color, type, price, "Color", color,6,bin_mapping)
        Bin_Movement.move_bin6()
    elif color=="Color-Less":
        bin_mapping[6]=bin_mapping[6]+1
        yield from stream.live_log(card_counter, name, color, type, price, "Color", color,7,bin_mapping)
        Bin_Movement.move_bin7()

    # BIN 8 is empty for maybe extra multicolor 

def magic_type(name,color,type,price,card_counter):
   
    global bin_mapping

    if type=="unknown":
        bin_mapping[8]=bin_mapping[8]+1
        yield from stream.live_log(card_counter, name, color, type, price, "Type", type,9,bin_mapping)
        Bin_Movement.move_bin9()
    elif type=="Creature":
        bin_mapping[0]=bin_mapping[0]+1
        yield from stream.live_log(card_counter, name, color, type, price, "Type", type,1,bin_mapping)
        Bin_Movement.move_bin1()
    elif type=="Artifact":
        bin_mapping[1]=bin_mapping[1]+1
        yield from stream.live_log(card_counter, name, color, type, price, "Type", type,2,bin_mapping)
        Bin_Movement.move_bin2()
    elif type=="Enchantment":
        bin_mapping[2]=bin_mapping[2]+1
        yield from stream.live_log(card_counter, name, color, type, price, "Type", type,3,bin_mapping)
        Bin_Movement.move_bin3()
    elif type=="Instant":
        bin_mapping[3]=bin_mapping[3]+1
        yield from stream.live_log(card_counter, name, color, type, price, "Type", type,4,bin_mapping)
        Bin_Movement.move_bin4()
    elif type=="Sorcery":
        bin_mapping[4]=bin_mapping[4]+1
        yield from stream.live_log(card_counter, name, color, type, price, "Type", type,5,bin_mapping)
        Bin_Movement.move_bin5()
    elif type=="Land":
        bin_mapping[5]=bin_mapping[5]+1
        yield from stream.live_log(card_counter, name, color, type, price, "Type", type,6,bin_mapping)
        Bin_Movement.move_bin6()
    elif type=="Planeswalker":
        bin_mapping[6]=bin_mapping[6]+1
        yield from stream.live_log(card_counter, name, color, type, price, "Type", type,7,bin_mapping)
        Bin_Movement.move_bin7()
    elif type=="Battle":
        bin_mapping[7]=bin_mapping[7]+1
        yield from stream.live_log(card_counter, name, color, type, price, "Type", type,8,bin_mapping)
        Bin_Movement.move_bin8()
   



###### HELPER FUNCTIONS #####

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