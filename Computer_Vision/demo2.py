import cv2
import requests
import Led
import magic_read_cards 
import Magic
import Pokemon


Led.turn_on_light()

camera = cv2.VideoCapture(0)
if not camera.isOpened():
    print("Error: Could not open camera.")
    exit()

ret, frame = camera.read()
if ret: 
    img_path ="/home/sortware/Documents/Sort-ware-Solutions/Scanned_Cards/demo1.jpg"
    cv2.imwrite(img_path, frame) #change path
    print("Image saved as demo1.jpg")
else:
    print("Failed to capture image.")

camera.release()

print("Which card are you scanning?")
print("1: Pokémon")
print("2: Magic")

choice = input("Enter 1 or 2: ").strip()

if choice=="2":
    setlist=[]
    url = f"https://api.scryfall.com/sets"
    response = requests.get(url)
    sets = response.json()
    for s in sets["data"]:
        setlist.append(s["code"])

    text = magic_read_cards.read("demo1")

    set_code, col_num= Magic.isolate_identifier(text,setlist, debug=False)
    name, color, type, price= Magic.get_parameters(set_code, col_num)
    # print (set_code, col_num)
    print(name, color, type , price)

elif choice == "1":
    text = magic_read_cards.read("demo1")
    full_text = " ".join(text)
    print(text)
    print(full_text)
    col_num= Pokemon.isolate_identifier(full_text)
    print(col_num)
    name, category, type, price= Pokemon.get_parameters("swsh11", col_num)
    print (name, category, type, price)

else:
    None