import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yaml
from streamlit_gsheets import GSheetsConnection
import streamlit.components.v1 as components
import sys
from utils import *
from itertools import product
from pywaffle import Waffle
import plotly.express as px
import numpy as np

# Setting
st.set_page_config(
    page_title="A year in pixel",
    page_icon="🟧"
)
    
sys.path.insert(0, "..")
local_css("style.css")

conn = st.connection("gsheets", type=GSheetsConnection)
config_modebar = {'displayModeBar': False}

with open("config.yml", 'r') as f:
    cfg = yaml.safe_load(f)
    
# Sidebar
st.sidebar.subheader('References')
st.sidebar.markdown("""
    The emotion wheel below represents my primary reference. Specifically, I'll be focusing on the eight internal emotions (four positives, four negatives) as my main guide, while considering the external ones to aid in distinguishing between different states. To learn more about the methodology behind this wheel, check out the links below.
    - [Emotion wheels](https://humansystems.co/emotionwheels/)
    - [The methodology](https://www.youtube.com/watch?v=ehzj0UHIU9w&t=113s)
    """)
with st.sidebar.expander('See the wheel:'):
    st.image("pics/emotion-wheel.png")
st.sidebar.subheader('Other inspirations')
st.sidebar.markdown("""
    - [Happy Coding blog](https://happycoding.io/blog/year-in-pixels-2019)
    """)

# Title
st.title("A Year in :rainbow[Pixel]")
st.markdown("A *Pixel Year* is a visual representation of personal emotions throughout the course of a year. Each day is assigned a specific color that refers to the predominant mood or feeling of that day.")

st.subheader("**2024**")

# Heatmap
dict_emotion_id = cfg['map_emotion_id']
dict_emotion_color = cfg['map_emotion_color']

# Emotion df
df_emotion = conn.read(
    worksheet="pixel_year",
    ttl="10m",
    usecols=range(13),
    nrows=31
)
df_emotion = (
    df_emotion
    .rename(columns={'day/month': 'id_day'})
    .set_index('id_day')
    .fillna('0')
)
month_list = list(df_emotion.columns)
emotion_list = list(dict_emotion_color.keys())[2:]
positive_emotion_list = emotion_list[:4]
negative_emotion_list = emotion_list[4:]

# Mapping emotions to numbers
df_emotion_id = (
    pd.DataFrame([df_emotion[col].map(dict_emotion_id) for col in df_emotion.columns])
    .transpose()
    .fillna(0)
    .astype(int)
)

# Emotion intensity
df_intensity = conn.read(
    worksheet="pixel_year_intensity",
    ttl="10m",
    usecols=range(13),
    nrows=31
)
df_intensity = (
    df_intensity
    .rename(columns={'day/month': 'id_day'})
    .set_index('id_day')
    .fillna('0')
)

# Visualization
tab1, tab2 = st.tabs(["Prevailing feeling", "Intensity"])
with tab1:
    fig, ax = plt.subplots(figsize=(10, 10))
    ax = sns.heatmap(
        df_emotion_id.transpose(),
        cmap=list(dict_emotion_color.values()),
        cbar=False,
        linewidths=1.2,
        linecolor='white',
        square=True,
        vmin=0,
        vmax=len(dict_emotion_color),
        xticklabels=1,
        ax=ax
    )

    ax.set_yticklabels(labels=['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'], rotation=0, fontsize=8)
    ax.set_xticklabels(labels=list(df_emotion_id.index), rotation=0, fontsize=8)
    ax.set_xlabel('')
    st.pyplot(fig)
    st.markdown("**Legenda**")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        st.markdown("<span class='happy_square'></span> Happy", unsafe_allow_html=True)
        st.markdown("<span class='loved_square'></span> Loved", unsafe_allow_html=True)
    with col2:
        st.markdown("<span class='confident_square'></span> Confident", unsafe_allow_html=True)
        st.markdown("<span class='playful_square'></span> Playful", unsafe_allow_html=True)
    with col3:
        st.markdown("<span class='embarassed_square'></span> Embarassed", unsafe_allow_html=True)
        st.markdown("<span class='angry_square'></span> Angry", unsafe_allow_html=True)
    with col4:
        st.markdown("<span class='scared_square'></span> Scared", unsafe_allow_html=True)
        st.markdown("<span class='sad_square'></span> Sad", unsafe_allow_html=True)
    st.markdown('#')

with tab2:
    labels = df_intensity.transpose().replace('0', '').replace('Missing', '').replace(':|', '')
    fig, ax = plt.subplots(figsize=(10, 10))
    ax = sns.heatmap(
        df_emotion_id.transpose(),
        cmap=list(dict_emotion_color.values()),
        cbar=False,
        linewidths=1.2,
        linecolor='white',
        square=True,
        vmin=0,
        annot=labels,
        fmt='',
        vmax=len(dict_emotion_color),
        xticklabels=1,
        ax=ax
    )

    ax.set_yticklabels(labels=['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'], rotation=0, fontsize=8)
    ax.set_xticklabels(labels=list(df_emotion_id.index), rotation=0, fontsize=8)
    ax.set_xlabel('')
    st.pyplot(fig)
    st.markdown("**Legenda**")
    st.markdown("""
    Feelings may be linked to various intensities. 
    Cells without any smile are just neutral, whereas positive pixels may be good :) or very good :)) days,
    as well as negative ones can be bad :( or very bad :(( days.
    """)

