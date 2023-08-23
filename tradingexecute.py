

import json
import time
import locale
import logging
import requests
import threading
import alpaca_trade_api as api

from time import sleep 

from alpaca_trade_api.rest import TimeFrame

import plotly.graph_objects as go
import plotly.express as px


# Importing the api and instantiating the rest client according to our keys
#Establish Alpaca connection

API_KEY = "PKLKK4Y1DQJ9TQ8JBRZS"
API_SECRET = "VwYnY5BDW2GPkRtCRhXebcasmocMFD2yecPYIGTH"
alpaca = api.REST(API_KEY, API_SECRET)

# Alpaca API endpoint for account information
base_url = 'https://paper-api.alpaca.markets'  # Use 'https://api.alpaca.markets' for live trading
account_endpoint = '/v2/account'
positions_endpoint = '/v2/positions'
orders_endpoint = '/v2/orders'

# Construct headers for the request
headers = {
    'APCA-API-KEY-ID': API_KEY,
    'APCA-API-SECRET-KEY': API_SECRET
}

# Make the API request
response = requests.get(base_url + account_endpoint, headers=headers)

# Print the account information
if response.status_code == 200:
    account_info = response.json()
    print("Account Information:")
    print("Account ID:", account_info['id'])
    print("Buying Power:", account_info['buying_power'])
    print("Cash:", account_info['cash'])
    # ... and so on
else:
    print("Failed to retrieve account information. Status code:", response.status_code)
    

    # Retrieve open positions (assets)
response_positions = requests.get(base_url + positions_endpoint, headers=headers)
if response_positions.status_code == 200:
    positions_data = response_positions.json()
    print("\nOpen Positions:")
    for position in positions_data:
        print("Symbol:", position['symbol'])
        print("Quantity:", position['qty'])
        print("Average Entry Price:", position['avg_entry_price'])
        print("Market Value:", position['market_value'])
        # print("Filled ID:", position['filled_at'])
        print("Asset ID:", position['asset_id'])
        print("---")
else:
    print("Failed to retrieve positions. Status code:", response_positions.status_code)
    

    #Get cash balance after purchases

# Set the locale to the user's default for appropriate comma separators
locale.setlocale(locale.LC_ALL, '')

# Retrieve account information
response = requests.get(base_url + account_endpoint, headers=headers)

if response.status_code == 200:
    account_info = response.json()
    cash_balance = float(account_info['cash'])
    buying_power = float(account_info['buying_power'])

    # Format values with comma separators and as currency
    formatted_cash_balance = locale.currency(cash_balance, grouping=True)
    formatted_buying_power = locale.currency(buying_power, grouping=True)

    print("Cash Balance:", formatted_cash_balance)
    print("Buying Power:", formatted_buying_power)
else:
    print("Failed to retrieve account information. Status code:", response.status_code)
    print("Response:", response.text)

    
# previous day close or average of bid and ask
# Calculate the average of 'ask_price' (ap) and 'bid_price' (bp)
ask_price = latest_quote.ap
bid_price = latest_quote.bp
average_price = (ask_price + bid_price) / 2

print(f"Bid price: ${bid_price:.2f}")
print(f"Ask price: ${ask_price:.2f}")
print(f"Average price: ${average_price:.2f}")    


    # Initialize the Alpaca API client for placing a market order based on 
api = tradeapi.REST(API_KEY, API_SECRET)

# Define the endpoint for placing orders
orders_endpoint = '/v2/orders'

# Specify the stock symbol for which you want to execute a market order
symbol = 'JNJ'  # Replace with the desired stock symbol from Streamlit

# Define the dollar amount you want to spend
dollar_amount = 1000  # Replace with the desired dollar amount

# Calculate the quantity of shares based on the dollar amount and current ask price
latest_trade = api.get_latest_trade(symbol)
ask_price = latest_trade.price
quantity = int(dollar_amount / ask_price)

# Construct the order payload
order_payload = {
    'symbol': symbol,
    'qty': quantity,
    'side': 'buy',      # 'buy' for a market buy order
    'type': 'market',   # 'market' order type
    'time_in_force': 'gtc'  # 'gtc' for "good 'til canceled"
}

# Place the market order
order_response = requests.post(base_url + orders_endpoint, json=order_payload, headers=headers)

if order_response.id is not None:
    order_info = order_response
    print("Order placed successfully:")
    print("Order ID:", order_info.id)
    print("Symbol:", order_info.symbol)
    print("Quantity:", order_info.qty)
    print("Side:", order_info.side)
    print("Type:", order_info.type)
    print("Time in Force:", order_info.time_in_force)
    
    # Start checking the order status immediately after placing the order
    order_id = order_info.id
    while True:
        order_status = api.get_order(order_id).status
        print("Order Status:", order_status)

        if order_status == 'filled':
            print("Order has been filled.")
            break
        elif order_status in ('canceled', 'expired'):
            print("Order has been canceled or expired.")
            break

        # Wait before checking status again
        time.sleep(5)
else:
    print("Order Pending.")