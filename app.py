import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date, timedelta
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_percentage_error
import matplotlib.pyplot as plt

# Streamlit App Title
st.title("Indian Stock Investment Predictor with ARIMA Forecasting & Backtesting")

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
            # Prepare data for ARIMA model
            data['Return'] = data['Close'].pct_change()
            avg_daily_return = data['Return'].mean()
            std_dev = data['Return'].std()
            
            # ARIMA Model Training
            train_size = int(len(data) * 0.8)
            train, test = data['Close'][:train_size], data['Close'][train_size:]
            
            model = ARIMA(train, order=(5, 1, 0))  # ARIMA(5,1,0) as a default simple model
            model_fit = model.fit()
            
            # Forecasting
            forecast = model_fit.forecast(steps=len(test))
            
            # Calculate Backtest Error
            mape = mean_absolute_percentage_error(test, forecast)
            st.subheader("Backtest Performance")
            st.write(f"Mean Absolute Percentage Error (MAPE): {mape:.2%}")
            
            # Future Price Predictions
            future_forecast = model_fit.forecast(steps=365)
            one_day_price = future_forecast[0]
            one_month_price = future_forecast[29]
            one_year_price = future_forecast[-1]
            
            # Predict investment value
            def predict_investment(future_price):
                latest_price = data['Close'].iloc[-1]
                return (future_price / latest_price) * investment_amount
            
            one_day_value = predict_investment(one_day_price)
            one_month_value = predict_investment(one_month_price)
            one_year_value = predict_investment(one_year_price)
            
            # Display Predictions
            st.subheader("Investment Forecast")
            st.write(f"Expected Value in 1 Day: **INR {one_day_value:.2f}**")
            st.write(f"Expected Value in 1 Month: **INR {one_month_value:.2f}**")
            st.write(f"Expected Value in 1 Year: **INR {one_year_value:.2f}**")
            
            # Plot Backtest Results
            fig, ax = plt.subplots()
            ax.plot(test.index, test, label="Actual Price", color='blue')
            ax.plot(test.index, forecast, label="ARIMA Forecast", color='red', linestyle='dashed')
            ax.set_title("Backtesting: Actual vs Forecasted Prices")
            ax.legend()
            st.pyplot(fig)
        else:
            st.warning("No data available for the entered stock symbol. Please check the symbol and try again.")
    except Exception as e:
        st.error(f"Error fetching stock data: {e}")
