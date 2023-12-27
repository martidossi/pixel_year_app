import streamlit as st
import pandas as pd


col1, col2 = st.columns(2)
with col1:
    st.markdown("Hello!", unsafe_allow_html=True)
    st.subheader("Who I am")
    st.markdown("nkfbkmb", unsafe_allow_html=True)
    st.markdown("nkfbkmb", unsafe_allow_html=False)
    st.subheader("Why this page")

with col2:
    st.image("profilepic2.jpeg")
    