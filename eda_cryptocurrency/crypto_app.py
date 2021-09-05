# Imports
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import json
import time
from datetime import datetime, timedelta

# Page layout
st.set_page_config(layout='wide')

# Image Title and Description
st.image('crypto_logo.jpg', width = 500)
st.title('Cryptocurrency Price App')
st.markdown("""
This app retrieves cryptocurrency prices for the top 100 cryptocurrencies from the **CoinMarketCap**.
""")

# About
expander_bar = st.expander('About')
expander_bar.markdown("""
* **Python libraries:** base64, pandas, streamlit, matplotlib, BeautifulSoup, requests, json, time
* **Data source:** [CoinMarketCap](http://coinmarketcap.com).
* **Project Credit:** Adapted from [Chanin Nantasenamat (aka Data Professor)](https://www.youtube.com/watch?v=JwSS70SZdyM).
Made improvements to displaying the bar plot based on the number of coins present and gave the end user the ability to select all coins.
""")

# Page layout cont.
col1 = st.sidebar
col2, col3 = st.columns((2,1))

# Sidebar
col1.header('Input Options')

currency_price_unit = col1.selectbox('Select currency for price', ('USD', 'BTC', 'ETH'))

# Scrape CoinMarketCap
@st.cache
def load_crypto():
    cmc = requests.get('https://coinmarketcap.com')
    soup = BeautifulSoup(cmc.content, 'html.parser')
    data = soup.find('script', id='__NEXT_DATA__', type='application/json')
    
    coins = {}
    coin_data = json.loads(data.contents[0])
    listings = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']
    for i in listings:
      coins[str(i['id'])] = i['slug']

    coin_name = []
    coin_symbol = []
    market_cap = []
    percent_change_1h = []
    percent_change_24h = []
    percent_change_7d = []
    price = []
    volume_24h = []

    for i in listings:
      coin_name.append(i['slug'])
      coin_symbol.append(i['symbol'])
      price.append(i['quote'][currency_price_unit]['price'])
      percent_change_1h.append(i['quote'][currency_price_unit]['percentChange1h'])
      percent_change_24h.append(i['quote'][currency_price_unit]['percentChange24h'])
      percent_change_7d.append(i['quote'][currency_price_unit]['percentChange7d'])
      market_cap.append(i['quote'][currency_price_unit]['marketCap'])
      volume_24h.append(i['quote'][currency_price_unit]['volume24h'])

    df = pd.DataFrame(columns=['coin_name', 'coin_symbol', 'market_cap', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'price', 'volume_24h'])
    df['coin_name'] = coin_name
    df['coin_symbol'] = coin_symbol
    df['price'] = price
    df['percent_change_1h'] = percent_change_1h
    df['percent_change_24h'] = percent_change_24h
    df['percent_change_7d'] = percent_change_7d
    df['market_cap'] = market_cap
    df['volume_24h'] = volume_24h
    return df

df = load_crypto()

# Sidebar - Crypto selections
all = col1.checkbox('Select All')
sorted_coin = sorted(df['coin_symbol'])
if all:
    selected_coin = col1.multiselect('Cryptocurency', sorted_coin, sorted_coin)
else:
    selected_coin = col1.multiselect('Cryptocurency', sorted_coin)

df_selected_coin = df[(df['coin_symbol'].isin(selected_coin))]

# Sidebar - # coins to display
num_coin = col1.slider('Display Top N Coins', 1, 100, 100)
df_coins = df_selected_coin[:num_coin]

# Sidebar - % change timeframe
percent_timeframe = col1.selectbox('Percent change time frame', ('7d', '24hr', '1hr'))
percent_dict = {'7d': 'percent_change_7d', '24hr': 'percent_change_24hr', '1hr': 'percent_change_1hr'}
selected_percent_timeframe = percent_dict[percent_timeframe]

# Sidebar - sorting values
sort_values = col1.selectbox('Sort Values?', ('Yes', 'No'))

# Col2 - DF
col2.subheader('Price Data of Selected Cryptocurrency')
col2.write(f'Data Dimension: {df_selected_coin.shape[0]} rows and {df_selected_coin.shape[1]} columns')
col2.dataframe(df_coins)


# Allow CSV Download
def file_download(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode() # Strings <-> Bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="cryptocurrency.csv">Download CSV File</a>'
    return href


col2.markdown(file_download(df_coins), unsafe_allow_html=True)

# % Price change Table
col2.subheader('Table of % Price Change')
df_change = pd.concat([df_coins.coin_symbol, df_coins.percent_change_1h, df_coins.percent_change_24h, df_coins.percent_change_7d], axis=1)
df_change = df_change.set_index('coin_symbol')
df_change['positive_percent_change_1h'] = df_change['percent_change_1h'] > 0
df_change['positive_percent_change_24h'] = df_change['percent_change_24h'] > 0
df_change['positive_percent_change_7d'] = df_change['percent_change_7d'] > 0
col2.dataframe(df_change)

# Conditional creation of Bar plot (time frame)
col3.subheader('Bar plot of % Price Change')

# Format chart based on number of coins selected
topmargin = 1 #inches
bottommargin = .9 #inches
categorysize = 2 # inches
n = df_change.shape[0]
figheight = topmargin + bottommargin + (n+1)*categorysize

# Write the bar plot if it contains coins
if not df_change.empty:
    if percent_timeframe == '7d':
        if sort_values == 'Yes':
            df_change = df_change.sort_values(by=['percent_change_7d'])
        col3.write('*7 days period*')
        plt.figure(figsize=(5,figheight))
        plt.subplots_adjust(top=topmargin, bottom=bottommargin)
        df_change['percent_change_7d'].plot(kind='barh', color=df_change.positive_percent_change_7d.map({True: 'g', False: 'r'}))
        col3.pyplot(plt)
    elif percent_timeframe == '24h':
        if sort_values == 'Yes':
            df_change = df_change.sort_values(by=['percent_change_24h'])
        col3.write('*24 hour period*')
        plt.figure(figsize=(5,figheight))
        plt.subplots_adjust(top=topmargin, bottom=bottommargin)
        df_change['percent_change_24h'].plot(kind='barh', color=df_change.positive_percent_change_24h.map({True: 'g', False: 'r'}))
        col3.pyplot(plt)
    else:
        if sort_values == 'Yes':
            df_change = df_change.sort_values(by=['percent_change_1h'])
        col3.write('*1 hour period*')
        plt.figure(figsize=(5,figheight))
        plt.subplots_adjust(top=topmargin, bottom=bottommargin)
        df_change['percent_change_1h'].plot(kind='barh', color=df_change.positive_percent_change_1h.map({True: 'g', False: 'r'}))
        col3.pyplot(plt)
else:
    col3.write('Pick some coins to see there percent change!')