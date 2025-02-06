import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import date, timedelta

# Define available trading strategies
strategies = ["Moving Average Crossover", "Ichimoku Cloud", "Parabolic SAR"]

# List of Indian Sensex stock symbols (Example: Add more as needed)
sensex_symbols = {
    "Reliance Industries": "RELIANCE.NS",
    "Tata Consultancy Services": "TCS.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "Infosys": "INFY.NS",
    "ICICI Bank": "ICICIBANK.NS"
}

st.title("AlgoTrading App for Indian Markets")

# User inputs
stock_choice = st.selectbox("Choose a stock:", list(sensex_symbols.keys()))
investment_amount = st.number_input("Investment Amount (INR):", min_value=1000, step=500)
strategy = st.selectbox("Select Trading Strategy:", strategies)

# Fetch historical data (12 months)
end_date = date.today()
start_date = end_date - timedelta(days=365)
stock_symbol = sensex_symbols[stock_choice]
data = yf.download(stock_symbol, start=start_date, end=end_date)

if not data.empty:
    # Plot historical stock price
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Candlestick Chart'
    ))
    fig.update_layout(title=f"Historical Price Chart of {stock_choice} (INR)", xaxis_title="Date", yaxis_title="Price (INR)")
    st.plotly_chart(fig)
else:
    st.warning("No data available for the selected stock.")

# Forecasting Next Trading Day Opening Price
last_close = data['Close'].iloc[-1]
forecasted_open = last_close * np.random.uniform(0.98, 1.02)  # Adding slight variation for demo
st.write(f"Forecasted Opening Price for Next Trading Day: INR {forecasted_open:.2f}")

# Trading Decision: Buy or Sell
if forecasted_open > last_close:
    st.success("Recommendation: BUY")
    expected_return = (forecasted_open - last_close) / last_close * investment_amount
    st.write(f"Expected Return by End of Day: INR {expected_return:.2f}")
else:
    st.error("Recommendation: SELL")
