# Libraries
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
from plotly import graph_objs as go
from prophet import Prophet
from prophet.plot import plot_plotly
import numpy as np
import matplotlib.pyplot as plt
import tickerdata_ms_app as ms_app
import machine_learning as ml_app
import alpaca_trade_api as tradeapi


# Title
st.title('Stock Trading Using Machine Learning')


# Content
st.image('./trading_bot.png')

st.write(
    """
The objective for this project was to build predictive models using time series analysis and different machine learning algorithms
to predict future stock prices and enable buy / sell decision making. The goal is to help our users develop 
profitable trading strategies based on the results of the machine learning models.
    """
)

st.subheader("Stock Ticker Data Analysis")

start_date = st.date_input("Start Date:", datetime.now() - timedelta(days=1825), key="start_date_input")
end_date = st.date_input("End Date:")

# List of Tickers

def generate_selected_stock(stocks):
    selected_stock = st.selectbox('Select a stock ticker and date range for analysis:', stocks)
    return selected_stock

# Pull data from Yahoo Finance 
def load_data(ticker):
    data = yf.download(ticker, start_date, end_date)
    #data.reset_index()
    return data

stocks = ['AAPL', 'MSFT','AMZN','GOOGL','META','IBM','NVDA', 'JPM','V','UNH']

selected_stock = generate_selected_stock(stocks)
data = load_data(selected_stock)


# Add a "Get Historic Price Data" button
get_data_button = st.button("Get Historic Price Data")


# Execute data query when the button is pressed
if get_data_button:
    st.write('__Historical Stock Data__')
    st.write(data)
   
    def plot_raw_data():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data['Open'], name='stock_open'))
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='stock_close'))
        fig.layout.update(title="Historical Stock Data Plot", xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)
    
    plot_raw_data()
    
# --------------------------------------------------------------------------

#2. Technical Indicators: Simple Moving Average - Chart

# Section Title
st.subheader("Stock Technical Indicators")

# User input for Simple Moving Average Chart
show_sma = st.checkbox("Show Simple Moving Average", key="plot_sma")

if show_sma:
        st.write("Enter window values for moving averages:")
        short_sma_window = st.number_input("Short SMA Window", value=10, key="short_sma_window")
        long_sma_window = st.number_input("Long SMA Window", value=50, key="long_sma_window")
        st.write(f"You've chosen short SMA window:  {short_sma_window} and long SMA window: {long_sma_window}")    
        
        ms_app.plot_sma(short_sma_window, long_sma_window, data)
  
    
# User input for Simple Moving Average Backtesting
show_sma_backtest = st.checkbox("Backtest your SMA strategy", key="backtest_sma")
if show_sma_backtest:
        total_sma_strategy_return = ms_app.backtest_sma_crossover_strategy(data, short_sma_window, long_sma_window)   
        st.write(f"Total return of SMA Crossover Strategy: {total_sma_strategy_return:.2f}%")                                


# User input for Exponential Moving Average Chart
show_ema = st.checkbox("Show Exponential Moving Average", key="plot_ema")

if show_ema:
        st.write("Enter window values for moving averages:")
        short_ema_window = st.number_input("Short EMA Window", value=10, key="short_ema_window")
        long_ema_window = st.number_input("Long EMA Window", value=50, key="long_ema_window")
        st.write(f"You've chosen short EMA window: {short_ema_window} and long EMA window: {long_ema_window}")

        ms_app.plot_ema(short_ema_window, long_ema_window, data)

# User input for Simple Moving Average Backtesting
show_ema_backtest = st.checkbox("Backtest your EMA strategy", key="backtest_ema")
if show_ema_backtest:
        total_ema_strategy_return = ms_app.backtest_ema_crossover_strategy(data, short_ema_window, long_ema_window)   
        st.write(f"Total return of EMA Crossover Strategy: {total_ema_strategy_return:.2f}%")                                


# ---------------------------------------------------------------------------
# # resume Mike's code

# st.subheader('Prophet Forecast')
# st.write(
#     """
#  Time series analysis involves analyzing time series data to identify meaningful patterns in the data. 
#  Time series forecasting involves using a model that's based on historical data to predict future values in the time series. 
#  Prophet is an open-source library for time series forecasting that Facebook developed to analyze their data and it automates the process of time series forecasting.
#     """
# )

