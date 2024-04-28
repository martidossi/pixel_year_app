import streamlit as st
import pandas as pd
import sys
from utils import *

## Setting
st.set_page_config(
    page_title="Hello!",
    page_icon="🟧"
)
#st.image("pics/cover.png")

sys.path.insert(0, "..")
local_css("style.css")

import base64

@st.cache_data()
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

set_png_as_page_bg('pics/cover.png')

st.sidebar.header("Martina Dossi")
st.sidebar.markdown("💬 If you have any questions, feedback of any kind, I'd be delighted to connect. Feel free to reach out to me!")
st.sidebar.markdown("- martinadossi.hello at gmail.com")
st.sidebar.markdown("- [LinkedIn](https://www.linkedin.com/in/martina-dossi/), [Instagram](https://www.instagram.com/adatastory_/), [Behance](https://www.behance.net/martinadossi)")

st.title("Hello!")

col1, col2 = st.columns(2)
with col1:
    st.subheader("My name is Martina.")
    st.markdown("""
    `why` I'd like to use this space to explore personal projects and Python visualizations, also in interactive ways. I'll be using Matplotlib, Seaborn, and Plotly.
    
    `who`I'm a data scientist with a statistical background, based in Italy, and particularly passionate about data visualization. To know more about me, check out my page: [URL](https://martina-dossi.notion.site/Hi-I-m-Martina-6c1e9636b59245cd8cfedc1fffd05a1b).
    """, unsafe_allow_html=True)

with col2:
    st.image("pics/profilepic2.jpeg")

