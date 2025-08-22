import streamlit as st
import time
import os
import sys

# Local imports (after sys.path modification)
# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils import local_css

# Loads and applies style.css
local_css("style.css")

st.sidebar.subheader('📙 References')
st.sidebar.image("pics/tree_barc.jpeg")
st.sidebar.caption("06/07/2024, Barcelona")
st.sidebar.markdown("""
    <span style="font-size:13px; font-style:italic;">«If there's something this year has taught me, 
    it's to appreciate the detours; to enjoy the weird pit stops; to collect unexpected memories.»
    Anne-Laure Le Cunff
""", unsafe_allow_html=True)

if st.sidebar.button('Three cheers 🎈'):
    st.toast('Hip!')
    time.sleep(.5)
    st.toast('Hip!')
    time.sleep(.5)
    st.toast('Hooray!', icon='🎉')
# st.sidebar.image("pics/feelings.jpeg", width=250)

st.title("📌 Notes")
col1, col2 = st.columns(2, gap='large')
with col1:
    st.markdown("## Motivation")
    st.markdown(
        f"""
        🔍 Data acts as a lens that we can leverage to **unravel the world’s complexity**, turning what might seem
        chaotic and convoluted into something much more structured and transparent.

        ✍️ **Self-reported data** serves the same purpose, yet shifts the focus inward, 
        explaining facts with personal narratives that reveal who we are and the stories we carry within.

        🌟 In this context, data visualization becomes a tool for **self-discovery**,
        helping us see patterns that might otherwise remain hidden. 

        🫐 Inspired by the concept of [Data Humanism](https://giorgialupi.com/data-humanism-my-manifesto-for-a-new-data-wold),
        this project explores the potential of small, subjective data.
        Over the past year (2024), I’ve been collecting data about my daily life that I found interesting
        –partly to better understand myself, reflect on the year once the collection is complete,
        and experiment with a new project without rigid goals. Working with personal data had been on my to-do list for some time, 
        and I’m glad I finally took the plunge.

        🧶 The **daily practice** of tracking data has been a valuable discovery itself:
        I practiced consistency, realized it works best when I focus on only a few features, 
        resisted the urge to introduce changes to keep the collection simple and coherent, 
        cursed myself when I forgot one or more days,
        and felt the satisfaction of steady progress. 

        🫧 Some of my initial research questions include:
        - How do emotions change throughout the year, across months, days, or weekends?
        - What are my favorite days and seasons, and how do these relate to mood? 
        - How does physical location or activities like watching movies influence my emotional state?
        - Are there surprising cross-influences, like certain days correlating with specific movies or moods?

""", unsafe_allow_html=True)


with col2:
    st.markdown("## Lessons learned")
    st.markdown("""
        - **Simplicity is key**: focusing on a few features makes the process manageable and the data more coherent.
        - **Consistency matters**: regular tracking, even with occasional lapses, makes the experience truly rewarding and insightful.
        - **Self-reflection**: the act of tracking itself naturally fosters greater self-awareness and mindfulness.           
        - **Behavior shifts**: tracking shapes behavior –for instance, keeping tabs on movies made me want to watch more, as clearly shown by January’s spike and the following (more real) trend.
        - **Imperfect is still valuable**: even imperfect tracking matters, it’s the effort and attention that count, not flawless data.
        - **Gentle accountability**: over time, the practice nudges you to notice what you value and what you want to prioritize.
        - **Visualization power**: visual representations helped uncover patterns and trends that were not immediately obvious.
        - **Emotions are very subjective**: how we feel is deeply personal, and finding the right way to categorize emotions isn’t easy. 
                I realized that some of the categories I chose didn’t fit me at all (some I never used). 
                I didn’t want to change them on the go, though I did add intensity information, which helped frame my experiences better. 
                Next time, I know I’ll need a different approach, also allowing for more feelings the same day.
        - **Tracking habits evolve**: I’ve noticed that “happy days” are easier to skip. On the other hand, when I feel sad or confused, I’m more willing to journal and track my emotions
                (this is also what I’ve been naturally doing lately).
""")

st.markdown("## The process")

col1, col2 = st.columns(2, gap='small')
with col1:
    st.markdown("#### 1. Data collection")
    st.markdown("""
       For data collection, I used a combination of Google Forms and Google Sheets:
        - First, I created a Google Form to easily track aspects of my daily life (such as emotions, visited cities, movies watched, and other activities).
        - The form automatically populated a Google Sheet. For clarity, I then cleaned and reorganized the data into dedicated sheets.
        """)
    st.markdown("#### 2. Data analysis")
    st.markdown("""
        For data analysis and visualization prototypes, I worked with Python using Jupyter Notebooks.
        """)
    st.markdown("#### 3. Data visualization")
    st.markdown("""
        The visualizations were created with `matplotlib`, `seaborn`, and `plotly`, and then brought together in an interactive dashboard built with `Streamlit`. 
        The goal was to develop clear and engaging visual representations of the data that not only revealed patterns and trends in my daily life but also allowed for an interactive exploration of them.
        """)
    st.markdown("#### *Tools and libraries*")
    st.markdown("""
        - **Streamlit**: for building the interactive web app.
        - **Google Sheets**: for data storage and management.
        - **Python**: for data analysis and visualization.
        - **Various Python libraries**: including `pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly`, `gspread`, and `st_gsheets_connection`.
        """)    
with col2:
    st.image("pics/process.png")

st.markdown("## Thanks for reading! 💜")

