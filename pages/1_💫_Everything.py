# Standard library imports
import datetime
import os
import sys
from collections import Counter

# Third-party imports
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import yaml
from streamlit_gsheets import GSheetsConnection

# Local imports (after sys.path modification)
# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils import local_css

# Loads and applies style.css
local_css("style.css")

# CONFIG
PAGE_TITLE = "💫 *Everything everywhere all at once*"
WORKSHEET_NAME = "100happydays"
N_COLS = 6
N_ROWS = 100
CACHE_TTL = "10m"
config_modebar = {'displayModeBar': False}

with open("config.yml", 'r') as f:
    cfg = yaml.safe_load(f)
dict_emotion_id = cfg['map_emotion_id']
dict_emotion_color = cfg['map_emotion_color']
dict_months = cfg['map_months']
journaling_dates = cfg['journaling_dates']

st.title(PAGE_TITLE)
col1, _ = st.columns([3, 1], gap='large')
with col1:
    st.markdown("""
        This visualization pulls together almost all the features I tracked, 
        wrapping them up in a unique and handy view. <br>
        To make it easier to read, the chart follows the pixel view format in the main page –just rotated 90 degrees 
        for better visibility. <br>
        Each bubble sits at the crossing of a day (vertical axis) and a month (horizontal axis). 
        As the sidebar legend shows, the color captures the day’s emotion, while the size reflects its intensity.
        On top of that, I added four extra details, marked with special symbols (check the legend on the top left): weekends, 
        days I was away from Milan, when I journaled, and when I watched a movie.
        <br>
        <br>
    """, unsafe_allow_html=True)

#### SIDEBAR -START

# Legend
st.sidebar.subheader('🔍 How to read')

st.sidebar.markdown("""
    **Color legend** – Colors below encode different emotions (as introduced in the main page)
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
    """, unsafe_allow_html=True)

