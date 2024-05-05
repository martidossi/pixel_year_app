import streamlit as st

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yaml
from streamlit_gsheets import GSheetsConnection
import sys
from utils import *

## Setting
st.set_page_config(
    page_title="A year in pixel",
    page_icon="🟧"
)
    
sys.path.insert(0, "..")
local_css("style.css")

conn = st.connection("gsheets", type=GSheetsConnection)

with open("config.yml", 'r') as f:
    cfg = yaml.safe_load(f)
    
## Sidebar
st.sidebar.subheader('References')
st.sidebar.image("pics/emotion-wheel.png")
st.sidebar.markdown("""
    The emotion wheel depicted above serves as my primary reference. Specifically, I'll be focusing on the eight internal emotions (four positives, four negatives) as my main guide, while considering the external ones to aid in distinguishing between different states. To learn more about the methodology behind this wheel, check out the links below.
    - [The emotion wheels](https://humansystems.co/emotionwheels/)
    - [The methodology](https://www.youtube.com/watch?v=ehzj0UHIU9w&t=113s)
    """)
st.sidebar.subheader('Other inspirations')
st.sidebar.markdown("""
    - [Happy Coding Blog](https://happycoding.io/blog/year-in-pixels-2019)
    """)

## Title
st.title("A Year in :rainbow[Pixel]")
st.markdown("A *Pixel Year* is a visual representation of personal emotions throughout the course of a year. Each day is assigned a specific color that refers to the predominant mood or feeling of that day.")

st.subheader("**2024**")

   
## Heatmap
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
    #ax.set_xticklabels(labels=list(df_emotion_id.index), rotation=0, fontsize=8)
    ax.set_xlabel('')
    st.pyplot(fig)
    st.markdown("**Legenda**")
    st.markdown("Feelings may be linked to various intensities. Cells without any smile are just neutral, whereas positive pixels may be good :) or very good :)) days, as well as negative ones can be bad :( or very bad :(( days.")


