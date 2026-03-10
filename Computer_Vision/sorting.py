

from Controls import Bin_Movement
from . import stream

bin_mapping= [0]*9

def price(name,subtype,category,type,price,card_counter):
    global bin_mapping
    if card_counter==1:
        bin_mapping= [0]*9

    if price=="unknown":
        bin_mapping[8]=bin_mapping[8]+1
        yield from stream.live_log(card_counter, name,subtype, category, type, price, "Price", "unknown",9,bin_mapping)
        Bin_Movement.move_bin(9)
    elif float(price) < 0.25:
        bin_mapping[0]=bin_mapping[0]+1
        yield from stream.live_log(card_counter, name,subtype, category, type, price, "Price", f"${price}",1,bin_mapping)
        Bin_Movement.move_bin(1)
    elif 0.25 <= float(price) < 1:
        bin_mapping[1]=bin_mapping[1]+1
        yield from stream.live_log(card_counter, name,subtype, category, type, price, "Price", f"${price}",2,bin_mapping)
        Bin_Movement.move_bin(2)
    elif 1 <= float(price) <2.5:
        bin_mapping[2]=bin_mapping[2]+1
        yield from stream.live_log(card_counter, name,subtype, category, type, price, "Price", f"${price}",3,bin_mapping)
        Bin_Movement.move_bin(3)
    elif 2.5 <= float(price) <5:
        bin_mapping[3]=bin_mapping[3]+1
        yield from stream.live_log(card_counter, name,subtype, category, type, price, "Price", f"${price}",4,bin_mapping)
        Bin_Movement.move_bin(4)
    elif 5 <= float(price) <10:
        bin_mapping[4]=bin_mapping[4]+1
        yield from stream.live_log(card_counter, name,subtype, category, type, price, "Price", f"${price}",5,bin_mapping)
        Bin_Movement.move_bin(5)
    elif 10 <= float(price) <20:
        bin_mapping[5]=bin_mapping[5]+1
        yield from stream.live_log(card_counter, name,subtype, category, type, price, "Price", f"${price}",6,bin_mapping)
        Bin_Movement.move_bin(6)
    elif 20 <= float(price) <50:
        bin_mapping[6]=bin_mapping[6]+1
        yield from stream.live_log(card_counter, name,subtype, category, type, price, "Price", f"${price}",7,bin_mapping)
        Bin_Movement.move_bin(7)
    elif float(price) >= 50:
        bin_mapping[7]=bin_mapping[7]+1
        yield from stream.live_log(card_counter, name,subtype, category, type, price, "Price", f"${price}",8,bin_mapping)
        Bin_Movement.move_bin(8)


def pokemon_category(name,subtype,category,type,price,card_counter):
    global bin_mapping
    if card_counter==1:
        bin_mapping= [0]*9
    
    if category=="unknown":
        bin_mapping[8]=bin_mapping[8]+1
        yield from stream.live_log(card_counter, name,subtype, category, type, price, "Category", category,9,bin_mapping)
        Bin_Movement.move_bin(9)
    elif category=="Pokemon":
        bin_mapping[0]=bin_mapping[0]+1
        yield from stream.live_log(card_counter, name, subtype, category, type, price, "Category", category,1,bin_mapping)
        Bin_Movement.move_bin(1)
    elif category=="Item":
        bin_mapping[1]=bin_mapping[1]+1
        yield from stream.live_log(card_counter, name,subtype, category, type, price, "Category", category,2,bin_mapping)
        Bin_Movement.move_bin(2)
    elif category=="Supporter":
        bin_mapping[2]=bin_mapping[2]+1
        yield from stream.live_log(card_counter, name,subtype, category, type, price, "Category", category,3,bin_mapping)
        Bin_Movement.move_bin(3)
    elif category=="Stadium":
        bin_mapping[3]=bin_mapping[3]+1
        yield from stream.live_log(card_counter, name,subtype, category, type, price, "Category", category,4,bin_mapping)
        Bin_Movement.move_bin(4)
    elif category=="null":
        bin_mapping[4]=bin_mapping[4]+1
        yield from stream.live_log(card_counter, name,subtype, category, type, price, "Category", category,5,bin_mapping)
        Bin_Movement.move_bin(5)
    # BIN 6,7,8 is empty for maybe overflow and unknown categories



def magic_color(name,subtype,color,type,price,card_counter):
    global bin_mapping
    if card_counter==1:
        bin_mapping= [0]*9
    
    if color=="unknown":
        bin_mapping[8]=bin_mapping[8]+1
        yield from stream.live_log(card_counter, name,subtype, color, type, price, "Color", color,9,bin_mapping)
        Bin_Movement.move_bin(9)
    elif color=="White":
        bin_mapping[0]=bin_mapping[0]+1
        yield from stream.live_log(card_counter, name,subtype, color, type, price, "Color", color,1,bin_mapping)
        Bin_Movement.move_bin(1)
    elif color=="Blue":
        bin_mapping[1]=bin_mapping[1]+1
        yield from stream.live_log(card_counter, name,subtype, color, type, price, "Color", color,2,bin_mapping)
        Bin_Movement.move_bin(2)
    elif color=="Black":
        bin_mapping[2]=bin_mapping[2]+1
        yield from stream.live_log(card_counter, name,subtype, color, type, price, "Color", color,3,bin_mapping)
        Bin_Movement.move_bin(3)
    elif color=="Red":
        bin_mapping[3]=bin_mapping[3]+1
        yield from stream.live_log(card_counter, name,subtype, color, type, price, "Color", color,4,bin_mapping)
        Bin_Movement.move_bin(4)
    elif color=="Green":
        bin_mapping[4]=bin_mapping[4]+1
        yield from stream.live_log(card_counter, name,subtype, color, type, price, "Color", color,5,bin_mapping)
        Bin_Movement.move_bin(5)
    elif color=="Multicolor":
        bin_mapping[5]=bin_mapping[5]+1
        yield from stream.live_log(card_counter, name,subtype, color, type, price, "Color", color,6,bin_mapping)
        Bin_Movement.move_bin(6)
    elif color=="Color-Less":
        bin_mapping[6]=bin_mapping[6]+1
        yield from stream.live_log(card_counter, name,subtype, color, type, price, "Color", color,7,bin_mapping)
        Bin_Movement.move_bin(7)
    # BIN 8 is empty for maybe extra multicolor 


