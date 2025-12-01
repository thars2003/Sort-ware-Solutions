import Computer_Vision.Magic as Magic
# import Computer_Vision.Read_Cards as Read_Cards
# import requests

# setlist=[]
# url = f"https://api.scryfall.com/sets"
# response = requests.get(url)
# sets = response.json()
# for s in sets["data"]:
#     setlist.append(s["code"])

# # Magic.magic_main()
# for i in range(1, 18):
#     text=Read_Cards.read(f"test{i}")
#     #print(text)
#     set_code,col_num=Magic.isolate_identifier(text,setlist)
#     print(f"{i} Set Code: {set_code}, Collector Number: {col_num}")

Magic.magic_main() 
