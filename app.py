"""Generates a webpage of the items and prices"""

from flask import Flask, render_template, request
import warframe_buy_or_farm as wf

app = Flask(__name__)

@app.route('/')
def hello():
    """Basic test page"""
    return 'Hello'

@app.route('/items', methods=['GET', 'POST'])
def prime_items():
    """Lists items and orders on webpage"""

    if request.method == 'POST':
        #Use entered URL to get items
        item_orders = {}
        print(request.form)
        items = wf.get_item_list(request.form['url_tenno'])
            
        for item in items:
            item_dict = wf.get_market_prices(item)
            if item_dict:
                item_orders.update(item_dict)

        return render_template('items_page.html', items=item_orders)
    else:
        #Display text box for link
        return render_template('items_page.html', items=[])

@app.route('/mods')
def mods():
    """Lists mods and statistics on webpage"""

    return render_template('mods_page.html', tables=wf.mods_df())


if __name__ == '__main__':
    app.run(debug=True)
    
