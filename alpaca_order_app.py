
import requests
import time
import locale
import yfinance as yf
import streamlit as st
import alpaca_trade_api as tradeapi


# Replace with your Alpaca API keys
API_KEY = "PKLKK4Y1DQJ9TQ8JBRZS"
API_SECRET = "VwYnY5BDW2GPkRtCRhXebcasmocMFD2yecPYIGTH"

# Initialize the Alpaca API client
api = tradeapi.REST(API_KEY, API_SECRET)

# Define the base URL for Alpaca API
base_url = "https://paper-api.alpaca.markets/v2"

# Define the headers
headers = {
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": API_SECRET
}

# Define the endpoint for placing orders
orders_endpoint = '/orders'

# Set the locale for currency formatting
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Streamlit app
st.title("Alpaca Order Placement")

symbol = st.text_input("Enter stock symbol:", value="JNJ")
stock_symbol = symbol
clicked = st.button("Get Last Trade Price")

def get_last_trade_price(stock_symbol):
    try:
        stock = yf.Ticker(stock_symbol)
        last_trade_price = stock.history(period="1d")["Close"][0]
        formatted_price = locale.currency(last_trade_price, grouping=True)
        return formatted_price
    except Exception as e:
        return "Error:", e

if clicked:
    try:
        jnj = yf.Ticker("JNJ")
        last_trade_price = jnj.history(period="1d")["Close"][0]
        formatted_price = get_last_trade_price(stock_symbol)
        st.write(f"Last Trade Price of {stock_symbol.upper()}: {formatted_price}")
    except Exception as e:
        st.write("Error:", e)

def place_market_order(symbol, dollar_amount):
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

    if order_response.status_code == 201:
        order_info = order_response.json()
        st.write("Order placed successfully:")
        st.write("Order ID:", order_info['id'])
        st.write("Symbol:", order_info['symbol'])
        st.write("Quantity:", order_info['qty'])
        st.write("Side:", order_info['side'])
        st.write("Type:", order_info['type'])
        st.write("Time in Force:", order_info['time_in_force'])
        
        # Start checking the order status immediately after placing the order
        order_id = order_info['id']
        while True:
            order_status = api.get_order(order_id).status
            st.write("Order Status:", order_status)

            if order_status == 'filled':
                st.write("Order has been filled.")
                break
            elif order_status in ('canceled', 'expired'):
                st.write("Order has been canceled or expired.")
                break

            # Wait before checking status again
            time.sleep(5)
    else:
        st.write("Order Pending.")

def main(stock_title, stock_symbol):
        
    clicked = st.button("Get Last Trade Price")

    if clicked:
        formatted_price = get_last_trade_price(stock_symbol)
        st.write(f"Last Trade Price of {stock_symbol.upper()}: {formatted_price}")     


dollar_amount = st.number_input("Enter dollar amount:", value=1000)

if st.button("Place Order"):
    place_market_order(symbol, dollar_amount)