# Df month emotion
df_melt = df_emotion.melt()
df_melt = df_melt[(df_melt['value']!='0') & (df_melt['value']!='Missing')]
df_melt.columns = ['month', 'emotion']
df_melt['day'] = df_melt.groupby(['month']).cumcount()+1
df_count = df_melt[['month', 'emotion']].value_counts().reset_index().rename(columns={0: 'value'})
df_month_emotion_base = pd.DataFrame(data=product(month_list, emotion_list), columns=['month', 'emotion'])
df_month_emotion_base['value'] = 0
df_month_emotion = (
    pd.merge(
        df_month_emotion_base,
        df_count,
        how='left',
        left_on=['month', 'emotion'],
        right_on = ['month', 'emotion'])
).fillna(0)
df_month_emotion['value'] = df_month_emotion.value_y.combine_first(df_month_emotion.value_x)
df_month_emotion = df_month_emotion.drop(['value_x', 'value_y'], axis=1)

# Bar plot
st.write('---')
st.subheader('Total number of days')
df_n_days = df_month_emotion.groupby('emotion').agg({'value': sum}).reindex(emotion_list).reset_index()
df_n_days_pos = df_n_days[df_n_days.emotion.isin(positive_emotion_list)]
df_n_days_neg = df_n_days[df_n_days.emotion.isin(negative_emotion_list)]

df_n_days['perc_value'] = round(100*df_n_days.value/df_n_days.value.sum()).astype(int)
df_n_days['emotion_type'] = list(np.repeat('positive emotion', 4)) + list(np.repeat('negative emotion', 4))

dict_emotion_color_extended = dict_emotion_color
dict_emotion_color_extended.update({'(?)': 'white'})
fig = px.treemap(
    df_n_days,
    path=[px.Constant("all"), 'emotion_type', 'emotion'],
    values='value',
    color='emotion',
    color_discrete_map=dict_emotion_color_extended,
)
fig.update_layout(
    height=380,
    margin=dict(t=20, b=0, r=50),
)
fig.update_traces(
    marker=dict(cornerradius=2),
    marker_line_width=1,
    marker_line_color='black'
)
fig.data[0].textinfo = 'label+text+percent entry'
fig.data[0].hovertemplate = '%{label}<br>number of days: %{value}'
st.plotly_chart(fig, config=config_modebar)

# Trend over time
st.write('---')
st.subheader('Trend over time')

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    Month by month, this visualization shows the trend over time of emotions, in terms of number of days.
    Use the widget on the right to highlight selected emotions.
    """)
with col2:
    sel_status = st.multiselect("Pick one or more emotions:", emotion_list, [])

fig = px.line(
    df_month_emotion,
    x="month",
    y="value",
    color="emotion",
    color_discrete_map=dict_emotion_color,
    template="simple_white"
)
if len(sel_status) >= 1:
    for d in fig['data']:
        if d['name'] in sel_status:
            d['line']['color'] = dict_emotion_color[d['name']]
            d['line']['width'] = 3
        if d['name'] not in sel_status:
            d['line']['color'] = 'lightgrey'
fig.update_layout(
    font=dict(
        family="Roboto",
        size=12
    ),
    legend_title_font_color="black",
    height=380,
    xaxis_title="",
    yaxis_title="number of days",
    xaxis=dict(showgrid=True, tickcolor='black', color='black'),
    yaxis=dict(showgrid=True, tickcolor='black', color='black'),
    margin=dict(t=20),
)
fig.update_xaxes(showline=True, linewidth=1, linecolor='black')
fig.update_yaxes(showline=True, linewidth=1, linecolor='black')
st.plotly_chart(fig, config=config_modebar)

st.markdown("##### Visualizing totals")
tab1, tab2 = st.tabs(["Stacked bar chart", "Polar chart"])
with tab1:
    fig = px.bar(
        df_month_emotion,
        x="month",
        y="value",
        color="emotion",
        color_discrete_map=dict_emotion_color,
        template="simple_white",
    )
    fig.update_layout(
        font=dict(
            family="Roboto",
            size=12,
        ),
        legend_title_font_color="black",
        height=380,
        xaxis_title="",
        yaxis_title="number of days",
        xaxis=dict(showgrid=True, tickcolor='black', color='black'),
        yaxis=dict(showgrid=True, tickcolor='black', color='black'),
        margin=dict(t=20),
        bargap=0
    )
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black')
    st.plotly_chart(fig, config=config_modebar)
with tab2:
    fig = px.bar_polar(
        df_month_emotion,
        r="value",
        theta="month",
        color="emotion",
        color_discrete_map=dict_emotion_color
    )
    fig.update_layout(
        font=dict(
            family="Roboto",
            size=12,
        ),
        margin=dict(t=20),
        height=380,
        legend_title_font_color="black",
        polar=dict(
            bgcolor="white",
            radialaxis=dict(
                gridcolor='lightgray',
                griddash='dot',
                tickcolor='black',
                tickfont_color='black'
                ),
            angularaxis=dict(
                linecolor='black',
                gridcolor='gray',
            )
        ),
    )
    st.plotly_chart(fig, config=config_modebar)

with st.expander("See the data:"):
    df_expander = (
        pd.pivot_table(df_month_emotion, index='month', columns='emotion', values='value')[emotion_list]
    ).reindex(month_list)
    st.dataframe(df_expander)
