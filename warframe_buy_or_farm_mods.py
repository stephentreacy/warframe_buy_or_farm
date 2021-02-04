"""
Gets the prices of mods from warframe.market

"""

import json
import urllib.request

#URL of JSON file on github that gets regularly updated
url = 'https://raw.githubusercontent.com/WFCD/warframe-items/development/data/json/Mods.json'


json_raw = urllib.request.urlopen(url)          
data = json.loads(json_raw.read())
print(type(data))
print(data[0].keys())

