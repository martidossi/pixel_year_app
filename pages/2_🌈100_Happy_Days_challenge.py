# Standard library imports
import base64
import glob
import os
import sys

# Third-party imports
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from st_clickable_images import clickable_images
from streamlit_gsheets import GSheetsConnection

# Local imports (after sys.path modification)
# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils import local_css, sort_images_by_number

# Loads and applies style.css
local_css("style.css")

# CONFIG
PAGE_TITLE = "🌈 100 Happy Days challenge"
WORKSHEET_NAME = "100happydays"
N_COLS = 6
N_ROWS = 100
IMAGES_PATH = "pics/100happydays/*.png"
IMAGE_100_PATH = "pics/100happydays/project_100happydays_apply_colors_pic100_col.png"
CACHE_TTL = "10m"

# CACHE_TTL controls how long Streamlit caches the Google Sheets data,
# after 10 minutes, the next user interaction will fetch fresh data,
# it prevents excessive API calls while keeping data reasonably fresh.

st.title(PAGE_TITLE)
st.markdown("""
    This year, inspired by my dear friend [Oriana](https://www.instagram.com/oriana.angelucci/?hl=en), 
    I decided to take on this challenge for **the last 100 days of 2024** (23/09/24–31/12/24). 
    
    *“This challenge is about training your perception on things. 
    Scanning your environment for positive things quickly creates a virtuous circle by adding a positive outlook
    on your daily activities.” [...] “It’s a fantastic reality check —you can’t always change the course of events, but you can always adapt your perception of it all.”
     [URL](https://buffer.com/resources/100-happy-days-challenge/)*
    
    Despite its name, this challenge isn’t about feeling happy every single day. It’s about noticing small moments of gratitude, tiny sparks of positivity to hold onto.
    Even on days when they seem hard to find, those moments are always there, quietly waiting to be seen.
    It might be as simple as a kind gesture, a fleeting smile, or a sense of hope that tough times will eventually pass.
    Day by day, I’ve learned how this practice of appreciating little things can deeply shape the way we move through life
    —turning it into a mindful act of creating joy and embracing the beauty of uncertainty.
    """)
st.markdown("""
    You can click the images below👇 to see the full-size version and details in the sidebar 👈. 
""")

# cols = st.columns(5)
# https://github.com/wjbmattingly/youtube-streamlit-image-grid/blob/main/Home.py
#n = 5
#groups = []
#for i in range(0, len(view_images), n):
#    groups.append(view_images[i:i+n])
#for group in groups:
#    cols = st.columns(n)
#    for i, image in enumerate(group):
#        cols[i].image(image)

conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data
def load_data(worksheet_name, n_cols, n_rows, cache_ttl):
    try:
        df = conn.read(
            worksheet=worksheet_name,
            ttl=cache_ttl,
            usecols=range(n_cols),
            nrows=n_rows
        )
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df = load_data(WORKSHEET_NAME, N_COLS, N_ROWS, CACHE_TTL)

@st.cache_data
def encode_images_to_base64(image_paths):
    encoded_images = []
    for file in image_paths:
        try:
            with open(file, "rb") as image:
                encoded = base64.b64encode(image.read()).decode()
                encoded_images.append(f"data:image/jpeg;base64,{encoded}")
        except FileNotFoundError:
            st.warning(f"Image not found: {file}")
            continue
        except Exception as e:
            st.error(f"Error encoding image {file}: {e}")
            continue
    return encoded_images

output_images = glob.glob(IMAGES_PATH)
view_images = sort_images_by_number(output_images)
images = encode_images_to_base64(view_images)

image_id = clickable_images(
    images,
    titles=[f"pic #{str(i+1)}" for i in range(len(images))],
    div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
    img_style={"margin": "1px", "height": "100px", "cursor": "pointer", "border-radius": "0px"},
)
# st.markdown(f"Image #{image_id} clicked" if clicked > -1 else "No image clicked")

legend_mapping = {
    'family_square': 'Family, home',
    'friends_square': 'Friends, partner, community',
    'nature_square': 'Outdoors, flowers, nature',
    'dataviz_square': 'Dataviz, work, learning',
    'personal_square': 'Self-care, various'
}
inverse_legend_mapping = {v: k for k, v in legend_mapping.items()}

st.sidebar.subheader('🔍 How to read')
st.sidebar.markdown("""
    **Color legend**
     – Below is the full list of categories and corresponding colors used to classify images.
    """)

#### SIDEBAR –START

# Legend on the sidebar
st.sidebar.markdown("""
    <span class='family_square'></span> Family, home <br>
    <span class='friends_square'></span> Friends, partner, community <br>
    <span class='nature_square'></span> Outdoors, flowers, nature <br>
    <span class='dataviz_square'></span> Dataviz, work, learning <br>
    <span class='personal_square'></span> Self-care, various <br>
    """, unsafe_allow_html=True
)
st.sidebar.markdown("""<hr style="height:2px; border:none; color:#333; background-color:#333;"/>""", unsafe_allow_html=True)

