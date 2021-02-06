"""Generates a webpage of the items and prices"""

from flask import Flask
import warframe_buy_or_farm as wf
from flask import render_template

app = Flask(__name__)

@app.route('/')
def hello():
    """Basic test page"""
    return 'Hello'

@app.route('/items')
def prime_items():
    """Lists items and orders on webpage"""

    item_orders = {}
    items = wf.get_item_list(wf.get_tenno_url())
        
    for item in items:
        item_dict = wf.get_market_prices(item)
        if item_dict:
            item_orders.update(item_dict)

    return render_template('items_page.html', items=item_orders)

@app.route('/mods')
def mods():
    """Lists mods and statistics on webpage"""
    table = wf.mods_df()
    print(table)
    #return wf.mods_df()
    return render_template('mods_page.html', tables=table)


if __name__ == '__main__':
    app.run(debug=True)
    
