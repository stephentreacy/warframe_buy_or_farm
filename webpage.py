'''Generates a webpage of the items and prices'''

from flask import Flask
import warframe_buy_or_farm as wf

app = Flask(__name__)

@app.route('/')
def hello():
    '''Basic test page'''
    return 'Hello'

@app.route('/items')
def items():
    '''Lists items on webpage'''
    url = wf.get_tenno_url()
    items = wf.get_item_list(url)
    html = ''
    for item in items:
        html +='<p>' + item + '</p>'
        print(item)
    return html

if __name__ == '__main__':
    app.run()
    
