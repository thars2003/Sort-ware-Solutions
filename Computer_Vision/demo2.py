import cv2
import requests
# import Led
import magic_read_cards 
import Magic

# Led.turn_on_led()

# camera = cv2.VideoCapture(0)
# if not camera.isOpened():
#     print("Error: Could not open camera.")
#     exit()

# ret, frame = camera.read()
# if ret:
#     cv2.imwrite("demo1.jpg", frame) #change path
#     print("Image saved as demo1.jpg")
# else:
#     print("Failed to capture image.")

# camera.release()
setlist=[]
url = f"https://api.scryfall.com/sets"
response = requests.get(url)
sets = response.json()
for s in sets["data"]:
    setlist.append(s["code"])

text = magic_read_cards.read("demo2")

set_code, col_num= Magic.isolate_identifier(text,setlist, debug=False)
name, color, type, price= Magic.get_parameters(set_code, col_num)