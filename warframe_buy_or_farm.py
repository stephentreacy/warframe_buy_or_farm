"""Warframe Buy or Farm
Takes a Tenno Zone link from a file
Gets the items selected via checkboxes on website
Shows the price of the items from warframe.market"""

import urllib.request
import json
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd

def get_tenno_url():
    """Gets personal https://tenno.zone/planner/ URL from the text file"""
    
    with open(r'tenno_url.txt') as url_file:
        url = url_file.read()
        
    return url

def get_item_list(url):
    """Returns the list of items with selected checkboxes from URL"""
    
    item_names = []

    #Open the URL as a headless Firefox instance
    print(f'Attempting to open {url} ...')
    opts = Options()
    opts.headless = True
    
    try:
        browser = webdriver.Firefox(options=opts)
        browser.get(url)
    except:
        print(f'Error connecting to {url}')
        item_names = []
    else:
        expand_checkbox = browser.find_element_by_xpath("//*[contains(text(), 'Include vaulted sets')]")
        browser.execute_script("arguments[0].click();", expand_checkbox.find_element_by_tag_name('input'))
        items = browser.find_elements_by_class_name('part-set')
        print('Connected to tenno zone, retrieving items...')

        for item in items:
            parts = item.find_elements_by_tag_name('label')
            for part in parts:
                if part is parts[0]:
                    item_name = part.text.title()
                if part.find_element_by_tag_name('input').is_selected():
                    if item_name != part.text.title():
                        if part.text.title().find('Neuroptics') > -1:
                            item_names.append(item_name + ' Neuroptics')
                        elif part.text.title().find('Systems') > -1:
                            item_names.append(item_name + ' Systems')
                        elif part.text.title().find('Chassis') > -1:
                            item_names.append(item_name + ' Chassis')
                        else:
                            item_names.append(item_name + ' ' + part.text.title())              
                    else:
                        item_names.append(item_name + ' Set')
    finally:            
        browser.quit()
        
    return item_names

def get_market_prices(item):
    """Create a dictionary for item with the highest 4 buy orders, lowest 4 sell orders and URL for item"""
    
    api_url = 'https://api.warframe.market/v1/items/'
    name_url = item.lower().replace(' ','_').replace('-','_').replace("'",'').replace('&','and')
    url_item = api_url + name_url + '/orders'
    item_orders = {}
    
    try:
        json_url_item = urllib.request.urlopen(url_item)          
    except:
        print(f'Item: {item} not found')
        print('Kubrow Items not supported')
    else:
        data_item = json.loads(json_url_item.read())
        payload_orders = data_item['payload']['orders']

        sells_all = []
        buys_all = []

        for order in payload_orders:
            if order['user']['status'] == 'ingame':
                if order['order_type'] == 'buy':
                    buys_all.append(order['platinum'])
                if order['order_type'] == 'sell':
                    sells_all.append(order['platinum'])

        buying = sub_list(buys_all, 'buy')
        selling = sub_list(sells_all)
        time.sleep(.5)
        item_orders[item] = [buying,selling,name_url]
        
        return item_orders

def sub_list(orders, order_type='sell'):
    '''Sorts the list and gets the 4 highest buy orders or 4 lowest sell orders'''
    
    if order_type == 'sell':
        orders.sort()
    else:
        orders.sort(reverse=True)
        
    if len(orders) < 5:
        return orders
    else:
        return orders[:4]

def mods_df():
    df_mod_stats = pd.read_csv("mod_stats.csv")
    df_mod_stats['url'] = df_mod_stats['name'].str.lower().str.replace(' ','_').str.replace('-','_').str.replace("'",'').str.replace('&','and')
    df_mod_stats['url'] = "<a href='https://warframe.market/items/" + df_mod_stats['url'] + "'>" + df_mod_stats['name'] + '</a>'
    html = df_mod_stats.to_html(escape=False)
    return html


if __name__ == '__main__':

    tenno_url = get_tenno_url()
    items = get_item_list(tenno_url)
    print('Items Retrieved')
    item_orders = {}
    for item in items:
        item_dict = get_market_prices(item)
        if item_dict:
            item_orders.update(item_dict)

    print(item_orders)

            
            



