import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Read stock tickers from the CSV file
tickers_df = pd.read_csv('Resources/stock_tickers.csv', header=None)
Nasdaq_NYSE_10 = tickers_df[0].tolist()

# Get user input for stock ticker selection
print("Select a stock ticker from the list:")
for i, ticker in enumerate(Nasdaq_NYSE_10):
    print(f"{i + 1}. {ticker}")
choice = int(input("Enter the number corresponding to the stock ticker: ")) - 1

selected_ticker = Nasdaq_NYSE_10[choice]

# Calculate start and end dates based on today's date
end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

# Fetch historical price data using yfinance
stock_data = yf.download(selected_ticker, start=start_date, end=end_date)

# Create a DataFrame with selected price data
stock_df = pd.DataFrame()
stock_df['High'] = stock_data['High']
stock_df['Low'] = stock_data['Low']
stock_df['Open'] = stock_data['Open']
stock_df['Close'] = stock_data['Close']

# Display the DataFrame
print(f"Historical price data for {selected_ticker} for the past year:")
print(stock_df)
