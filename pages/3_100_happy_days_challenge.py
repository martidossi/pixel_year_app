import base64
import streamlit as st
from st_clickable_images import clickable_images
import glob as glob

st.markdown(
    """
    <style>
    img {
        cursor: pointer;
        transition: all .2s ease-in-out;
    }
    img:hover {
        transform: scale(1.2);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

image_list = glob.glob('pics_100_days/original/*.png')
# colored images
image_list_col = glob.glob('pics_100_days/color/*.png')

desc = ['immagine 1', 'immagine 2']
dict_images = dict(zip(image_list_col, image_list))
dict_images_desc = dict(zip(image_list_col, desc))

# st.write(image_list, image_list_col, dict_images, dict_images_desc)
images = []
for file in image_list_col:
    with open(file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
        images.append(f"data:image/jpeg;base64, {encoded}")

titles = desc
clicked = clickable_images(
    images,
    titles=titles,
    div_style={
        "display": "flex",
        "justify-content": "center",
        "flex-wrap": "wrap",
        "cursor": "pointer",
        "transition": "all .2s ease-in-out",
    },
    img_style={"margin": "5px", "height": "200px"},
)

# st.markdown(f"Image #{clicked} clicked" if clicked > -1 else "No image clicked")
map_image = f"pics_100_days/color/img_c_{clicked}.png"
st.sidebar.image(dict_images[map_image])
st.sidebar.write(dict_images_desc[map_image])