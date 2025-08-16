import plotly.graph_objects as go
import numpy as np
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import yaml
import streamlit as st
from utils import *
import sys
import datetime
from time import strptime

sys.path.insert(0, "..")
local_css("style.css")

st.title("💫 *Everything everywhere all at once*")
st.markdown("""
    This visualization brings together some of the main metrics I’ve collected,
    wrapping them up in one clear and handy view.
    """)
st.markdown("""
    - **color**: size is..
    - **size**: size is..
    """)

st.sidebar.subheader('🔍 How to read')

st.sidebar.markdown("""
    **Color legend** – Colors below encodes different emotions (as introduced in the main page).
    """)
st.sidebar.markdown("""
    <span class='happy_square'></span> Happy <br>
    <span class='loved_square'></span> Loved <br>
    <span class='confident_square'></span> Confident <br>
    <span class='playful_square'></span> Playful <br>
    <span class='embarassed_square'></span> Embarassed <br>
    <span class='angry_square'></span> Angry <br>
    <span class='scared_square'></span> Scared <br>
    <span class='sad_square'></span> Sad <br>
    """, unsafe_allow_html=True
)

# Add to your Notes page
st.sidebar.markdown("**Shape legend** –")
st.sidebar.markdown("""
    <span class='weekend-circle'></span>Weekend day <br>
    <span class='octagon'></span>Watched a movie <br>
    <span class='journaling-diamond-star'></span>Journaling <br>
    <span class='out-milan-line'></span>Out of Milan <br>
    """, unsafe_allow_html=True)

st.sidebar.markdown("""<hr style="height:2px; border:none; color:#333; background-color:#333;"/>""", unsafe_allow_html=True)
st.sidebar.subheader('📙 References')
st.sidebar.markdown("""
    *«Every new discovery is just a reminder that we're all small and stupid.»*
    """)
url_video = "https://www.youtube.com/watch?v=UXar2tNdG34"
st.sidebar.video(url_video)

conn = st.connection("gsheets", type=GSheetsConnection)
@st.cache_data
def load_data(worksheet_name, n_cols, n_rows):
    df = conn.read(
        worksheet=worksheet_name,
        ttl="10m",
        usecols=range(n_cols),
        nrows=n_rows
    )
    return df

# config
with open("config.yml", 'r') as f:
    cfg = yaml.safe_load(f)

dict_emotion_id = cfg['map_emotion_id']
dict_emotion_color = cfg['map_emotion_color']
dict_months = cfg['map_months']
config_modebar = {'displayModeBar': False}

df_emotion_to_melt = st.session_state['df_emotion'].reset_index()
df_emotion = pd.melt(df_emotion_to_melt, id_vars=['id_day'], var_name='month_name', value_name='emotion')
df_emotion = df_emotion.rename(columns={'id_day': 'day'})
df_emotion['color'] = df_emotion.emotion.map(dict_emotion_color)
df_emotion['month'] = df_emotion.month_name.map(dict_months)
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
dict_weekend_col = {el: '#f5fc12' if el in ["Saturday", "Sunday"] else '#ffffff' for el in days}

df_emotion = df_emotion[df_emotion.emotion!='Missing']
df_emotion['date'] = [datetime.datetime(year=2024, month=el[0], day=el[1]) for el in zip(df_emotion.month, df_emotion.day)]
df_emotion['weekday_id'] = df_emotion['date'].apply(lambda x: x.weekday()+1)
df_emotion['weekday'] = df_emotion['date'].apply(lambda x: days[x.weekday()])
df_emotion['weekend_color'] = df_emotion.weekday.map(dict_weekend_col)

df_intensity_to_melt = st.session_state['df_intensity'].reset_index()
df_intensity = pd.melt(df_intensity_to_melt, id_vars=['id_day'], var_name='month_name', value_name='intensity')
df_intensity = df_intensity.rename(columns={'id_day': 'day'})
df_intensity['month'] = df_intensity.month_name.map(dict_months)
df_intensity = df_intensity.drop('month_name', axis=1)
dict_intensity_size = {
    '0': 15,
    'Missing': 15,
    ':((': 30,
    ':(': 22,
    ':|': 15,
    ':)': 22,
    ':))': 30
}

df_intensity['size'] = df_intensity.intensity.map(dict_intensity_size)
df_plot = df_emotion.merge(df_intensity, on=['day', 'month'], how='left')

df_movies = st.session_state['df_movies'].drop('jouornaling_date', axis=1)
df_movies['flag_movie'] = 1
df_movies['movie_date'] = pd.to_datetime(df_movies['movie_date'], format='%d/%m/%Y')
df_movies['day'] = df_movies['movie_date'].dt.day
df_movies['month'] = df_movies['movie_date'].dt.month
df_plot = df_plot.merge(df_movies.drop('movie_date', axis=1), on=['day', 'month'], how='left')

