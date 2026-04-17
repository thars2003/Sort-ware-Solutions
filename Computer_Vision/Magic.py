from Controls import dispenser
from Controls import servo
from . import write_csv
from . import read_cards
from . import stream
import requests 
import re
from datetime import datetime
from . import sorting
from . import camera
from Controls import buzzer
import time




def magic_main(sort_by, pause_event, stop_event):
    global Cards
    write_csv.create_csv("magic")
    setlist=[]
    card_counter=1
    dispenser._get_bin_motor().enable()
    dispenser._get_dispense_motor().enable()
    servo.initialize()
    # servo.release_card() #Louis Add for debug
    
    url = f"https://api.scryfall.com/sets"
    response = requests.get(url)
    sets = response.json()
    for s in sets["data"]:
        setlist.append(s["code"])
    stop_counter=0
    while True:
        if check_pause(pause_event, stop_event):
            break
        servo.hold_card()

        dispenser.dispense_card()
        # camera.capture_image()
        stop_break=False
        if check_pause(pause_event, stop_event):
                break
        for attempt in range(3):
            if stop_break:
                break
            if check_pause(pause_event, stop_event):
                break
            camera.capture_image()
            text = read_cards.read("image_capture")
            print(text)

            if text is None:
                if attempt==2:
                    return None
                continue
        
            
            flat = " ".join(text).upper()
            flat = re.sub(r"[^A-Z0-9]", "", flat)

            set_code, col_num = isolate_identifier(text, setlist)
            print(set_code, col_num)
            if set_code != "unknown" and col_num is not None:
                break

            elif (re.search(r"S[O0]RT", flat) or re.search(r"W[A4]RE", flat)) and stop_counter <3:
                stop_counter+=1
                stop_break=True
                print(stop_counter)
                if stop_counter >2:
                    print("stoping")
                    stop_event.set()
                    yield {"event": "stop", "reason": "sortware_limit"} 
                    time.sleep(4)
                    buzzer.boot_buzzer()   
                continue
            if stop_event.is_set():
                break
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
            yield from sorting.price(name,"Color",color,type,price,card_counter)
        elif sort_by=="mtg_color":
            yield from sorting.magic_color(name,"Color",color,type,price,card_counter)
        elif sort_by=="mtg_type":
            yield from sorting.magic_type(name,"Color",color,type,price,card_counter)
        card_counter+=1

        #Card Release
        servo.release_card()
        
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
            time.sleep(10)
            
            
        
        # return


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

def check_pause(pause_event, stop_event):
    while pause_event.is_set():
        if stop_event.is_set():  # don't get stuck in pause loop if stop is called
            return True
        time.sleep(0.1)
    if stop_event.is_set():
        return True
    return False