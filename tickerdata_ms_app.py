import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import tickerdata_app as app

#1. Price Data

selected_ticker = app.selected_stock
start_date = app.start_date
end_date = app.end_date

# Convert dates to string format
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

stock_data = yf.download(selected_ticker, start=start_date_str, end=end_date_str)

# Create a DataFrame with selected price data
stock_df = ()
stock_df = pd.DataFrame()
stock_df['High'] = stock_data['High']
stock_df['Low'] = stock_data['Low']
stock_df['Open'] = stock_data['Open']
stock_df['Close'] = stock_data['Close']
stock_df['Volume'] = stock_data['Volume']


#-------------------------------------------------------------
#2. Technical Indicators: Simple Moving Average - Chart

def calculate_sma(stock_data, window):
    return stock_data['Close'].rolling(window=window).mean()

# Calculate and plot indicators
def plot_sma(short_sma_window, long_sma_window, stock_data):
        # Calculate moving averages
        moving_averages = []
        short_sma_window = int(short_sma_window)
        long_sma_window = int(long_sma_window)

        if short_sma_window > 0 and long_sma_window > 0:
            sma_short = calculate_sma(stock_data, short_sma_window)
            sma_long = calculate_sma(stock_data, long_sma_window)
            moving_averages.append((f'SMA {short_sma_window}', sma_short))
            moving_averages.append((f'SMA {long_sma_window}', sma_long))

       # Plot indicators
        plt.figure(figsize=(10,6))
        plt.plot(stock_data['Close'], label='Close Price', color='blue')

        for label, ma in moving_averages:
            plt.plot(ma, label=label)

        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.title(f"{selected_ticker} Closing Price and Simple Moving Averages")
        plt.legend()
        st.pyplot(plt)
    
#---------------------------------------------------------------------------------

#3. Technical Indicators: Simple Moving Average - Backtest

def backtest_sma_crossover_strategy(stock_df, short_sma_window, long_sma_window):
    short_sma = calculate_sma(stock_df, short_sma_window)
    long_sma = calculate_sma(stock_df, long_sma_window)

    # Buy signal: when short EMA crosses above long EMA
    stock_df['SMA Buy Signal'] = (short_sma > long_sma) & (short_sma.shift(1) <= long_sma.shift(1))

    # Sell signal: when short EMA crosses below long EMA
    stock_df['SMA Sell Signal'] = (short_sma < long_sma) & (short_sma.shift(1) >= long_sma.shift(1))

    # Assume starting with cash, so the first signal should be a buy
    initial_position = "cash"
    positions = [initial_position]

    for i in range(1, len(stock_df)):
        if stock_df['SMA Buy Signal'].iloc[i]:
            positions.append("stock")
        elif stock_df['SMA Sell Signal'].iloc[i]:
            positions.append("cash")
        else:
            positions.append(positions[-1])

    stock_df['SMA Position'] = positions
    
    # Calculate returns
    stock_df['Daily SMA Strategy Return'] = np.where(stock_df['SMA Position'] == "stock", stock_df['Close'].pct_change(), 0)
    stock_df['Cumulative SMA Strategy Return'] = (stock_df['Daily SMA Strategy Return'] + 1).cumprod()
    total_sma_strategy_return = (stock_df['Cumulative SMA Strategy Return'].iloc[-1] - 1)*100
    return total_sma_strategy_return

# total_sma_strategy_return = backtest_sma_crossover_strategy(stock_df, short_sma_window, long_sma_window)
#-------------------------------------------------------------

#4. Technical Indicators: Exponential Moving Average - Chart

def calculate_ema(stock_data, window):
    return stock_data['Close'].ewm(span=window, adjust=False).mean()

# Calculate and plot indicators
def plot_ema(short_ema_window, long_ema_window, stock_data):

    # Calculate moving averages
    moving_averages = []
    short_ema_window = int(short_ema_window)
    long_ema_window = int(long_ema_window)
    
    if short_ema_window > 0 and long_ema_window > 0:
        ema_short = calculate_ema(stock_data, short_ema_window)
        ema_long = calculate_ema(stock_data, long_ema_window)
        moving_averages.append((f'EMA {short_ema_window}', ema_short))
        moving_averages.append((f'EMA {long_ema_window}', ema_long))

   # Plot indicators
    plt.figure(figsize=(10,6))
    plt.plot(stock_data['Close'], label='Close Price', color='blue')

    for label, ema in moving_averages:
        plt.plot(ema, label=label)

    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title(f"{selected_ticker} Closing Price and Exponential Moving Averages")
    plt.legend()
    st.pyplot(plt)
    
#---------------------------------------------------------------------------------

# #5. Technical Indicators: Exponential Moving Average - Backtest

def backtest_ema_crossover_strategy(stock_df, short_ema_window, long_ema_window):
    short_ema = calculate_ema(stock_df, short_ema_window)
    long_ema = calculate_ema(stock_df, long_ema_window)

    # Buy signal: when short EMA crosses above long EMA
    stock_df['EMA Buy Signal'] = (short_ema > long_ema) & (short_ema.shift(1) <= long_ema.shift(1))

    # Sell signal: when short EMA crosses below long EMA
    stock_df['EMA Sell Signal'] = (short_ema < long_ema) & (short_ema.shift(1) >= long_ema.shift(1))

    # Assume starting with cash, so the first signal should be a buy
    initial_position = "cash"
    positions = [initial_position]

    for i in range(1, len(stock_df)):
        if stock_df['EMA Buy Signal'].iloc[i]:
            positions.append("stock")
        elif stock_df['EMA Sell Signal'].iloc[i]:
            positions.append("cash")
        else:
            positions.append(positions[-1])

    stock_df['EMA Position'] = positions
    
    # Calculate returns
    stock_df['Daily EMA Strategy Return'] = np.where(stock_df['EMA Position'] == "stock", stock_df['Close'].pct_change(), 0)
    stock_df['Cumulative EMA Strategy Return'] = (stock_df['Daily EMA Strategy Return'] + 1).cumprod()
    total_ema_strategy_return = (stock_df['Cumulative EMA Strategy Return'].iloc[-1] - 1)*100
    return total_ema_strategy_return
    
#---------------------------------------------------------------------------------