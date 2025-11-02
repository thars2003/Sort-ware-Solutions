import requests

set_code = "eoe"
collector_number = "158"
url = f"https://api.scryfall.com/cards/{set_code}/{collector_number}"

response = requests.get(url)
data = response.json()

# Get card name and color
card_name = data['name']
card_colors = data['color_identity']  

print(f"Name: {card_name}")
print(f"Colors: {card_colors}")
