import streamlit as st
import pandas as pd

import sys
from utils import *
sys.path.insert(0, "..")
local_css("style.css")

css_font = """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300&display=swap');
    html, body, [class*="css"] {
    font-family: 'Inter', sans-serif; 
    font-size: 18px;
    font-weight: 500;
    color: #091747;
}
"""
st.markdown(f'<style>{css_font}</style>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("Hello!", unsafe_allow_html=True)
    st.subheader("Who I am")
    st.markdown("nkfbkmb", unsafe_allow_html=True)
    st.markdown("nkfbkmb", unsafe_allow_html=False)
    st.subheader("Why this page")

with col2:
    st.image("profile_pic_arancio.png")
    