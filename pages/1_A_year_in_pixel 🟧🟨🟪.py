import streamlit as st

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_gsheets import GSheetsConnection

#import sys
#from utils import *
#sys.path.insert(0, "..")
#local_css("style.css")

## Setting
st.set_page_config(
    page_title="A year in pixel",
    page_icon="🟧"
)

st.write("# A year in pixel \n")

st.sidebar.header("A year in pixel")
st.sidebar.write("➜aka a mood tracker")


#t = "<div>Hello there my <span class='highlight blue'>   </span> </div>"
#st.markdown(t, unsafe_allow_html=True)

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
    '0': '#b3b3b3',
    'Missing': '#000000',
    'Happy': '#ffd92f',
    'Normal': '#fc8d62', 
    'Relaxed': '#66c2a5',
    'Sad': '#8da0cb',
    'Excited': '#e78ac3'
}

for col in data.columns:
    data[col] = data[col].map(pixel_val_map)    
col_hex = sns.color_palette("Set2", 8).as_hex()

fig, ax = plt.subplots(1, 1, figsize=(10,10))
ax = sns.heatmap(
    data.transpose(),
    cmap=list(pixel_col_map.values()),
    cbar=False,
    linewidths=1,
    linecolor='white',
    square=True,
    xticklabels=1,
    ax=ax
)
ax.set_xlabel('Day')
ax.set_xticklabels(labels=list(data.index),rotation=0, fontsize=10)
st.pyplot(fig)