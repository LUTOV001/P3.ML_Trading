
#Imports
import os
import datetime
import json
import logging
import requests
import threading
import time
import pandas as pd

import alpaca_trade_api as api
from alpaca_trade_api.rest import TimeFrame

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.data.timeframe import TimeFrame

from alpaca.trading.client import TradingClient
from alpaca.trading.enums import AssetClass
from alpaca.trading.enums import AssetClasstrading_client
from alpaca.trading.enums import OrderSide, TimeInForce

from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.requests import MarketOrderRequest

from alpaca.trading.stream import TradingStream


import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

# Tracks market open time via countdown

def awaitMarketOpen(self):
  isOpen = self.alpaca.get_clock().is_open
  while(not isOpen):
    clock = self.alpaca.get_clock()
    openingTime = clock.next_open.replace(tzinfo=datetime.timezone.utc).timestamp()
    currTime = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
    timeToOpen = int((openingTime - currTime) / 60)
    print(str(timeToOpen) + " minutes til market open.")
    time.sleep(60)
    isOpen = self.alpaca.get_clock().is_open
    
# Get the total price of the array of input stocks.
def getTotalPrice(self, stocks, resp):
  totalPrice = 0
  for stock in stocks:
    bars = self.alpaca.get_barset(stock, "minute", 1)
    totalPrice += bars[stock][0].c
  resp.append(totalPrice)    

def get_orders():
    r = requests.get(ORDERS_URL, headers = HEADERS)
    
    return json.loads(r.content)
orders = get_orders()

print(orders)