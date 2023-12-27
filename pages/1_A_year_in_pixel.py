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
    worksheet="2024_pixel",
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
    'Normal': 3, 
    'Relaxed': 4,
    'Sad': 5,
    'Excited': 6
}

pixel_col_map = {
    '0': '#ebebeb',
    'Missing': '#000000',
    'Happy': '#ffd92f',
    'Normal': '#fc8d62', 
    'Relaxed': '#66c2a5',
    'Sad': '#8da0cb',
    'Excited': '#e78ac3'
}

for col in data.columns:
    data[col] = data[col].map(pixel_val_map)    

fig, ax = plt.subplots(figsize=(10, 10))
ax = sns.heatmap(
    data.transpose(),
    cmap=list(pixel_col_map.values()),
    cbar=False,
    linewidths=1.2,
    linecolor='white',
    square=True,
    xticklabels=1,
    ax=ax
)
#ax.xaxis.tick_top() # x axis on top
#ax.xaxis.set_label_position('top')
ax.set_yticklabels(labels=['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'], rotation=0, fontsize=8)
ax.set_xticklabels(labels=list(data.index), rotation=0, fontsize=8)
ax.set_xlabel('')
st.pyplot(fig)

with st.expander('**Legenda:**', expanded=False):
    col1, col2, col3, col4 = st.columns([1,1,1, 1])
    with col1:
        st.markdown("<div><span class='highlight happy'>Happy</span></div>", unsafe_allow_html=True)
        st.markdown("<div><span class='highlight happy'>Happy</span></div>", unsafe_allow_html=True) 
    with col2:
        st.markdown("<div><span class='highlight happy'>Happy</span></div>", unsafe_allow_html=True)
        st.markdown("<div><span class='highlight happy'>Happy</span></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div><span class='highlight happy'>Happy</span></div>", unsafe_allow_html=True)
        st.markdown("<div><span class='highlight happy'>Happy</span></div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div><span class='highlight happy'>Happy</span></div>", unsafe_allow_html=True)
        st.markdown("<div><span class='highlight happy'>Happy</span></div>", unsafe_allow_html=True)
    st.markdown('#')
    
st.subheader('Some references')
st.markdown("[Happy Coding Blog](https://happycoding.io/blog/year-in-pixels-2019)")
