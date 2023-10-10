import json

import requests
from urllib.request import urlopen

def get_inventory(steamid):
    url = f'https://steamcommunity.com/inventory/{steamid}/730/2?l=russian&count=75'
    inventory_items = requests.get(url)
    data = json.loads(inventory_items.text)
    return data
