import streamlit as st
import time
import sys
from utils import local_css

sys.path.insert(0, "..")
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

st.markdown("## Motivation")
col1, col2 = st.columns(2, gap='large')
with col1:
    st.markdown(
        f"""
        🔍 Data acts as a lens that we can leverage to unravel the world’s complexity, turning what might seem
        chaotic and convoluted into something much more structured and transparent.

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
    st.markdown(
        f"""
        🫧 Some relationships I aim to explore —my personal research questions— include:
        - How do I feel throughout the year? Is there a correlation between my emotions and months, days, or weekends?
        - What is my favourite days? How do I feel during weekends? Which season brings me the most happiness?
        - Are my emotions influenced by my physical location? For example, how does going to the office affect my mood?
        - Is there a connection between watching movies and my emotional state?
        - What about cross-influences? For instance, do specific days of the year correlate with movies, or do cities and movies affect each other?
        """, unsafe_allow_html=True)
    st.markdown("## Lessons learned")
    st.markdown("""
        - the importance of tracking things consistently, even when it feels challenging;
        - how categories and structure matter—and how I’d like to refine them for next year;
        - that the exercise worked as a kind of personal journal, helping me revisit past moments and appreciate small joys (like in *100 Happy Days*);
        - how tracking itself can shape behavior—for example, noticing patterns like watching many movies at the beginning and fewer later on
    """)


st.markdown("## The process")

col1, col2 = st.columns(2, gap='small')
with col1:
    st.markdown("""
    The data collection process was relatively simple. It involved three main steps:
    1. **Google Form**: I created a Google Form that I could easily access from my phone every day to track features about my daily life (emotions, visited cities, movies watched, and other aspects).
    2. **Google Sheets**: For the sake of clarity, I rearranged the data in cleaned and dedicated Google Sheets.
    3. **Python**: I used Python to explore the data and find patterns, then Streamlit to visualize them in a meaningful and interactive way.
    """)
with col2:
    st.image("pics/process.png")


with st.container():
    with st.form("input_form"):
        col1, col2 = st.columns([9, 1])

        with col1:
            st.text_input("Please enter what you want to tell me here: ")

        with col2:
            st.form_submit_button()

with st.form("my_form"):
    st.write("Inside the form")
    slider_val = st.slider("Form slider")
    checkbox_val = st.checkbox("Form checkbox")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("slider", slider_val, "checkbox", checkbox_val)
st.write("Outside the form")