# n_years = st.slider("Years of prediction:", 1, 4)
# period = n_years *365

# # Add a "Run Prophet Forecast" button
# prophet_button = st.button("Run Prophet Forecast")

# # Run LSTM ML Model and provide buy / sell recommendation if button is pressed
# if prophet_button: 
# # Run Propeht Forecast
#     df_train = data[['Date', 'Close']]
#     df_train = df_train.rename(columns={"Date": "ds", "Close":"y"})

#     m = Prophet()
#     m.fit(df_train)
#     future = m.make_future_dataframe(periods=period)
#     forecast = m.predict(future)

#     st.write('__Prophet Forecast Data__')
#     st.write(forecast.tail())

#     fig1 = plot_plotly(m, forecast)
#     fig1.layout.update(title = "Prophet Forecast Plot")
#     st.plotly_chart(fig1)
    


# st.subheader('LSTM Model Recommendation')
# st.write(
#     """
# LSTM (Long Short-Term Memory) is a type of recurrent neural network (RNN) machine learning model. 
# LSTM networks are particularly well-suited for time series forecasting tasks due to their ability to 
# capture sequential dependencies and patterns in the data.  Here we will use the LSTM ML Model to predict 
# the future stock price selected and provide a buy / sell recommendation based on predicted stock price. 
#     """
# )

# # Add a "Run LSTM ML Model" button
# lstm_button = st.button("Get Recommendation")

# # Run LSTM ML Model and provide buy / sell recommendation if button is pressed
# # if lstm_button: 

# ---------------------------------------------------------------------------------------------
st.subheader('Supervised Learning Algorithm Recommendation')
st.write(
    """
Support Vector Machines (SVM) is a supervised learning algorithm used for both regression and 
classification tasks. In this case, we leveraged it for classification, where the goal was to predict whether the trading 
signal will be positive (+1) or negative (-1) based on the features derived from technical indicators and historical price data which represent 
the buy (+1) / sell (-1) recommendation.
    """
)

svm_testing_report, predictions_df, actual_returns_cum, strategy_returns_cum = ml_app.drive_machine_learning(selected_stock, start_date, end_date)
    
# Create a button to trigger analysis
if st.button("Get Recommendation", key="SVM"):
    
    # Display most recent trading signal prediction
    latest_signal_prediction = predictions_df['Predicted'].iloc[-1]
    latest_signal_predictionBS = "Sell" if latest_signal_prediction == -1 else "Buy" #Revised to convert to Buy/Sell
    st.write(f"Most Recent Trading Signal Prediction: {latest_signal_predictionBS}")
    
    # Display SVM testing report
    st.write("SVM Testing Report:")
    st.write(svm_testing_report)
    
    # Display returns report
    st.write("Returns Report:")
    st.write(f"Total Actual Returns: {actual_returns_cum:.2f}%")
    st.write(f"Total Strategy Returns: {strategy_returns_cum:.2f}%")

# -----------------------------------------------------------------------------------------------
# Trading Execution

st.subheader('Execute Trade using Alpacas')

# Set up Alpaca API

API_KEY = "PKLKK4Y1DQJ9TQ8JBRZS"
API_SECRET = "VwYnY5BDW2GPkRtCRhXebcasmocMFD2yecPYIGTH"
api = tradeapi.REST(API_KEY, API_SECRET, base_url='https://paper-api.alpaca.markets')  # Using paper trading URL

# Get input from user on how much to spend
# amounts = ['100','1,000','10,000','100,000']
# investment_amount = st.selectbox('How much do you want to invest (in USD)?', amounts, key="investment_amount")
# st.write(f"You've chosen : {investment_amount}.")

# Input parameters
ticker = selected_stock
quantity = st.number_input("Enter Quantity:", 1, key="share_number" )
action = st.radio("Select Action:", ["Buy", "Sell"])

if st.button("Execute Trade", key="execute_trade"):
    if action == "Buy":
        api.submit_order(
            symbol=ticker,
            qty=quantity,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
        st.success(f"Successfully bought {quantity} shares of {ticker}!")
    else:
        api.submit_order(
            symbol=ticker,
            qty=quantity,
            side='sell',
            type='market',
            time_in_force='gtc'
        )
        st.success(f"Successfully sold {quantity} shares of {ticker}!")

# Display account info (optional)
account = api.get_account()
st.write(f"Current Account Balance: ${account.cash}")