def pokemon_type(name,subtype,category,type,price,card_counter): #grass, fire, water, lightning, psychic, fighting, darkness, colorless
    global bin_mapping
    if card_counter==1:
        bin_mapping= [0]*9
        
    if type=="unknown" or type == "Metal" or type == "Fairy" or type == "Dragon" or type == "null":
        bin_mapping[8]=bin_mapping[8]+1
        yield from stream.live_log(card_counter, name,subtype, category, type, price, "Type", type,9,bin_mapping)
        Bin_Movement.move_bin(9)
    elif type=="Grass":
        bin_mapping[0]=bin_mapping[0]+1
        yield from stream.live_log(card_counter, name,subtype, category, type, price, "Type", type,1,bin_mapping)
        Bin_Movement.move_bin(1)
    elif type=="Fire":
        bin_mapping[1]=bin_mapping[1]+1
        yield from stream.live_log(card_counter, name,subtype, category, type, price, "Type", type,2,bin_mapping)
        Bin_Movement.move_bin(2)
    elif type=="Water":
        bin_mapping[2]=bin_mapping[2]+1
        yield from stream.live_log(card_counter, name,subtype, category, type, price, "Type", type,3,bin_mapping)
        Bin_Movement.move_bin(3)
    elif type=="Lightning":
        bin_mapping[3]=bin_mapping[3]+1
        yield from stream.live_log(card_counter, name,subtype, category, type, price, "Type", type,4,bin_mapping)
        Bin_Movement.move_bin(4)
    elif type=="Psychic":
        bin_mapping[4]=bin_mapping[4]+1
        yield from stream.live_log(card_counter, name,subtype, category, type, price, "Type", type,5,bin_mapping)
        Bin_Movement.move_bin(5)
    elif type=="Fighting":
        bin_mapping[5]=bin_mapping[5]+1
        yield from stream.live_log(card_counter, name,subtype, category, type, price, "Type", type,6,bin_mapping)
        Bin_Movement.move_bin(6)
    elif type=="Darkness":
        bin_mapping[6]=bin_mapping[6]+1
        yield from stream.live_log(card_counter, name,subtype, category, type, price, "Type", type,7,bin_mapping)
        Bin_Movement.move_bin(7)
    elif type=="Colorless":
        bin_mapping[7]=bin_mapping[7]+1
        yield from stream.live_log(card_counter, name,subtype, category, type, price, "Type", type,8,bin_mapping)
        Bin_Movement.move_bin(8)


def magic_type(name,subtype,color,type,price,card_counter):
    global bin_mapping
    if card_counter==1:
        bin_mapping= [0]*9
        
    if type=="unknown":
        bin_mapping[8]=bin_mapping[8]+1
        yield from stream.live_log(card_counter, name,subtype, color, type, price, "Type", type,9,bin_mapping)
        Bin_Movement.move_bin(9)
    elif type=="Creature":
        bin_mapping[0]=bin_mapping[0]+1
        yield from stream.live_log(card_counter, name,subtype, color, type, price, "Type", type,1,bin_mapping)
        Bin_Movement.move_bin(1)
    elif type=="Artifact":
        bin_mapping[1]=bin_mapping[1]+1
        yield from stream.live_log(card_counter, name,subtype, color, type, price, "Type", type,2,bin_mapping)
        Bin_Movement.move_bin(2)
    elif type=="Enchantment":
        bin_mapping[2]=bin_mapping[2]+1
        yield from stream.live_log(card_counter, name,subtype, color, type, price, "Type", type,3,bin_mapping)
        Bin_Movement.move_bin(3)
    elif type=="Instant":
        bin_mapping[3]=bin_mapping[3]+1
        yield from stream.live_log(card_counter, name,subtype, color, type, price, "Type", type,4,bin_mapping)
        Bin_Movement.move_bin(4)
    elif type=="Sorcery":
        bin_mapping[4]=bin_mapping[4]+1
        yield from stream.live_log(card_counter, name,subtype, color, type, price, "Type", type,5,bin_mapping)
        Bin_Movement.move_bin(5)
    elif type=="Land":
        bin_mapping[5]=bin_mapping[5]+1
        yield from stream.live_log(card_counter, name,subtype, color, type, price, "Type", type,6,bin_mapping)
        Bin_Movement.move_bin(6)
    elif type=="Planeswalker":
        bin_mapping[6]=bin_mapping[6]+1
        yield from stream.live_log(card_counter, name,subtype, color, type, price, "Type", type,7,bin_mapping)
        Bin_Movement.move_bin(7)
    elif type=="Battle":
        bin_mapping[7]=bin_mapping[7]+1
        yield from stream.live_log(card_counter, name,subtype, color, type, price, "Type", type,8,bin_mapping)
        Bin_Movement.move_bin(8)
   

