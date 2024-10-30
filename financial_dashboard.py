import streamlit as st
import yfinance as yf
from prophet import Prophet
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob
from datetime import datetime, timedelta

st.title("Financial Analysis & Prediction Dashboard")
st.sidebar.header("User Input")

# User Input: Stock Symbol and Date Range
stock_symbol = st.sidebar.text_input("Enter Stock Symbol", "AAPL")
start_date = st.sidebar.date_input("Start Date", datetime.today() - timedelta(days=365))
end_date = st.sidebar.date_input("End Date", datetime.today())

@st.cache_data
def fetch_stock_data(symbol, start, end):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(start=start, end=end)
        data.reset_index(inplace=True)
        # Ensure 'Date' column is timezone-naive
        data['Date'] = pd.to_datetime(data['Date']).dt.tz_localize(None)
        return data
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

try:
    stock_data = fetch_stock_data(stock_symbol, start_date, end_date)
    
    if stock_data is not None and not stock_data.empty:
        st.subheader(f"Stock Data for {stock_symbol}")
        st.write(stock_data.tail())

        fig2 = plt.figure(figsize=(10, 6))
        plt.plot(stock_data["Date"], stock_data["Close"], label='Stock Price')
        plt.legend()
        st.pyplot(fig2)
        plt.close()

        # Prophet Forecasting
        def forecast_prices(data):
            df = data[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})
            model = Prophet()
            model.fit(df)
            future = model.make_future_dataframe(periods=30)
            forecast = model.predict(future)
            return forecast

        st.subheader("Stock Price Forecast")
        forecast = forecast_prices(stock_data)

        fig1 = plt.figure(figsize=(10, 6))
        plt.plot(forecast['ds'], forecast['yhat'], label='Forecast')
        plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], alpha=0.3)
        plt.legend()
        st.pyplot(fig1)
        plt.close()

        # Portfolio Analysis
        investment_amount = st.sidebar.number_input("Investment Amount ($)", value=10000)
        returns = stock_data['Close'].pct_change().dropna()
        portfolio_return = (1 + returns).cumprod() * investment_amount

        st.subheader("Simulated Portfolio Growth")
        fig3 = plt.figure(figsize=(10, 6))
        plt.plot(portfolio_return, label='Portfolio Value')
        plt.legend()
        st.pyplot(fig3)
        plt.close()

        # Sentiment Analysis
        news_text = st.sidebar.text_area("Enter News Headline for Sentiment", "Apple reports record earnings.")
        sentiment = TextBlob(news_text).sentiment.polarity
        st.subheader("Sentiment Analysis Result")
        if sentiment > 0:
            st.success(f"Positive Sentiment: {sentiment:.2f}")
        elif sentiment < 0:
            st.error(f"Negative Sentiment: {sentiment:.2f}")
        else:
            st.warning("Neutral Sentiment")

        # Monte Carlo Simulation
        num_simulations = st.sidebar.slider("Number of Simulations", 100, 1000, 500)

        def monte_carlo_simulation(data, simulations):
            daily_return = data['Close'].pct_change().mean()
            daily_volatility = data['Close'].pct_change().std()
            results = []

            for _ in range(simulations):
                simulated_price = [data['Close'].iloc[-1]]
                for _ in range(30):
                    next_price = simulated_price[-1] * (1 + np.random.normal(daily_return, daily_volatility))
                    simulated_price.append(next_price)
                results.append(simulated_price[-1])

            return results

        simulation_results = monte_carlo_simulation(stock_data, num_simulations)
        future_value = np.mean(simulation_results) * (investment_amount / stock_data['Close'].iloc[-1])
        st.subheader("Monte Carlo Simulation Result")
        st.write(f"Expected Portfolio Value after 30 days: ${future_value:.2f}")

    else:
        st.error("No data available for the selected stock symbol and date range.")

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.info("Please check the stock symbol and try again.")

st.write("Thank you for using the Financial Dashboard!")
