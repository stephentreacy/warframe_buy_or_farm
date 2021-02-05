"""
Gets the prices of mods from warframe.market

"""

import json
import urllib.request
import pandas as pd
import time

def get_market_prices(item):
    """Create a dictionary for item with the highest 4 buy orders and lowest 4 sell orders"""
    
    api_url = 'https://api.warframe.market/v1/items/'
    name_url = item.lower().replace(' ','_').replace('-','_').replace("'",'').replace('&','and')
    url_item = api_url + name_url + '/statistics'
    statistics = {} 
    
    try:
        json_url_item = urllib.request.urlopen(url_item)          
    except:
        print(f'Item: {item} not found')
    else:
        data_item = json.loads(json_url_item.read())
        statistics = data_item['payload']['statistics_closed']['90days']
    finally:
        return statistics  
		
#URL of JSON file on github that gets regularly updated
url = 'https://raw.githubusercontent.com/WFCD/warframe-items/development/data/json/Mods.json'

#Get the mods
json_raw = urllib.request.urlopen(url)          
data = json.loads(json_raw.read())

df_mods = pd.DataFrame(data)
df_mods = df_mods[df_mods['tradable']]
df_mods.drop_duplicates(subset=['name'], inplace=True, ignore_index=True)

#Take the rare mod names
rare_mods = df_mods[df_mods['rarity'] == 'Rare']
rare_mod_names = rare_mods['name'].tolist()

#Test getting statistics
print(rare_mod_names[0])

mod_stats = get_market_prices(rare_mod_names[0])
print(mod_stats[-1]['volume'])
print(mod_stats[-1]['min_price'])
print(mod_stats[-1]['max_price'])
print(mod_stats[-1]['avg_price'])
print(mod_stats[-1]['median'])