st.sidebar.markdown("**Size legend** – The bubble size refers to three possible feeling intensity levels")
st.sidebar.markdown("""
<div style="margin: 5px 0;"><span class='intensity-small'></span>:| <span style='font-size:0.9em; font-style:italic; color:#666;'> </span></div>
<div style="margin: 5px 0;"><span class='intensity-medium'></span>:) or :( <span style='font-size:0.9em; font-style:italic; color:#666;'>–depending on whether the feeling is already positive or negative</span></div>
<div style="margin: 5px 0;"><span class='intensity-large'></span>:)) or :(( <span style='font-size:0.9em; font-style:italic; color:#666;'>–depending on whether the feeling is already positive or negative</span></div>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("""<hr style="height:2px; border:none; color:#333; background-color:#333;"/>""", unsafe_allow_html=True)
st.sidebar.subheader('📙 References')
url_video = "https://www.youtube.com/watch?v=UXar2tNdG34"
st.sidebar.video(url_video)
st.sidebar.markdown("""
    <span style="font-size:13px; font-style:italic;">
    «Every new discovery is just a reminder that we're all small and stupid.»
    Everything Everywhere All at Once (2022)
    </span>
""", unsafe_allow_html=True)
# st.sidebar.caption("Everything Everywhere All at Once (2022)")

#### SIDEBAR -END

# DATA

conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data
def load_data(worksheet_name, n_cols, n_rows, cache_ttl):
    try:
        df = conn.read(
            worksheet=worksheet_name,
            ttl=cache_ttl,
            usecols=range(n_cols),
            nrows=n_rows
        )
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Dataframe validation (val after loading session state data)
if 'df_emotion' not in st.session_state:
    st.error("df_emotion not found in session state. Please load data first.")
    st.stop()

if 'df_intensity' not in st.session_state:
    st.error("df_intensity not found in session state. Please load data first.")
    st.stop()

if 'df_movies' not in st.session_state:
    st.error("df_movies not found in session state. Please load data first.")
    st.stop()

if 'df_place' not in st.session_state:
    st.error("df_place not found in session state. Please load data first.")
    st.stop()


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

df_movies = st.session_state['df_movies'][['movie_date', 'movie_title']]
df_movies['flag_movie'] = 1
df_movies['movie_date'] = pd.to_datetime(df_movies['movie_date'], format='%d/%m/%Y')
df_movies['day'] = df_movies['movie_date'].dt.day
df_movies['month'] = df_movies['movie_date'].dt.month
df_plot = df_plot.merge(df_movies.drop('movie_date', axis=1), on=['day', 'month'], how='left')

df_jou = pd.DataFrame({'dates': journaling_dates.split()})
df_jou = df_jou.rename(columns={'dates': 'journaling_date'})
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


# CHART
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
        'Date=%{text}<br>' +  # Use 'text' for the date
        'Day of the week=%{customdata[2]}<br>' +  # Use 'text' for the date
        'Emotion=%{customdata[1]}<br>' +  # Assuming you have an 'emotion' column
        'Intensity=%{customdata[0]}<br>' +  # Use 'customdata' for intensity
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
        size=14,  # Fixed size for additional points
        symbol='star-diamond-open',  # Different shape
    ),
    name='Watched a movie',
    text=df_movies['movie_title'],
    hovertemplate=('Movie=%{text}<br>')
))

df_jou = df_plot[df_plot.flag_jou==1]
fig.add_trace(go.Scatter(
    x=df_jou['month'],
    y=df_jou['day'],
    mode='markers',
    marker=dict(
        color='black',  # Random color for additional points
        size=28,  # Fixed size for additional points
        symbol='octagon-open',  # Different shape
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
        size=14,  # Fixed size for additional points
        symbol='line-ne-open',  # Different shape
    ),
    name='Out of Milan',
    text=df_milano['place'],
    hovertemplate=('Place=%{text}<br>'),
))
fig.add_trace(
    go.Scatter(
        y=[None], mode='markers',
        marker=dict(opacity=0, color='white'),
        name='<span style="font-size:14px"><b>Features</b></span>',
        showlegend=True,
        hoverinfo='skip',
    ))
fig.data = (fig.data[-1],) + fig.data[:-1]

# Update layout with reversed axes
fig.update_layout(
    width=800,
    height=1200,
    xaxis=dict(
        tickvals=np.arange(1, 13),
        ticktext=['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'],
        showgrid=True,
        #tickangle=0,
        side='top',
        range=[0, 12.5]
    ),
    yaxis=dict(
        zeroline=False,
        tickvals=np.arange(1, 32),
        showgrid=True,
        #autorange="reversed",
        range=[32, 0]
    ),
    template="simple_white",
    legend=dict(
        title="",
        font=dict(size=12),  # Increase legend font size
        title_font_size=14,   # Increase legend title font size
        itemsizing="constant",
        itemwidth=40, 
    ),
    margin=dict(l=30, r=30, t=0, b=30)
)
fig.update_layout(legend= {'itemsizing': 'trace'})

# Show the plot
st.plotly_chart(fig, config=config_modebar, use_container_width=False)

st.markdown("""<hr style="height:1px; border:none; color:#333; background-color:#333;"/>""", unsafe_allow_html=True)

# MOVIE VIZ
st.subheader("🎬 Movies")
col1, _ = st.columns([3, 1], gap='large')
with col1:
    st.markdown("""
            This section highlights information about the movies I’ve watched throughout the year. <br>
            The scatter plot below shows when I watched movies, where, and with whom. Hovering over the points reveals additional details about each movie, including its title, director, city, cinema, and month of release.
    """, unsafe_allow_html=True)
# The scatter plot below displays the month on the x-axis and the release year on the y-axis. 
# The color represents the companion I watched the movie with, while the symbol indicates where I watched it (at home or in a cinema).

# df prep
df_movies_plot = st.session_state['df_movies']
df_movies_plot['movie_date'] = pd.to_datetime(df_movies_plot['movie_date'], format='%d/%m/%Y')
df_movies_plot['month'] = df_movies_plot['movie_date'].dt.month
inverse_dict_months = {v: k for k, v in dict_months.items()}
df_movies_plot['month_name'] = df_movies_plot['month'].map(inverse_dict_months)
df_movies_plot = df_movies_plot.sort_values(by='month')

st.markdown("#### When I watched movies (by month) vs. their release year")
df_movies_plot.movie_companion = df_movies_plot.movie_companion.map(
    {
    "Alone": "Alone",
    "Partner": "With a partner",
    "Friends": "With friends",
    "Volunteering": "Volunteering",
    "Mom": "With my mom"
    }
    )

color_map = {
    "Alone": "#70c9ed",
    "With a partner": "#e85050",
    "With friends": "#FF9F19",
    "Volunteering": "#CC79A7",
    "With my mom": "#0072B2" # "#5dc1a1"
}

symbol_map = {
        'At home': 'star-diamond-open',
        'Cinema': 'star-diamond'
    }


# --- Jitter toggle UI ---
use_jitter = st.checkbox("Use jitter for month axis (scatter plot)", value=True, help="Reduces overlap by adding a small random offset to months.")
jitter_strength = 0.1
random_seed = 42
rng = np.random.default_rng(random_seed)
if use_jitter:
    df_movies_plot['month_jitter'] = df_movies_plot['month'] + rng.uniform(-jitter_strength, jitter_strength, size=len(df_movies_plot))
else:
    df_movies_plot['month_jitter'] = df_movies_plot['month']
# df_movies_plot['movie_release_year_jitter'] = df_movies_plot['movie_release_year'] + np.random.uniform(-0.18, 0.18, size=len(df_movies_plot))

# Scatter plot
fig_scatter = px.scatter(
    df_movies_plot, 
    x='month_jitter', 
    y='movie_release_year',
    color='movie_companion',
    symbol='movie_place', 
    symbol_map=symbol_map,
    color_discrete_map=color_map,
    hover_data=['movie_title', 'movie_director', 'movie_city', 'movie_cinema', 'month_name'],
    opacity=0.8
)

# Update hovertemplate for all main data traces (skip dummy traces)
for trace in fig_scatter.data:
    if hasattr(trace, 'customdata') and ',' in trace.name:
        trace.hovertemplate = (
            'Movie=%{customdata[0]}<br>'
            'Movie director=%{customdata[1]}<br>'
            'Release year=%{y}<br>'
            'City=%{customdata[2]}<br>'
            'Cinema=%{customdata[3]}<br>'
            'Month=%{customdata[4]}<br>'
        )

# Insert dummy "With whom" trace at the very top (index=0)
fig_scatter.add_trace(
    go.Scatter(
        y=[None], mode='markers',
        marker=dict(opacity=0, color='white'),
        name='<span style="font-size:14px"><b>With whom</b></span>',
        showlegend=True,
        hoverinfo='skip',
        legendgroup='companion'
    ))
fig_scatter.data = (fig_scatter.data[-1],) + fig_scatter.data[:-1]

# Customize symbols
# fig_scatter.update_traces(marker=dict(size=20, line=dict(width=1, color='white')))
for trace in fig_scatter.data:
    if hasattr(trace.marker, "symbol"):
        if trace.marker.symbol == "star-diamond-open":
            trace.marker.size = 18
            trace.marker.line.width = 1
        elif trace.marker.symbol == "star-diamond":
            trace.marker.size = 20
            trace.marker.line.width = .8
            trace.marker.line.color = "white"

# To avoid showing the second part of the name in the legend
# I split the name and check if it contains a comma
for trace in fig_scatter.data:
    if ',' in trace.name:
        name = trace.name.split(',')
        if name[1].strip() == 'At home':
            trace['name'] = ''
            trace['showlegend'] = False
        else:
            trace['name'] = name[0]

fig_scatter.add_trace(
    go.Scatter(
        y=[None], mode='markers',
        marker=dict(opacity=0, color='white'),
        name='<span style="font-size:14px"><b>Where</b></span>',
        showlegend=True,
        hoverinfo='skip',
        legendgroup='place'
    )
)

fig_scatter.add_trace(
    go.Scatter(y=[None], mode='markers',
    marker=dict(symbol='star-diamond-open', size=20, color='black'),
    name='At home', showlegend=True, legendgroup='place'
    ))

fig_scatter.add_trace(
    go.Scatter(y=[None], mode='markers',
    marker=dict(symbol='star-diamond', size=20, color='black'),
    name='Cinema', showlegend=True, legendgroup='place'
    ))

fig_scatter.update_layout(
    width=800,
    height=400,
    legend=dict(
        title="",
        font=dict(size=12), 
        title_font_size=14,
        itemsizing='constant'
    ),
    xaxis=dict(
        zeroline=True,
        tickvals=np.arange(1, 13),
        range=[0.5, 12.5],
        ticktext=['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'],
        showgrid=True,
        title='month I watched the movie (2024)'
    ),
    yaxis=dict(
        showgrid=True,
        title='release year'
    ),
    margin=dict(l=30, r=30, t=15, b=30)
)

# Display the chart
st.plotly_chart(fig_scatter, config=config_modebar, use_container_width=False)

# Stats
st.markdown("#### 🗂️ Data <br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1], gap='large')
with col2:
    selected_month = st.selectbox(
        "Select a month:",
        options=["All"] + list(dict_months.keys()),
        index=0
    )
    if selected_month == "All":
        df_movie_show = df_movies_plot.copy()
    else:
        df_movie_show = df_movies_plot[df_movies_plot['month_name']==selected_month]
    df_movie_show = df_movie_show[
        ['movie_date', 'movie_title', 'movie_director', 'movie_release_year', 'movie_city', 'movie_place', 'movie_cinema', 'movie_companion', 'movie_rewatched', 'movie_favorite']
        ]
    df_movie_show = df_movie_show.rename(columns={
        'movie_date': 'Date',
        'movie_title': 'Title',
        'movie_director': 'Director',
        'movie_release_year': 'Release year',
        'movie_city': 'City',
        'movie_cinema': 'Cinema',
        'movie_place': 'Where',
        'movie_companion': 'With whom',
        'movie_rewatched': 'Rewatched',
        'movie_favorite': 'Favorite'
        })
    df_movie_show = (
        df_movie_show
        .fillna('')
        .sort_values(by='Date')
        .reset_index(drop=True)
    )
    # df display properties
    df_movie_show["Release year"] = df_movie_show["Release year"].astype(int).astype(str)
    col_config = {
        "Date": st.column_config.DateColumn("Date", format="DD MMM YYYY")
    }
    styled_df = (
        df_movie_show
        .style
        .set_properties(**{
            "white-space": "pre-wrap",
            "text-align": "left",
            "color": "black",
            #"background-color": "#f9f9f9", 
            "border": "2px solid gray", 
            "padding": "5px",  
            "max-width": "200px",  
        })
    )
    st.dataframe(styled_df, column_config=col_config, height=300)

with col1:
    with st.container(border=True):
        st.markdown("**🎞️ Total movies**")
        st.markdown(f"""
            <div style='font-size:2.5em; font-weight:400; margin-top:-0.2em; margin-bottom:0.1em;'>
                {len(df_movies_plot)}
            </div>
        """, unsafe_allow_html=True)
    with st.container(border=True):
        top_cinemas = df_movies_plot['movie_cinema'].value_counts().head(3)
        st.markdown("**🎪 Top cinemas**")
        #for cinema, count in top_cinemas.items():
        #    st.caption(f"{cinema}: {count}")
        st.markdown(
            """
            <div style='line-height:1.5; margin-top:0.2em; margin-bottom:0.2em;'>
            """ +
            "<br>".join([f"<span style='font-size:0.9em; color:var(--text-secondary);'>{cinema}: {count}</span>" for cinema, count in top_cinemas.items()]) +
            "</div>"
            , unsafe_allow_html=True)
    with st.container(border=True):
        top_directors = df_movies_plot['movie_director'].value_counts().head(3)
        st.markdown("**🎭 Top directors**")
        # Use markdown with custom CSS for tighter spacing
        st.markdown(
            """
            <div style='line-height:1.5; margin-top:0.2em; margin-bottom:0.2em;'>
            """ +
            "<br>".join([f"<span style='font-size:0.9em; color:var(--text-secondary);'>{director}: {count}</span>" for director, count in top_directors.items()]) +
            "</div>"
            , unsafe_allow_html=True)