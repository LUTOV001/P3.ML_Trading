# Libraries
import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
import yfinance as yf
from plotly import graph_objs as go


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

# List of Tickers
stocks = ['AAPL', 'MSFT','AMZN','GOOGL','META','IBM','NVDA', 'JPM','V','UNH']
selected_stock = st.selectbox('Select a stock ticker from the list:', stocks)

start_date = st.date_input("Start Date:", datetime.now() - timedelta(days=365))
end_date = st.date_input("End Date:")

# Add a "Get Historic Price Data" button
get_data_button = st.button("Get Historic Price Data")

# Pull data from Yahoo Finance and cache data
@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, start_date, end_date)
    data.reset_index(inplace=True)
    return data

# Execute data query when the button is pressed
if get_data_button:
    data = load_data(selected_stock)

    st.subheader('Historical Stock Data')
    st.write(data)

    def plot_raw_data():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open'))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_close'))
        fig.layout.update(title = "Historical Stock Data Plot", xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)

    plot_raw_data()

st.subheader('LSTM ML Model Recommendation')
st.write(
    """
LSTM (Long Short-Term Memory) is a type of recurrent neural network (RNN) machine learning model. 
LSTM networks are particularly well-suited for time series forecasting tasks due to their ability to 
capture sequential dependencies and patterns in the data.  Here we will use the LSTM ML Model to predict 
the future stock price selected and provide a buy / sell recommendation based on predicted stock price. 
    """
)

# Add a "Run LSTM ML Model" button
lstm_button = st.button("Get Recommendation")

# Run LSTM ML Model and provide buy / sell recommendation if button is pressed
# if lstm_button: 

# Get input from user on how much to spend
amounts = ['100','1,000','10,000','100,000']
investment_amount = st.selectbox('How much do you want to invest (in USD)?', amounts)


st.subheader('Execute Trade using Alpacas')

st.write("Selected Stock:", selected_stock)
st.write("Investment Amount: $", investment_amount)



# Add a "Execute Trade" button
execute_trade_button = st.button("Execute Trade")

# Execute trade through Alpaca when the button is pressed
# if execute_trade_button:
    # enter code to return remaining cash balance (Matt's code)
    # enter code to return report of open positions (Matt's code)
