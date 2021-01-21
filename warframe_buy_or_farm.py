'''Warframe Buy or Farm
Takes a Tenno Zone link from a file
Gets the items you have selected
Shows the price of the items from warframe.market'''

from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

def get_tenno_url():
    '''Gets personal https://tenno.zone/planner/ URL to scrape from text file'''
    
    with open('tenno_url.txt') as url_file:
        url = url_file.read()
        
    return url

def get_tenno_html(url):
    '''Returns the HTML string for url provided'''
    
    html = 'ERROR'
    context = ssl._create_unverified_context()

    print(f'Attempting to open {url} ...')
    try:
        page = urlopen(url, context=context)
        
    except Exception as e:
        print('Failed to open page')
        print(e)
        
    else:
        html = page.read().decode('utf-8') 
    
    return html


tenno_url = get_tenno_url()
tenno_html = get_tenno_html(tenno_url)
soup = BeautifulSoup(tenno_html, "html.parser")
print(soup.prettify())

