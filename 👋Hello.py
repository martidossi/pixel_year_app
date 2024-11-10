import sys
import streamlit as st
import base64
from utils import *
from annotated_text import annotation


## Setting
st.set_page_config(
    page_title="Hello",
    page_icon="🟧",
    layout="wide"
)

# st.image("pics/cover.png")
def set_bg_hack(main_bg):
    '''
    A function to unpack an image from root folder and set as bg.

    Returns
    -------
    The background.
    '''
    # set bg name
    main_bg_ext = "png"

    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )

set_bg_hack('pics/cover_v.png')

sys.path.insert(0, "..")
local_css("style.css")

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

st.title("🌞 Hello!")
text_1 = "Welcome to my 2024 "
text_2 = " collection"
st.markdown("### " + text_1 + str(annotation(" personal data", "", "#fea"))
            + text_2, unsafe_allow_html=True)
# st.markdown("<h3>" + text + str(annotation("apple", "", "#fea")) + "</h3>", unsafe_allow_html=True)
# st.write(st.secrets['connections'])

st.markdown("""<hr style="height:1px; border:none; color:#333; background-color:#333;"/>""", unsafe_allow_html=True)

#import streamlit.components.v1 as components
#components.html("""<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """)
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        🔍 Data is a lens through which we shape and interpret reality,
        bringing clarity to complex phenomena.
        
        ✍️ Self-reported data shares the same goal, yet shifts the focus,
        from the external world to our inner reality,
        revealing a narrative of who we are and the story we carry within.
        
        🌟 In this context, data visualization becomes a powerful tool for self-discovery,
        helping us see patterns that might otherwise remain hidden.
        
        🫐 Inspired by the concept of [Data Humanism](https://giorgialupi.com/data-humanism-my-manifesto-for-a-new-data-wold),
        this project explores the potential of small, subjective data.
        Over the past year, on a daily basis, I have been collecting data on a few key indicators,
        without a predefined goal, just out of curiosity, to experiment and see where it might lead.
        
        🧶 The daily practice of tracking data has been a valuable discovery itself:
        I practiced consistency, learned that this consistency works best
        when I track only a few indicators, resisted the urge to introduce changes
        to keep the collection simple and coherent, cursed myself when I forgot one or more days,
        and felt the satisfaction of steady progress. With each small step, I discovered the true
        impact of the journey, which is only
        visible in hindsight.
        """, unsafe_allow_html=True)

with col2:
    st.markdown(
        f"""
        🫧 Some relationships I aim to explore—my personal research questions—include:
        - How do I feel throughout the year? Is there a correlation between my emotions and months, days, or weekends?
        - Are my emotions influenced by my physical location? For example, how does going to the office affect my mood?
        - Is there a connection between watching movies and my emotional state?
        - How do I feel on days when I have a headache?
        - What about cross-influences? For instance, do specific days of the year correlate with movies, or do cities and movies affect each other?
        """, unsafe_allow_html=True)

st.markdown("""<hr style="height:1px; border:none; color:#333; background-color:#333;"/>""", unsafe_allow_html=True)
st.markdown(
    f"""
    🧑‍💻 From a technical point of view, the app is developed in [Streamlit](https://streamlit.io/),
    on open-source Python framework, to experiment with different libraries, graphical models, and interactive visualizations.
    """, unsafe_allow_html=True)
