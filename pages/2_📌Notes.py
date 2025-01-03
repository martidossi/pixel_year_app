import streamlit as st
import time
import sys
from utils import *

sys.path.insert(0, "..")
local_css("style.css")

st.sidebar.markdown("""
    # If there's something this year has taught me, it's to appreciate the detours; to enjoy the weird pit stops; to collect unexpected memories.
    Anne-Laure Le Cunff.
    """)
if st.sidebar.button('Three cheers'):
    st.toast('Hip!')
    time.sleep(.5)
    st.toast('Hip!')
    time.sleep(.5)
    st.toast('Hooray!', icon='🎉')
# st.sidebar.image("pics/feelings.jpeg", width=250)

st.markdown("# My intention")
col1, col2 = st.columns(2, gap='large')
with col1:
    st.markdown(
        f"""
        🔍 Data acts as a lens that we can leverage to unravel the world’s complexity, turning what might seem
        chaotic and convoluted into something more structured and transparent.

        ✍️ Self-reported data serves the same purpose, yet shifts the focus inward, 
        explaining facts with personal narratives that reveal who we are and the stories we carry within.

        🌟 In this context, data visualization becomes a tool for self-discovery,
        helping us see patterns that might otherwise remain hidden. 

        🫐 Inspired by the concept of [Data Humanism](https://giorgialupi.com/data-humanism-my-manifesto-for-a-new-data-wold),
        this project explores the potential of small, subjective data.
        Over the past year, I’ve been collecting data about my daily life that I found interesting
        —partly to understand myself better, reflect on the past year once the collection is complete,
        and also to experiment with a new project and see where it might lead, without predefined goals.

        🧶 The daily practice of tracking data has been a valuable discovery itself:
        I practiced consistency, learned that this consistency works best
        when I track only a few features, resisted the urge to introduce changes
        to keep the collection simple and coherent, cursed myself when I forgot one or more days,
        and felt the satisfaction of steady progress. 
        """, unsafe_allow_html=True)

with col2:
    st.image("pics/tree_barc.jpeg", width=300)
    st.write("06/07/2024, Barcelona")

st.markdown(
    f"""
    🫧 Some relationships I aim to explore—my personal research questions—include:
    - How do I feel throughout the year? Is there a correlation between my emotions and months, days, or weekends?
    - What is my favourite days? How do I feel during weekends? Which season brings me the most happiness?
    - Are my emotions influenced by my physical location? For example, how does going to the office affect my mood?
    - Is there a connection between watching movies and my emotional state?
    - What about cross-influences? For instance, do specific days of the year correlate with movies, or do cities and movies affect each other?
    """, unsafe_allow_html=True)
st.markdown("**Navigate the sidebar or explore the other pages:**")
st.page_link("pages/1_🌈100_Happy_Days_challenge.py", label="100 Happy Days challenge", icon="🌈")
st.page_link("pages/2_📌Notes.py", label="Take-aways", icon="📌")



