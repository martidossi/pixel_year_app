import streamlit as st
import glob
import base64
from st_clickable_images import clickable_images
from streamlit_gsheets import GSheetsConnection
import sys
from utils import *


sys.path.insert(0, "..")
local_css("style.css")

st.title("🌈 100 Happy Days challenge")
st.markdown("""
    This year, inspired by a close friend, I decided to take on this challenge for the last 100 days of 2024. 
    
    *“This challenge is about training your perception on things.”* [...] 
    *“It’s a fantastic reality check —you can’t always change the course of events, but you can always adapt your perception of it all.”*
     [URL](https://buffer.com/resources/100-happy-days-challenge/)
    
    The challenge is not about being happy every single day; rather, it’s about uncovering small moments of gratitude, like a glimmer of positivity to hold onto.
    Even on days when such moments seem out of reach, they are always there, quietly waiting to be noticed. 
    It could be as simple as a kind gesture or a fleeting experience that brings a smile or a sense of hope that tough times will pass.
    Day by day, I’ve found how nurturing this habit of appreciating little things can profoundly shape how we navigate life
     as an intentional practice of creating joy and embracing the beauty of life’s uncertainties.
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
def load_data(worksheet_name, n_cols, n_rows):
    df = conn.read(
        worksheet=worksheet_name,
        ttl="10m",
        usecols=range(n_cols),
        nrows=n_rows
    )
    return df

df = load_data("100happydays", 6, 100)

@st.cache_data
def encode_images_to_base64(image_paths):
    encoded_images = []
    for file in image_paths:
        with open(file, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()
            encoded_images.append(f"data:image/jpeg;base64,{encoded}")
    return encoded_images

output_images = glob.glob("happy_days_pics/output/*.png")
view_images = sorted(output_images)
del view_images[9]
view_images.append("happy_days_pics/output/_pic100_col.png")
images = encode_images_to_base64(view_images)

image_id = clickable_images(
    images,
    #titles=[f"pic #{str(i+1)}" for i in range(len(images))],
    div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
    img_style={"margin": "1px", "height": "100px", "cursor": "pointer", "border-radius": "0px"},
)
# st.markdown(f"Image #{image_id} clicked" if clicked > -1 else "No image clicked")
# Display image with rounded borders using custom CSS

# Path to the image
image_path = "your_image_path_here.jpg"

# Display the image with the custom class
st.sidebar.subheader(f'📸 Selected pic #{image_id+1}')
if image_id == -1:
    st.sidebar.markdown(f"No image selected.")
else:
    # st.sidebar.markdown(f'<img src="{images[image_id]}" class="rounded-image" width="250"/>', unsafe_allow_html=True)
    st.sidebar.markdown(f"""<p class="consolas-font">{df.loc[image_id, 'event_description']}</p>""", unsafe_allow_html=True)
    st.sidebar.markdown(f"""
        <p class="consolas-font">
        {df.loc[image_id, 'weekday']}, {df.loc[image_id, 'day']}, {df.loc[image_id, 'place']}</p>""",
        unsafe_allow_html=True)
    image_tag = df.loc[image_id, 'tag']
    st.sidebar.markdown(f"""
        <p style="display:inline; vertical-align:middle;">
            <span class='{image_tag}_square' style="display:inline-block; vertical-align:middle;"></span>
            <span class="consolas-font">{image_tag.capitalize()}</span>
        </p>
        """, unsafe_allow_html=True)
st.sidebar.markdown("""<hr style="height:1px; border:none; color:#333; background-color:#333;"/>""",
                    unsafe_allow_html=True)
st.sidebar.subheader('🔍 How to read')

st.sidebar.markdown("""
    **Color legend** | Below is the full list of categories and corresponding colors used to classify pictures.
    """)
st.sidebar.markdown("""
    <span class='family_square'></span> Family <br>
    <span class='friends_square'></span> Friends <br>
    <span class='flowers_square'></span> Flowers <br>
    <span class='food_square'></span> Food <br>
    <span class='dataviz_square'></span> Dataviz <br>
    <span class='other_square'></span> Other <br>
    """, unsafe_allow_html=True
)

st.sidebar.markdown("""<hr style="height:2px; border:none; color:#333; background-color:#333;"/>""", unsafe_allow_html=True)
st.sidebar.subheader('📙 References')
# st.sidebar.subheader('📙 References')
url_video = "https://www.youtube.com/watch?v=J4UtPDaR3cA"
st.sidebar.video(url_video)
st.sidebar.markdown("""[100 Happy Days](https://100happydays.com/), Dmitry Golubnichy.""")
st.sidebar.subheader("""
    小確幸 «shōgakkō» Small but Certain Happinesses

    The concept of “shōgakkō” was introduced by Japanese author Haruki Murakami in his 1986 essay “Afternoon in the Islets of Langerhans”.
    He described these small, tangible joys as moments like eating a freshly baked loaf of bread with bare hands,
    opening a drawer to see neatly folded underwear, slipping into a new shirt with the scent of clean cotton,
    or hearing the rustle of a cat settling into bed.
""")
st.sidebar.markdown("""
    <span style="font-size:13px; font-style:italic;">Life’s Little Instruction Book: 1137.
    Be happy with what you have while working for what you want.
    [Letterina](https://letterina.substack.com/).</span>
""", unsafe_allow_html=True)
st.sidebar.markdown("""
    <span style="font-size:13px; font-style:italic;">Be content with what you have; rejoice in the way things are.
    When you realize there is nothing lacking, the whole world belongs to you. Lao Tzu. [Zen Habits](https://zenhabits.net/perfect/).
""", unsafe_allow_html=True)
