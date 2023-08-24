{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "6f849157-9b7a-4cc5-9a50-6efb8dce5650",
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st\n",
    "import pandas as pd\n",
    "from datetime import datetime, timedelta\n",
    "import yfinance as yf"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "5119fa7b-789c-4b9e-b76b-7b7a59027fc8",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Read stock tickers from the CSV file\n",
    "tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'IBM', 'NVDA', 'JPM', 'V', 'UNH']\n",
    "tickers_df = pd.DataFrame(tickers)\n",
    "#tickers_df = (pd.read_csv('Resources\\stock_tickers.csv', header=None)\n",
    "Nasdaq_NYSE_10 = tickers_df[0].tolist()\n",
    "\n",
    "st.title(\"Stock Ticker Data Analysis\")\n",
    "\n",
    "# User input using Streamlit components\n",
    "selected_ticker = st.selectbox(\"Select a stock ticker from the list:\", Nasdaq_NYSE_10)\n",
    "start_date = st.date_input(\"Start Date:\", datetime.now() - timedelta(days=365))\n",
    "end_date = st.date_input(\"End Date:\")\n",
    "\n",
    "# Add a \"Get Historic Price Data\" button\n",
    "get_data_button = st.button(\"Get Historic Price Data\")\n",
    "\n",
    "# Convert dates to string format\n",
    "start_date_str = start_date.strftime('%Y-%m-%d')\n",
    "end_date_str = end_date.strftime('%Y-%m-%d')\n",
    "\n",
    "# Execute data query when the button is pressed\n",
    "if get_data_button:\n",
    "    # Fetch historical price data using yfinance\n",
    "    stock_data = yf.download(selected_ticker, start=start_date_str, end=end_date_str)\n",
    "\n",
    "    # Create a DataFrame with selected price data\n",
    "    stock_df = pd.DataFrame()\n",
    "    stock_df['High'] = stock_data['High']\n",
    "    stock_df['Low'] = stock_data['Low']\n",
    "    stock_df['Open'] = stock_data['Open']\n",
    "    stock_df['Close'] = stock_data['Close']\n",
    "\n",
    "    # Display the DataFrame\n",
    "    st.write(f\"Historical price data for {selected_ticker} from {start_date_str} to {end_date_str}:\")\n",
    "    st.dataframe(stock_df)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "fe64a419-eb55-4387-bb70-5a88f1a2cfd2",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python (dev)",
   "language": "python",
   "name": "dev"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
