import requests # type: ignore
import pytesseract_test

setlist=[]
text= pytesseract_test.read("test9")
print(text)
url = f"https://api.scryfall.com/sets"
response = requests.get(url)
sets = response.json()
for s in sets["data"]:
        setlist.append(s["code"])

setline=None
for i, t in enumerate(text):
    if len(t) >= 3:  # avoid short strings
        prefix = t[:3].lower()
        #print(prefix)
        if prefix in setlist:
            if (text[i-1][2].isdigit()):
                setline = i
#print(setline)
setcode=text[setline][:3]
if text[setline-1][0].isalpha():
    collectornumber = int(text[setline-1][2:6])
else:
    collectornumber = int(text[setline-1][:3])
#print(setline)


print(setcode)
print(collectornumber)

