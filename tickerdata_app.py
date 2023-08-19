import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf

# Read stock tickers from the CSV file
tickers_df = pd.read_csv('Resources/stock_tickers.csv', header=None)
Nasdaq_NYSE_10 = tickers_df[0].tolist()

st.title("Stock Ticker Data Analysis")

# User input using Streamlit components
selected_ticker = st.selectbox("Select a stock ticker from the list:", Nasdaq_NYSE_10)
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
    stock_df = pd.DataFrame()
    stock_df['High'] = stock_data['High']
    stock_df['Low'] = stock_data['Low']
    stock_df['Open'] = stock_data['Open']
    stock_df['Close'] = stock_data['Close']

    # Display the DataFrame
    st.write(f"Historical price data for {selected_ticker} from {start_date_str} to {end_date_str}:")
    st.dataframe(stock_df)

