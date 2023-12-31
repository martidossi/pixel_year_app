import streamlit as st
import pandas as pd

## Setting
st.set_page_config(
    page_title="Hello!",
    page_icon="🟧"
)

st.sidebar.header("Martina Dossi")
st.sidebar.subheader("🎯 Reach me out")
st.sidebar.markdown("- martinadossi.hello@gmail.com")
st.sidebar.markdown("- linkedin, IG, Behance")

st.title("Hello!")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Who I am")
    st.markdown("writing someth - adding sections, personal projects, blog, cv...", unsafe_allow_html=True)
    st.subheader("Why this page")
    st.markdown("For several reasons...creating a dashboard by myself, having some kind of website/online portoflio other than Behance, doing some Python data visualization", unsafe_allow_html=True)

with col2:
    st.image("profilepic2.jpeg")

