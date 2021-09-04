import yfinance as yf
import streamlit as st
import pandas as pd

# Start Streamlit App
st.write("""
# Simple Stock Price App

Shown are the stock **closing price** and **volume** of Google.

""")

# Get Google Stock Data
tickerSymbol = 'GOOGL'
tickerData = yf.Ticker(tickerSymbol)
tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2020-5-31')
# Available DF options: Open, High, Low, Close, Volume, Dividends, Stock splits

# Create Line Chart using Google Stock Data
st.write("""
## Closing Price
""")
st.line_chart(tickerDf.Close)
st.write("""
## Volume
""")
st.line_chart(tickerDf.Volume)