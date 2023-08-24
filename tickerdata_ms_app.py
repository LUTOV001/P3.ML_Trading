import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

#1. Price Data

# Read stock tickers from the CSV file
#tickers_df = pd.read_csv('\Resources\stock_tickers.csv', header=None)
tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'IBM', 'NVDA', 'JPM', 'V', 'UNH']
tickers_df = pd.DataFrame(tickers)
Nasdaq_NYSE_10 = tickers_df[0].tolist()

st.title("Stock Ticker Data Analysis")

# User input using Streamlit components
#selected_ticker = st.selectbox("Select a stock ticker from the list:", Nasdaq_NYSE_10)
selected_ticker = "AAPL"
start_date = st.date_input("Start Date:", datetime.now() - timedelta(days=365))
end_date = st.date_input("End Date:")

# Add a "Get Historic Price Data" button
get_data_button = st.button("Get Historic Price Data")

# Convert dates to string format
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

# Execute data query when the button is pressed
if get_data_button:
    # Fetch historical price data using yfinance
    stock_data = yf.download(selected_ticker, start=start_date_str, end=end_date_str)

    # Create a DataFrame with selected price data
    stock_df = ()
    stock_df = pd.DataFrame()
    stock_df['High'] = stock_data['High']
    stock_df['Low'] = stock_data['Low']
    stock_df['Open'] = stock_data['Open']
    stock_df['Close'] = stock_data['Close']

    # Display the DataFrame
    st.write(f"Historical price data for {selected_ticker} from {start_date_str} to {end_date_str}:")
    st.dataframe(stock_df)

#-------------------------------------------------------------
#2. Technical Indicators: Simple Moving Average - Chart
def calculate_sma(stock_data, window):
    return stock_data['Close'].rolling(window=window).mean()

# Streamlit
st.title("Stock Technical Indicators")
selected_ticker = st.text_input("Enter Ticker Symbol:", "AAPL")
start_date = st.date_input("Start Date", pd.to_datetime('2020-01-01'))
end_date = st.date_input("End Date", pd.to_datetime('2021-01-01'))

# User input for Simple Moving Average
show_sma = st.checkbox("Show Simple Moving Average")

# Fetch data
stock_data = yf.download(selected_ticker, start=start_date, end=end_date)

# Calculate and plot indicators
if show_sma:
    st.write("Enter window values for moving averages:")
    
    short_sma_window = st.number_input("Short SMA Window", value=10)
    long_sma_window = st.number_input("Long SMA Window", value=50)

    st.write(f"You've chosen short SMA window: {short_sma_window} and long SMA window: {long_sma_window}")
        
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
# User input for Simple Moving Average
show_sma_backtest = st.checkbox("Backtest your SMA strategy")
stock_data = yf.download(selected_ticker, start=start_date, end=end_date)

# Create a DataFrame with selected price data
stock_df = ()
stock_df = pd.DataFrame()
stock_df['High'] = stock_data['High']
stock_df['Low'] = stock_data['Low']
stock_df['Open'] = stock_data['Open']
stock_df['Close'] = stock_data['Close']
 
# Functions for calculations
def calculate_sma(stock_df, window):
    return stock_df['Close'].rolling(window=window, min_periods=1).mean()

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
    total_sma_strategy_return = (stock_df['Daily SMA Strategy Return'] + 1).prod()
    return total_sma_strategy_return
    
# Activate the backtest based on checkbox state
if show_sma_backtest:
    # NOTE: You may want to check if stock_df exists or if it has required data
    total_sma_strategy_return = backtest_sma_crossover_strategy(stock_df, short_sma_window, long_sma_window)
    stock_df.to_csv('sma_crossover.csv', index=False)
    total_sma_strategy_return = 100 * (total_sma_strategy_return - 1)
    st.write(f"Total return of SMA Crossover Strategy: {total_sma_strategy_return:.2f}%")
    # Optionally display the modified stock_df
    # st.dataframe(stock_df)    
    

#-------------------------------------------------------------

#4. Technical Indicators: Exponential Moving Average - Chart
def calculate_ema(stock_data, window):
    return stock_df['Close'].ewm(span=window, adjust=False).mean()

# User input for Exponential Moving Average
show_ema = st.checkbox("Show Exponential Moving Average")

# Fetch data
stock_data = yf.download(selected_ticker, start=start_date, end=end_date)

# Calculate and plot indicators
if show_ema:
    st.write("Enter window values for exponential moving averages:")
    
    short_ema_window = st.number_input("Short EMA Window", key="EMA_S", value=10)
    long_ema_window = st.number_input("Long EMA Window", key="EMA_L", value=50)

    st.write(f"You've chosen EMA short window: {short_ema_window} and EMA long window: {long_ema_window}")
        
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

# User input for Exponential Moving Average
show_ema_backtest = st.checkbox("Backtest your EMA strategy")
stock_data = yf.download(selected_ticker, start=start_date, end=end_date)

# # Create a DataFrame with selected price data
# stock_df = ()
# stock_df = pd.DataFrame()
# stock_df['High'] = stock_data['High']
# stock_df['Low'] = stock_data['Low']
# stock_df['Open'] = stock_data['Open']
# stock_df['Close'] = stock_data['Close']
 
# # Functions for calculations
# def calculate_ema(stock_df, window):
#     return stock_df['Close'].rolling(window=window, min_periods=1).mean()

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
    total_ema_strategy_return = (stock_df['Daily EMA Strategy Return'] + 1).prod()
    return total_ema_strategy_return
    
# Activate the backtest based on checkbox state
if show_ema_backtest:
    # NOTE: You may want to check if stock_df exists or if it has required data
    total_ema_strategy_return = backtest_ema_crossover_strategy(stock_df, short_ema_window, long_ema_window)
    stock_df.to_csv('ema_crossover.csv', index=False)
    total_ema_strategy_return = 100 * (total_ema_strategy_return - 1)
    st.write(f"Total return of EMA Crossover Strategy: {total_ema_strategy_return:.2f}%")
    # Optionally display the modified stock_df
    # st.dataframe(stock_df) 
    
#---------------------------------------------------------------------------------