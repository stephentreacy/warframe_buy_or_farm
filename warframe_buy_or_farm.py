'''Warframe Buy or Farm
Takes a Tenno Zone link from a file
Gets the items you have selected
Shows the price of the items from warframe.market'''

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def get_tenno_url():
    '''Gets personal https://tenno.zone/planner/ URL from the text file'''
    
    with open('tenno_url.txt') as url_file:
        url = url_file.read()
        
    return url

def get_item_list(url):
    '''Returns the list of items with selected checkboxes from URL'''
    
    item_names = []

    #Open the URL as a headless Firefox instance
    print(f'Attempting to open {url} ...')
    opts = Options()
    opts.headless = True
    browser = webdriver.Firefox(options=opts)
    browser.get(url)

    #Find the names of items with a selected checkbox
    items = browser.find_elements_by_class_name('part-set-name')
    for item in items:
        checkbox = item.find_element_by_tag_name('input')
        if checkbox.is_selected():
            item_names.append(item.find_element_by_tag_name('span').get_attribute('innerHTML'))

    browser.quit()
    
    return item_names

tenno_url = get_tenno_url()
items = get_item_list(tenno_url)
print(items)

name_file = open('name_list.txt', 'w')
for item in items:
    name_file.write(item + '\n')
name_file.close()

    