# Display the image on the sidebarwith the custom class and details in the sidebar
if image_id < 0:
    st.sidebar.subheader('📸 Select an image')
    st.sidebar.markdown("No image selected.")
else:
    st.sidebar.subheader(f'📸 Selected pic #{image_id+1}')
    # Display image with rounded borders using custom CSS
    st.sidebar.markdown(f'<img src="{images[image_id]}" class="rounded-image" width="200"/>', unsafe_allow_html=True)
    image_tag = df.loc[image_id, 'tag']
    st.sidebar.markdown(f"""
        <br>
        <p style="display:inline; vertical-align:middle;">
            <span class='{inverse_legend_mapping[image_tag]}' style="display:inline-block; vertical-align:middle;"></span>
            <span class="consolas-font" style="font-weight: bold;">tag: </span>
            <span class="consolas-font">{image_tag.capitalize()}</span>
        </p>
        <br>
        <p class="consolas-font" style="font-size: 12px; display:inline; vertical-align:middle">
        ✏️𓂃 {df.loc[image_id, 'event_description']}
        </p>
        <br>
        <p class="consolas-font" style="font-size: 12px; display:inline; vertical-align:middle">
        📍{df.loc[image_id, 'weekday']}, {df.loc[image_id, 'day']}, {df.loc[image_id, 'place']}
        </p>
        """, unsafe_allow_html=True)
st.sidebar.markdown("""
        <hr style="height:1px; border:none; color:#333; background-color:#333;"
        />
        """, unsafe_allow_html=True)

color_dict = {
    'Family, home': '#ffd86d',  # family_square color
    'Friends, partner, community': '#e45761',  # friends_square color  
    'Outdoors, flowers, nature': '#59b257',  # nature_square color
    'Dataviz, work, learning': '#2f5e92',  # dataviz_square color (assuming personal_square)
    'Self-care, various': '#6cc4c7'  # personal_square color
}

# Data prep and sorting
df_places = df[['place', 'tag']].value_counts().reset_index(name='count')
totals = df_places.groupby('place')['count'].sum().sort_values(ascending=False)
sorted_places = totals.index.tolist() 
sorted_places = sorted_places[::-1]
pivot_df = df_places.pivot_table(
    index='place', columns='tag', values='count', aggfunc='sum', fill_value=0
).loc[sorted_places]

# Plot
fig, ax = plt.subplots(figsize=(4, 3.5))  # small size for sidebar
bottom = None
for tag, color in color_dict.items():
    if tag in pivot_df.columns:
        bars = ax.barh(pivot_df.index, pivot_df[tag], height=0.6,
                left=bottom, label=tag, color=color, alpha=0.8,
                edgecolor='white', linewidth=0.5)
        bottom = pivot_df[tag] if bottom is None else bottom + pivot_df[tag]
        for bar in bars:
            bar.set_capstyle('round')
# Styling
ax.grid(axis='x', linestyle='--', alpha=0.7)
ax.set_xlabel("Days", fontsize=12, color="#444")
ax.set_ylabel("")
ax.set_title("")
ax.tick_params(axis='x', labelsize=12, color="#444")
ax.tick_params(axis='y', labelsize=12, color="#444")
ax.legend().set_visible(False)
plt.tight_layout()
for item in [fig, ax]:
    item.patch.set_visible(False)
for spine in ax.spines.values():
    spine.set_visible(False)
# Show in sidebar
st.sidebar.subheader("Places I've been in the last 100 days of the year & number of days")
st.sidebar.pyplot(fig, dpi=1000, use_container_width=True)

st.sidebar.markdown("""<hr style="height:2px; border:none; color:#333; background-color:#333;"/>""", unsafe_allow_html=True)
st.sidebar.subheader('📙 References')
url_video = "https://www.youtube.com/watch?v=J4UtPDaR3cA"
st.sidebar.video(url_video)
st.sidebar.caption("""Dmitry Golubnichy, [100 Happy Days](https://100happydays.com/)""")
st.sidebar.subheader("""
    小確幸 «shōgakkō» Small but Certain Happinesses

    The concept of “shōgakkō” was introduced by Japanese author Haruki Murakami in his 1986 essay “Afternoon in the Islets of Langerhans”.
    He described these small, tangible joys as moments like eating a freshly baked loaf of bread with bare hands,
    opening a drawer to see neatly folded underwear, slipping into a new shirt with the scent of clean cotton,
    or hearing the rustle of a cat settling into bed.
""")
st.sidebar.markdown("""
    <span style="font-size:13px; font-style:italic;">Life’s Little Instruction Book: 1137.
    «Be happy with what you have while working for what you want.»
    [Letterina](https://letterina.substack.com/)</span>
""", unsafe_allow_html=True)
st.sidebar.markdown("""
    <span style="font-size:13px; font-style:italic;">«Be content with what you have; rejoice in the way things are.
    When you realize there is nothing lacking, the whole world belongs to you.» Lao Tzu, [Zen Habits](https://zenhabits.net/perfect/)</span>
""", unsafe_allow_html=True)

#### SIDEBAR -END