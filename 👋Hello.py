import streamlit as st
import pandas as pd
import sys
from utils import *
from annotated_text import annotation


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
st.sidebar.subheader('🌸 About me')
# st.sidebar.image("pics/profile_pic.png", width=250)
st.sidebar.markdown("""
    I'm a data scientist with a statistical background, based in Italy,
    and particularly passionate about data visualization. 
    To know more about me, check out my [personal page](https://martina-dossi.notion.site/Hi-I-m-Martina-6c1e9636b59245cd8cfedc1fffd05a1b).
    """)
st.sidebar.subheader('💌 Contacts')
st.sidebar.markdown("""
    If you have any questions, feedback of any kind, I'd be delighted to connect.
    Feel free to reach out to me!
    - martinadossi.hello at gmail.com
    - [LinkedIn](https://www.linkedin.com/in/martina-dossi/), [Instagram](https://www.instagram.com/adatastory_/), [Behance](https://www.behance.net/martinadossi)
    """)

st.sidebar.subheader('📙 References')

st.sidebar.markdown("""
    *«Data collected from life can be a snapshot of the world
    in the same way that a picture catches small moments in time.»*
    """)
st.sidebar.image("pics/smalldata_bigdata_output.png", width=250)
st.sidebar.write("[Dear Data](https://www.dear-data.com/theproject), Giorgia Lupi and Stefanie Posavec.")
st.sidebar.write("[Feltron personal annual reports](http://feltron.com/), Nicholas Felton.")

st.title("Hello!")

st.header("My name is Martina.")
text_1 = "Here is where I planned to visualize "
text_2 = " I am collecting through 2024."
st.markdown("### " + text_1 + str(annotation("personal data", "", "#fea"))
            + text_2, unsafe_allow_html=True)
# st.markdown("<h3>" + text + str(annotation("apple", "", "#fea")) + "</h3>", unsafe_allow_html=True)

st.write("---")
st.markdown(
    f"""
    → This year I am finally succeeding in collecting various personal data from everyday life (emotions, where I am, the movies I see,
    and some others) –after a few failed attempts. Since last year, I've realized that in order to be consistent 
    in daily data collection, I cannot gather data of too many diverse topics (if the goal is annual). 
    So to begin with, I am focusing on what I am most interested in: {str(annotation("daily emotions", "", "#faa"))} and
    what can influence them! 
    """, unsafe_allow_html=True)
st.markdown(
    f"""
    → If data is a filter we use to portray reality and learn more about it, then self-reporting data may serve as a 
    powerful lens for {str(annotation("self discovery", "", "#faa"))}, to uncover and recognize patterns we might
    not otherwise pay attention to. Taking up the concept of 
    [Data Humanism](https://giorgialupi.com/data-humanism-my-manifesto-for-a-new-data-wold), data moves from being
    something cold and aseptic to being filled with life, being a tool to foster human knowledge and introspection.
    """, unsafe_allow_html=True)

st.markdown(
    f"""
    → The relationships I intend to explore –aka my {str(annotation("research questions", "", "#faa"))}:
    - How do I feel during the year? Is there a correlation between feelings and months, days, weekends?
    - Are my emotions influenced by where I am, physically? For instance, how does going to the office affect me?
    - Is there a correlation between watching movies and mood?
    - How do I feel on days when I have a headache?
    - What about cross influences? For example, days of the year and movies, cities and movies?
    """, unsafe_allow_html=True)

st.markdown(
    f"""
    → From a technical point of view, I use {str(annotation("Python", "", "#faa"))} to experiment with various
    libraries, graphical models, and interactive visualizations, all supported by Streamlit.
    """, unsafe_allow_html=True)

st.subheader("Join me as I decode the year through data!")