df_jou = st.session_state['df_movies'][['jouornaling_date']]
df_jou = df_jou.rename(columns={'jouornaling_date': 'journaling_date'})
df_jou['flag_jou'] = 1
df_jou['journaling_date'] = pd.to_datetime(df_jou['journaling_date'], format='%d/%m/%Y')
df_jou['day'] = df_jou['journaling_date'].dt.day
df_jou['month'] = df_jou['journaling_date'].dt.month
df_plot = df_plot.merge(df_jou.drop('journaling_date', axis=1), on=['day', 'month'], how='left')

df_place_to_melt = st.session_state.df_place
df_place = pd.melt(df_place_to_melt, id_vars=['day/month'], var_name='month_name', value_name='place')
df_place = df_place.rename(columns={'day/month': 'day'})
df_place['month'] = df_place.month_name.map(dict_months)
df_place = df_place.drop('month_name', axis=1)
df_place = df_place[df_place.place!='Missing']
df_place['is_milano'] = (df_place['place'] == 'Milano').astype(int)
df_plot = df_plot.merge(df_place, on=['day', 'month'], how='left')

fig = go.Figure()

# Scatter plot: main grid of dots
# Add actual data points (optional)

fig.add_trace(go.Scatter(
    x=df_plot['month'],
    y=df_plot['day'],
    mode='markers',
    marker=dict(
        color=df_plot['color'],
        size=df_plot['size'],
        showscale=False,
        line=dict(
            width=3,  # Border width
            color=df_plot['weekend_color']  # Border color
            )
    ),
    text=df_plot['date'].astype(str),
    customdata=df_plot[['intensity', 'emotion', 'weekday']],
    hovertemplate=(
        'Date: %{text}<br>' +  # Use 'text' for the date
        'Day of the week: %{customdata[2]}<br>' +  # Use 'text' for the date
        'Emotion: %{customdata[1]}<br>' +  # Assuming you have an 'emotion' column
        'Intensity: %{customdata[0]}<br>' +  # Use 'customdata' for intensity
        '<extra></extra>'
    ),
    showlegend=False
))

fig.add_trace(go.Scatter(
    x=[None],  # Dummy data, doesn't appear in the plot
    y=[None],  # Dummy data, doesn't appear in the plot
    mode='markers',
    marker=dict(
        color='white',  # Set the color to yellow for weekends
        size=10,  # Size for legend
        line=dict(
            width=3,  # Border width
            color="#f5fc12"  # Border color
        )
    ),
    name='Weekend day',
    showlegend=True
))

# Additional scatter plot with different shape
df_movies = df_plot[df_plot.flag_movie==1]
fig.add_trace(go.Scatter(
    x=df_movies['month'],
    y=df_movies['day'],
    mode='markers',
    marker=dict(
        color='black',  # Random color for additional points
        size=26,  # Fixed size for additional points
        symbol='octagon-open',  # Different shape
    ),
    name='Watched a movie',
    text=df_movies['movie_title'],
    hovertemplate=('Movie: %{text}<br>')
))

df_jou = df_plot[df_plot.flag_jou==1]
fig.add_trace(go.Scatter(
    x=df_jou['month'],
    y=df_jou['day'],
    mode='markers',
    marker=dict(
        color='black',  # Random color for additional points
        size=12,  # Fixed size for additional points
        symbol='star-diamond-open',  # Different shape
    ),
    name='Journaling',
    hovertemplate=('Journaling'),
))

df_milano = df_plot[df_plot.is_milano==0]
fig.add_trace(go.Scatter(
    x=df_milano['month'],
    y=df_milano['day'],
    mode='markers',
    marker=dict(
        color='black',  # Random color for additional points
        size=10,  # Fixed size for additional points
        symbol='line-ne-open',  # Different shape
    ),
    name='Out of Milan',
    text=df_milano['place'],
    hovertemplate=('Location: %{text}<br>'),
))

# Update layout with reversed axes
fig.update_layout(
    width=800,
    height=1200,
    xaxis=dict(
        tickvals=np.arange(1, 13),
        ticktext=['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'],
        showgrid=True,
        tickangle=0,
        side='top'
    ),
    yaxis=dict(
        zeroline=False,
        tickvals=np.arange(1, 32),
        showgrid=True,
        autorange="reversed"
    ),
    template="simple_white",
    legend=dict(title="Legend"),
    margin=dict(t=50),
)
fig.update_layout(legend= {'itemsizing': 'trace'})

# Show the plot
st.plotly_chart(fig, config=config_modebar, use_container_width=False)