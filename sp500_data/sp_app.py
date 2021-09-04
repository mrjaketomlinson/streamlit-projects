# Imports
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta

# Title and Description
st.title('S&P 500 App')
st.markdown("""
This app retrieves the list of the **S&P 500** (from Wikipedia).
* **Python libraries:** base64, pandas, streamlit, matplotlib, yfinance
* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies)
""")
st.sidebar.header('User Input Features')


@st.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header=0)
    df = html[0]
    return df


df = load_data()
sector = df.groupby('GICS Sector')

# Sidebar - Sector Selection
sorted_sector_unique = sorted(df['GICS Sector'].unique())
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique)

# Filtering data
df_selected_sector = df[(df['GICS Sector'].isin(selected_sector))]

# Display companies in sector(s)
st.header('Display Companies in Selected Sector')
st.write(f'Data Dimension: {str(df_selected_sector.shape[0])} rows and {str(df_selected_sector.shape[1])} columns')
st.dataframe(df_selected_sector)


# Allow CSV Download
def file_download(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode() # Strings <-> Bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href


st.markdown(file_download(df_selected_sector), unsafe_allow_html=True)


# Sidebar - Ticker Selection
def get_ticker_data(*args):
    symbols = [x for x in args if x != '']
    chart_data = pd.DataFrame(columns=symbols)
    today = datetime.strftime(datetime.today(), '%Y-%m-%d')
    one_year_ago = datetime.strftime(datetime.today()-timedelta(days=365), '%Y-%m-%d')
    for i in symbols:
        tickerData = yf.Ticker(i)
        tickerDf = tickerData.history(period='1d', start=one_year_ago, end=today)
        chart_data[i] = tickerDf.Close
    st.line_chart(chart_data)

with st.sidebar.form('ticker_form'):
    st.write('Choose up to 3 stocks to compare')
    symbols = [''] + list(df_selected_sector.Symbol)
    first_ticker = st.selectbox('First Ticker', symbols)
    second_ticker = st.selectbox('Second Ticker', symbols)
    third_ticker = st.selectbox('Third Ticker', symbols)

    submitted = st.form_submit_button("Submit")

if submitted:
    get_ticker_data(first_ticker, second_ticker, third_ticker)
