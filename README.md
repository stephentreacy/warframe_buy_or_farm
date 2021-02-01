# Warframe Buy or Farm
A work in progress to find the price of prime items in Warframe. Used to get a quick overview of prices and decide if the item should be bought or farmed in game.

Takes selected items from personal https://tenno.zone/planner/ link using Selenium.

Uses the https://warframe.market/ API to get current orders for each item.

Prints 4 of the highest buy orders and lowest sell orders to a webpage using Flask. Will update website to allow inputs. 

Running the python script webpage.py and going to page in browser produces the image below.

![alt text](https://github.com/stephentreacy/warframe_buy_or_farm/blob/main/images/output_webpage.PNG?raw=true)
