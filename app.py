"""Generates a webpage of the items and prices"""

from flask import Flask, render_template, request
import warframe_buy_or_farm as wf
import pandas as pd
import time

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

        items = wf.get_item_list(request.form['url_tenno'])

        for item in items:
            orders = wf.get_market_prices(item, 'item')
            if orders:
                df_orders = pd.json_normalize(orders['orders'])
                df_sell = df_orders[(df_orders['user.status'] == 'ingame') & (df_orders['order_type'] == 'sell')]
                df_buy = df_orders[(df_orders['user.status'] == 'ingame') & (df_orders['order_type'] == 'buy')]
                sell_orders = df_sell.nsmallest(5, 'platinum')['platinum'].values
                buy_orders = df_buy.nlargest(5, 'platinum')['platinum'].values
                item_orders.update({item : [sell_orders, buy_orders, item.lower().replace(' ','_').replace('-','_').replace("'",'').replace('&','and')]})

            time.sleep(0.4)

        return render_template('items_page.html', items=item_orders)
    else:
        #Display text box for link
        return render_template('items_page.html', items=[])

@app.route('/mods', methods=['GET', 'POST'])
def mods():
    """Lists mods and statistics on webpage"""
    if request.method == 'POST':
        #Get updated prices and reload
        pass

    else:
        df_mod_stats = pd.read_csv("mod_stats.csv")
        df_mod_stats['url'] = df_mod_stats['name'].str.lower().str.replace(' ','_').str.replace('-','_').str.replace("'",'').str.replace('&','and')
        df_mod_stats['url'] = "<a href='https://warframe.market/items/" + df_mod_stats['url'] + "'>" + df_mod_stats['name'] + '</a>'
        html = df_mod_stats[['url','datetime','rarity','avg_price','volume']].to_html(escape=False)
        return render_template('mods_page.html', tables=html)


if __name__ == '__main__':
    app.run(debug=True)
    
