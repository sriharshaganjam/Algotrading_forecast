import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date, timedelta

# Streamlit App Title
st.title("Indian Stock Investment Predictor")

# User Input: Stock Symbol & Investment Amount
stock_symbol = st.text_input("Enter the Indian Stock Symbol (e.g., RELIANCE.NS):")
investment_amount = st.number_input("Investment Amount (INR):", min_value=1000, step=500)

if stock_symbol and investment_amount:
    try:
        # Fetch historical data (1 year)
        end_date = date.today()
        start_date = end_date - timedelta(days=365)
        data = yf.download(stock_symbol, start=start_date, end=end_date)
        
        if not data.empty:
            # Calculate daily return
            data['Return'] = data['Close'].pct_change()
            avg_daily_return = data['Return'].mean()
            std_dev = data['Return'].std()
            
            # Predict future values using a simple growth model
            def predict_future_value(days):
                return investment_amount * (1 + avg_daily_return) ** days
            
            one_day_value = predict_future_value(1)
            one_month_value = predict_future_value(30)
            one_year_value = predict_future_value(365)
            
            # Display Predictions
            st.subheader("Investment Forecast")
            st.write(f"Expected Value in 1 Day: **INR {one_day_value:.2f}**")
            st.write(f"Expected Value in 1 Month: **INR {one_month_value:.2f}**")
            st.write(f"Expected Value in 1 Year: **INR {one_year_value:.2f}**")
        else:
            st.warning("No data available for the entered stock symbol. Please check the symbol and try again.")
    except Exception as e:
        st.error(f"Error fetching stock data: {e}")
