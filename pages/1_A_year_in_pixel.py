import streamlit as st

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_gsheets import GSheetsConnection
import sys
from utils import *
sys.path.insert(0, "..")
local_css("style.css")
    
## Setting
#st.set_page_config(
#    page_title="A year in pixel",
#    page_icon="🟧"
#)

#st.set_page_config(layout="wide")

st.title("A year in :rainbow[pixel]")
st.markdown("A *pixel year* is a visual representation of one's emotions and experiences throughout the course of a year. In this concept, each day is assigned a specific color that encapsulates the predominant mood or feeling of that day.")

st.subheader("**2024**")
conn = st.connection("gsheets", type=GSheetsConnection)
data = conn.read(
    worksheet="pixel_year",
    ttl="10m",
    usecols=range(13),
    nrows=31
)
first_col = data.columns[0]
data = data.rename(columns={first_col: 'id_day'})
data = data.set_index('id_day')
data = data.fillna('0')

pixel_val_map = {
    '0': 0,
    'Missing': 1,
    'Happy': 2,
    'Loved': 3, 
    'Confident': 4,
    'Playful': 5,
    'Embarassed': 6,
    'Angry': 7,
    'Scared': 8,
    'Sad': 9,
    
}
# from text to numbers
for col in data.columns:
    data[col] = data[col].map(pixel_val_map)

cmap_dict = {
    0: '#ebebeb',
    1: '#ffffff',
    2: '#f78ac7',
    3: '#f88595',
    4: '#fa9c7d',
    5: '#fbc779',
    6: '#6ad2a7',
    7: '#7ccdf8',
    8: '#8d9dfa',
    9: '#c78dfc'
}
cmap = list(cmap_dict.values())

fig, ax = plt.subplots(figsize=(10, 10))
ax = sns.heatmap(
    data.transpose(),
    cmap=cmap,
    cbar=False,
    linewidths=1.2,
    linecolor='white',
    square=True,
    vmin=0,
    vmax=len(cmap_dict),
    xticklabels=1,
    ax=ax
)
ax.set_yticklabels(labels=['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'], rotation=0, fontsize=8)
ax.set_xticklabels(labels=list(data.index), rotation=0, fontsize=8)
ax.set_xlabel('')
st.pyplot(fig)

with st.expander('**Legenda**', expanded=False):
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

st.sidebar.subheader('Some references')
st.sidebar.markdown("[Happy Coding Blog](https://happycoding.io/blog/year-in-pixels-2019)")
st.sidebar.markdown("[The emotion wheels](https://humansystems.co/emotionwheels/)")

col1, col2 = st.columns([1, 2])
with col1:
    st.markdown("To determine which emotions to consider, I did some research and came across this emotions wheel. I'll be using the 8 internal emotions as my main reference and the external ones to help me in deciding between different states. I like that it's symmetrical, with warm colors for comfortable and positive emotions and cool colors for the others, so that for this initial attempt, I've decided to keep the same color scale. To learn more about the methodology behind this wheel, check out the *references*. Alternatively, you can watch this [video](https://www.youtube.com/watch?v=ehzj0UHIU9w&t=113s) where the author describes the methodology used.")
with col2:
    st.image("emotion-wheel.png", width=450)

