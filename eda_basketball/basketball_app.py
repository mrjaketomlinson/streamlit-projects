import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Header & description
st.title('NBA Player Stats Explorer')
st.markdown("""
This app performs simple webscraping of NBA player stats!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [basketball-reference.com](https://www.basketball-reference.com)
""")

# Sidebar
st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,2020))))

# Web scrape NBA player stats
@st.cache
def load_data(year):
    url = f'https://www.basketball-reference.com/leagues/NBA_{str(year)}_per_game.html'
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    # Had to cast a type, otherwise would get ArrowTypeError
    playerstats['FG%'] = playerstats['FG%'].astype(float)
    playerstats['3P%'] = playerstats['3P%'].astype(float)
    playerstats['2P%'] = playerstats['2P%'].astype(float)
    playerstats['eFG%'] = playerstats['eFG%'].astype(float)
    playerstats['FT%'] = playerstats['FT%'].astype(float)
    return playerstats

playerstats = load_data(selected_year)

# Sidebar - team selection
sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - position selection
unique_position = ['C', 'PF', 'SF', 'PG', 'SG']
selected_position = st.sidebar.multiselect('Position', unique_position, unique_position)

# Filtering data
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_position))]

# Display DF
st.header('Display Player Stats of Selected Team(s)')
st.write(f'Data Dimension: {str(df_selected_team.shape[0])} rows and {str(df_selected_team.shape[1])} columns')
st.dataframe(df_selected_team)


# Allow CSV Download
def file_download(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode() # Strings <-> Bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href


st.markdown(file_download(df_selected_team), unsafe_allow_html=True)

# Heatmap
if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matric Heatmap')
    df_selected_team.to_csv('output.csv', index=False)
    df = pd.read_csv('output.csv')

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style('white'):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot(f)