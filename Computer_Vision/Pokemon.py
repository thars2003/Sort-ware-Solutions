from turtle import color
from . import write_csv
from . import read_cards
import requests # type: ignore
import re
from datetime import datetime
from . import stream
from . import sorting
from . import camera 
from Controls import dispenser
from Controls import servo
import time
from Controls import buzzer
from Computer_Vision import Led


bin_mapping= [0]*9


def pokemon_main(sort_by, pause_event, stop_event):
    write_csv.create_csv("pokemon")
    card_counter=1
    temp=0
    dispenser._get_bin_motor().enable()
    dispenser._get_dispense_motor().enable()
    servo.initialize()
    stop_counter=0

    while True:
        if check_pause(pause_event, stop_event):
            break
        servo.hold_card()

        dispenser.dispense_card()
        # camera.capture_image()

        stop_breaks=False
        if check_pause(pause_event, stop_event):
                break

        col_num = None

        for attempt in range(8):
            if check_pause(pause_event, stop_event):
                break
            if attempt < 4:
                Led.poke_turn_on_light(0, 0, 255)
            else:
                Led.poke_turn_on_light(255, 255, 255)

            camera.capture_image()
            text = read_cards.read("image_capture")
            print(text)

            if text is None:
                print(f"Attempt {attempt+1}: text is None, retrying...")
                continue

            full_text = " ".join(text)
            flat = full_text.upper()
            flat = re.sub(r"[^A-Z0-9]", "", flat)

            # Check for sortware BEFORE trying to isolate identifier
            if re.search(r"S[O0]RT", flat) or re.search(r"W[A4]RE", flat):
                stop_counter += 1
                print(f"Sortware detected ({stop_counter})")
                if stop_counter > 2:
                    print("stopping")
                    stop_event.set()
                    yield {"event": "stop", "reason": "sortware_limit"}
                    time.sleep(4)
                    buzzer.boot_buzzer()
                stop_breaks = True
                break

            col_num = isolate_identifier(full_text)
            print(f"Attempt {attempt+1}: col_num = {col_num}")

            # ✅ Only break if we actually found a valid col_num
            if col_num != "Not found" and col_num is not None:
                break

            print(f"Attempt {attempt+1}: col_num not found, retrying...")

        if stop_event.is_set():
            break
        # for attempt in range(3):
        #     if stop_break:
        #         break
        #     if check_pause(pause_event, stop_event):
        #         break
        #     camera.capture_image()
        #     text = read_cards.read("image_capture")
        #     print(text)

        #     if text is None:
        #         if attempt==2:
        #             return None
        #         continue
     
        #     text = read_cards.read("image_capture")
                
        #     full_text = " ".join(text)
        #     col_num=isolate_identifier(full_text)
        #     if col_num=="Not_found":
        #             if attempt== 2:
        #                 return None
        #             continue
            
        #     print(col_num)
        #     flat = " ".join(text).upper()
        #     flat = re.sub(r"[^A-Z0-9]", "", flat)

        #     if col_num is not None or col_num != "Not found":
        #         break

        #     elif (re.search(r"S[O0]RT", flat) or re.search(r"W[A4]RE", flat)) and stop_counter <3:
        #         stop_counter+=1
        #         stop_break=True
        #         print(stop_counter)
        #         if stop_counter >2:
        #             print("stoping")
        #             stop_event.set()
        #             yield {"event": "stop", "reason": "sortware_limit"} 
        #             time.sleep(4)
        #             buzzer.boot_buzzer()   
        #         continue
        #     if stop_event.is_set():
        #         break

        name,category,type,price=get_parameters("swsh11", col_num)
        write_csv.append_csv(name,category,type,price)

        if sort_by=="pokemon_price":
            yield from sorting.price(name,"Category",category,type,price,card_counter)
        elif sort_by=="pokemon_category":
            yield from sorting.pokemon_category(name,"Category",category,type,price,card_counter)
        elif sort_by=="pokemon_type":
            yield from sorting.pokemon_type(name,"Category",category,type,price,card_counter)
        
        servo.release_card()
        card_counter+=1

        sortware_detected=False
       
        for attempt in range(3):  
            camera.capture_image()
            text = read_cards.read("image_capture")
            # print (text)
            print("Reading card again")

            if text is None:
                continue

            flat = " ".join(text).upper()
            flat = re.sub(r"[^A-Z0-9]", "", flat)  # strip spaces/punctuation

            if re.search(r"S[O0]RT", flat) or re.search(r"W[A4]RE", flat):
                sortware_detected= True
                print("read sortware")
                break

            else:
                servo.release_card()
                print("pushing again")

        if not sortware_detected:
            #servo.release()
            print("did not sortware")
            buzzer.boot_buzzer()
            pause_event.set() 
            yield {"pause": True} 
            while pause_event.is_set():
                time.sleep(0.3)

###### HELPER FUNCTIONS #####
def isolate_identifier(text):
    full_text = " ".join(text) if isinstance(text, list) else text
    
    match = re.search(r'(\d{1,3})\s*/\s*(\d{3})', full_text)
    if match:
        col_num = str(match.group(1)) # strip leading zeros: 046 -> 46
        return col_num
    
    return "Not found"

def get_parameters(set_code, col_num):
    if col_num == "Not found" or col_num is None:
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
    tcg = pricing.get("tcgplayer", {}) or {}
    if "normal" in tcg and tcg["normal"]:
        price = tcg["normal"].get("marketPrice")

    return name, category, type, price

def check_pause(pause_event, stop_event):
    while pause_event.is_set():
        if stop_event.is_set():  # don't get stuck in pause loop if stop is called
            return True
        time.sleep(0.1)
    if stop_event.is_set():
        return True
    return False