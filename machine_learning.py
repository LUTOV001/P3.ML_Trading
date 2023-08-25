import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import tickerdata_app as app
import hvplot
import warnings
import pathlib as Path
import xgboost as xgb
import talib as ta
from talib import MA_Type
from pandas.tseries.offsets import DateOffset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn import svm
from sklearn.metrics import classification_report

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
#warnings.filterwarnings("ignore", category=SettingWithCopyWarning)

# Disable SettingWithCopyWarning
pd.options.mode.chained_assignment = None

# --------------------------------------------------------------------------------------------

#1. Price Data


# Create a DataFrame with selected price data

def create_df(stock_data, selected_ticker, start_date, end_date):
    stock_df = pd.DataFrame()
    stock_df['High'] = stock_data['High']
    stock_df['Low'] = stock_data['Low']
    stock_df['Open'] = stock_data['Open']
    stock_df['Close'] = stock_data['Close']
    return stock_df


#-------------------------------------------------------------

#2. Technical Indicators

# Create Method

def create_data_df(data_df):  # Add data_df as an argument
    # Define the technical indicators
    sma_periods = [5, 10, 20, 50, 100, 200]
    rsi_periods = [14]
    macd_periods = [(12, 26)]

    for period in sma_periods:
        sma_column_name = f"SMA {period}"
        data_df[sma_column_name] = ta.SMA(data_df['Close'], timeperiod=period)

    for period in rsi_periods:
        rsi_column_name = f"RSI {period}"
        data_df[rsi_column_name] = ta.RSI(data_df['Close'], timeperiod=period)

    for short_period, long_period in macd_periods:
        macd_column_name = f"MACD {short_period}-{long_period}"
        macd_values = ta.MACD(data_df['Close'], fastperiod=short_period, slowperiod=long_period, signalperiod=9)
        data_df[macd_column_name] = macd_values[0]  # Extract MACD line

    # Calculate price change
    data_df['Price Change -10d'] = (data_df['Close'] - data_df['Close'].shift(10)) / data_df['Close'] * 100

    # Calculate actual daily returns
    data_df['Actual Returns'] = data_df['Close'].pct_change()

    return data_df


# Fetch P/E Ratio for each ETF
# for symbol in etf_symbols:
#     ticker = yf.Ticker(symbol)
#     pe_ratio = ticker.info.get('trailingPE')
#     data_df.loc[data_df['Symbol'] == symbol, 'P/E Ratio'] = pe_ratio
    
#---------------------------------------------------------------------------------

# Clean data
def make_clean_data_df(data_df):
    # Clean data of 0 and NA
    data_df = data_df.replace(0, pd.NA)
    # Drop NA
    data_df = data_df.dropna()
    na_counts = data_df.isna().sum()
    return data_df


#------------------------------------------------------------------------------------

# Generate signals

def generate_signal_price(clean_data_df):
    conditions = [
        (clean_data_df['Price Change %-10d'].to_numpy() > 0),
        (clean_data_df['Price Change %-10d'].to_numpy() < 0)
    ]

    choices = [1, -1]

    clean_data_df['Signal'] = np.select(conditions, choices, default=0)
    return clean_data_df['Signal']


# ------------------------------------------------------------------------------------------

def prepare_training_testing_data(clean_data_df):
    # Create Training and Testing Datasets
    X = clean_data_df.drop(['Symbol', 'Signal', 'Price Change %-10d'], axis=1)

    # Define the target set y 
    y = clean_data_df['Signal']

    # Select the start of the training period
    training_begin = X.index.min()

    # Calculate the index for the training data end (70% of the dataset)
    training_data_length = int(len(X) * 0.7)
    training_end_index = X.index[training_data_length]

    # Convert the index to a datetime format
    training_end = X.index.to_series().loc[training_end_index]

    # Generate the X_train and y_train DataFrames
    X_train = X.loc[training_begin:training_end]
    y_train = y.loc[training_begin:training_end]
    X_test = X.loc[training_end:]
    y_test = y.loc[training_end:]

    # Create a StandardScaler instance
    scaler = StandardScaler()

    # Apply the scaler model to fit the X-train data
    X_scaler = scaler.fit(X_train)

    # Transform the X_train and X_test DataFrames using the X_scaler
    X_train_scaled = X_scaler.transform(X_train)
    X_test_scaled = X_scaler.transform(X_test)

    return X_train_scaled, y_train, X_test_scaled, y_test



#----------------------------------------------------------------------------------------------------

def get_classification_report (X_train_scaled, y_train, X_test_scaled, y_test):
    # From SVM, instantiate SVC classifier model instance
    svm_model = svm.SVC()

    # Fit the model to the data using the training data
    svm_pred = svm_model.fit(X_train_scaled, y_train)

    # Use the testing data to make the model predictions
    training_signal_predictions = svm_model.predict(X_test_scaled)

    # Use a classification report to evaluate the model using the predictions and testing data
    svm_testing_report = classification_report(y_test, training_signal_predictions)
    
    return svm_testing_report, training_signal_predictions


# -------------------------------------------------------------------------------------------------------

def make_predictions_df(X_test, training_signal_predictions, clean_data_df):
    # Create a predictions DataFrame
    predictions_df = pd.DataFrame(index=X_test.index)

    # Add the SVM model predictions to the DataFrame
    predictions_df['Predicted'] = training_signal_predictions

    # Add the actual returns to the DataFrame
    predictions_df['Actual Returns'] = clean_data_df["Actual Returns"] 

    # Add the strategy returns to the DataFrame
    predictions_df['Strategy Returns'] = clean_data_df["Actual Returns"] * predictions_df['Predicted']
    
    return predictions_df 


# ------------------------------------------------------------------------------------------------------------

# Plot the actual returns versus the strategy returns

def returns_report(predictions_df):
    (1 + predictions_df[['Actual Returns','Strategy Returns']]).cumprod().plot(title='SVC Classifier Model')
    actual_returns_cum = 100*((1 + predictions_df['Actual Returns']).cumprod().iloc[-1] - 1)
    #print(f"Total Actual Returns: {actual_returns_cum:.2f}%")
    strategy_returns_cum = 100*((1 + predictions_df['Strategy Returns']).cumprod().iloc[-1] - 1)
    #print(f"Total Strategy Returns: {strategy_returns_cum:.2f}%")
    return actual_returns_cum, strategy_returns_cum



def drive_machine_learning (selected_ticker, start_date, end_date):
    
#     #1. Price Data

#     selected_ticker = app.selected_stock
#     start_date = app.start_date
#     end_date = app.end_date

    # Convert dates to string format
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    stock_data = yf.download(selected_ticker, start=start_date_str, end=end_date_str)
    
    stock_df = create_df(stock_data, selected_ticker, start_date, end_date)

    data_df = create_data_df(stock_df)  # Call the function with your DataFrame
    
    clean_data_df = make_clean_data_df(data_df)
  
    # Call the function on your DataFrame
    generate_signal_price(clean_data_df)

    # Fill NaN values with 0 and convert the signal to int
    clean_data_df['Signal'] = clean_data_df['Signal'].fillna(0).astype(int)
    
    X_train_scaled, y_train, X_test_scaled, y_test = prepare_training_testing_data(clean_data_df)

    svm_testing_report, training_signal_predictions = get_classification_report (X_train_scaled, y_train, X_test_scaled, y_test)

    predictions_df = make_predictions_df(X_test, training_signal_predictions, clean_data_df)

    actual_returns_cum, strategy_returns_cum = returns_report(predictions_df)
    
    return svm_testing_report, predictions_df, actual_returns_cum, strategy_returns_cum

