import streamlit as st
import glob

st.title("100 Happy days challenge")

directory = r'happy_days_pics/'
output_images = glob.glob(directory + "/output/*.png")
view_images = sorted(output_images)
cols = st.columns(5)

# https://github.com/wjbmattingly/youtube-streamlit-image-grid/blob/main/Home.py

n = 5
groups = []
for i in range(0, len(view_images), n):
    groups.append(view_images[i:i+n])
for group in groups:
    cols = st.columns(n)
    for i, image in enumerate(group):
        cols[i].image(image)