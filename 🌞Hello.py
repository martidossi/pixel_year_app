import sys
from streamlit_gsheets import GSheetsConnection
import base64
import yaml
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils import *
from annotated_text import annotation
from itertools import product
import plotly.express as px
from pywaffle import Waffle


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

st.sidebar.subheader('(A Year in Pixel) legend')
st.sidebar.markdown("Colors used are based on the emotion wheel, except where otherwise specified.")
st.sidebar.markdown("""
    <span class='happy_square'></span> Happy <br>
    <span class='loved_square'></span> Loved <br>
    <span class='confident_square'></span> Confident <br>
    <span class='playful_square'></span> Playful <br>
    <span class='embarassed_square'></span> Embarassed <br>
    <span class='angry_square'></span> Angry <br>
    <span class='scared_square'></span> Scared <br>
    <span class='sad_square'></span> Sad <br>
    """, unsafe_allow_html=True
)
st.sidebar.markdown("""<hr style="height:2px; border:none; color:#333; background-color:#333;"/>""", unsafe_allow_html=True)

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

st.sidebar.markdown("""<hr style="height:2px; border:none; color:#333; background-color:#333;"/>""", unsafe_allow_html=True)

st.sidebar.subheader('📙 References')
st.sidebar.markdown("""
    *«Data collected from life can be a snapshot of the world
    in the same way that a picture catches small moments in time.»*
    """)
st.sidebar.image("pics/smalldata_bigdata_output.png", width=250)
st.sidebar.markdown("""
    - [Dear Data](https://www.dear-data.com/theproject), Giorgia Lupi and Stefanie Posavec.
    - [Feltron personal annual reports](http://feltron.com/), Nicholas Felton.
    """
    )
st.sidebar.subheader('Made with 🫶 in [Streamlit](https://streamlit.io/)')


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

# Title
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("# A Year in :rainbow[Pixel]")
    st.markdown("""#### A *pixel year* is a visual representation of personal emotions over the course of a year, with each day assigned a color that reflects the dominant mood or feeling for that day.""")
    st.markdown("""
        The [emotion wheel](https://humansystems.co/emotionwheels/) on the right represents the main guide for the project.
        I used its eight core emotions (four positive, four negative) to classify each day, with the outer emotions helping 
        to capture different shades of feeling. Here are a few more links that sparked ideas along the way.
        - [Happy Coding blog](https://happycoding.io/blog/year-in-pixels-2019)
        - [Celebrating Daily Joys](https://public.tableau.com/app/profile/qingyue.li8346/viz/CelebratingDailyJoysFindingLoveinEverydayLifeIronviz2024_Qingyue/Dashboard1)
        """)
with col2:
    st.markdown("#")
    st.image("pics/emotion-wheel.png")


conn = st.connection("gsheets", type=GSheetsConnection)
config_modebar = {'displayModeBar': False}

with open("config.yml", 'r') as f:
    cfg = yaml.safe_load(f)

# Heatmap
dict_emotion_id = cfg['map_emotion_id']
dict_emotion_color = cfg['map_emotion_color']

# Emotion df
df_emotion = conn.read(
    worksheet="pixel_year",
    ttl="10m",
    usecols=range(13),
    nrows=31
)
df_emotion = (
    df_emotion
    .rename(columns={'day/month': 'id_day'})
    .set_index('id_day')
    .fillna('0')
)
month_list = list(df_emotion.columns)
emotion_list = list(dict_emotion_color.keys())[2:]
positive_emotion_list = emotion_list[:4]
negative_emotion_list = emotion_list[4:]

# Mapping emotions to numbers
df_emotion_id = (
    pd.DataFrame([df_emotion[col].map(dict_emotion_id) for col in df_emotion.columns])
    .transpose()
    .fillna(0)
    .astype(int)
)
from matplotlib.patches import Patch

# Emotion intensity
df_intensity = conn.read(
    worksheet="pixel_year_intensity",
    ttl="10m",
    usecols=range(13),
    nrows=31
)
df_intensity = (
    df_intensity
    .rename(columns={'day/month': 'id_day'})
    .set_index('id_day')
    .fillna('0')
)

# Visualization
col1, _ = st.columns([3, 1])
with col1:
    tab1, tab2 = st.tabs(["Prevailing feeling", "Intensity"])
    with tab1:
        fig, ax = plt.subplots(figsize=(10, 10))
        ax = sns.heatmap(
            df_emotion_id.transpose(),
            cmap=list(dict_emotion_color.values()),
            cbar=False,
            linewidths=1.2,
            linecolor='white',
            square=True,
            vmin=0,
            vmax=len(dict_emotion_color),
            xticklabels=1,
            ax=ax
        )
        ax.set_yticklabels(labels=['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'], rotation=0, fontsize=8)
        ax.set_xticklabels(labels=list(df_emotion_id.index), rotation=0, fontsize=8)
        ax.set_xlabel('')
        for item in [fig, ax]:
            item.patch.set_visible(False)
        st.pyplot(fig, dpi=1000)
        #st.markdown('#')

    with tab2:
        labels = df_intensity.transpose().replace('0', '').replace('Missing', '').replace(':|', '')
        fig, ax = plt.subplots(figsize=(10, 10))
        ax = sns.heatmap(
            df_emotion_id.transpose(),
            cmap=list(dict_emotion_color.values()),
            cbar=False,
            linewidths=1.2,
            linecolor='white',
            square=True,
            vmin=0,
            annot=labels,
            fmt='',
            vmax=len(dict_emotion_color),
            xticklabels=1,
            ax=ax
        )
        ax.set_yticklabels(labels=['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'], rotation=0, fontsize=8)
        ax.set_xticklabels(labels=list(df_emotion_id.index), rotation=0, fontsize=8)
        ax.set_xlabel('')
        for item in [fig, ax]:
            item.patch.set_visible(False)
        st.pyplot(fig, dpi=1000)
        st.markdown("**Legenda**")
        st.markdown("""
        Feelings may be linked to various intensities. 
        Cells without any smile are just neutral, whereas positive pixels may be good :) or very good :)) days,
        as well as negative ones can be bad :( or very bad :(( days.
        """)

##########################

# Df monthly emotion
df_melt = df_emotion.melt()
df_melt = df_melt[(df_melt['value']!='0') & (df_melt['value']!='Missing')]
df_melt.columns = ['month', 'emotion']
df_melt['day'] = df_melt.groupby(['month']).cumcount()+1
df_count = df_melt[['month', 'emotion']].value_counts().reset_index()
df_count.columns = ['month', 'emotion', 'value']
df_month_emotion_base = pd.DataFrame(data=product(month_list, emotion_list), columns=['month', 'emotion'])
df_month_emotion_base['value'] = 0
df_month_emotion = (
    pd.merge(
        df_month_emotion_base,
        df_count,
        how='left',
        left_on=['month', 'emotion'],
        right_on = ['month', 'emotion'])
).fillna(0)
df_month_emotion['value'] = df_month_emotion.value_y.combine_first(df_month_emotion.value_x)
df_month_emotion = df_month_emotion.drop(['value_x', 'value_y'], axis=1)

# Treemap
st.markdown("""<hr style="height:1px; border:none; color:#333; background-color:#333;"/>""", unsafe_allow_html=True)
st.subheader('1. Relative number of days (%)')
st.markdown("""
    These visualizations show the overall proportion of each emotion across all observed days, 
    grouped into positive and negative categories.
    """)
df_n_days = df_month_emotion.groupby('emotion').agg({'value': sum}).reindex(emotion_list).reset_index()
df_n_days_pos = df_n_days[df_n_days.emotion.isin(positive_emotion_list)]
df_n_days_neg = df_n_days[df_n_days.emotion.isin(negative_emotion_list)]

df_n_days['perc_value'] = round(100*df_n_days.value/df_n_days.value.sum()).astype(int)
df_n_days['emotion_type'] = list(np.repeat('positive emotion', 4)) + list(np.repeat('negative emotion', 4))

dict_emotion_color_extended = dict_emotion_color
dict_emotion_color_extended.update({'(?)': 'white'})

tab1, tab2 = st.tabs(["Waffle chart", "Treemap"])
with tab1:
    col1, _ = st.columns([2, 1])
    with col1:
        df_n_days['perc_value'] = round(100*df_n_days['value']/df_n_days['value'].sum()).astype(int)
        df_n_days['emotion_type'] = list(np.repeat('positive emotion', 4)) + list(np.repeat('negative emotion', 4))
        df_waffle = df_n_days.sort_values(by=['emotion_type', 'perc_value'], ascending=[False, False])
        waffle_dict = df_waffle.set_index('emotion')[['perc_value']].to_dict()['perc_value']
        waffle_dict_new = {}
        for el in waffle_dict:
            waffle_dict_new[el] = dict_emotion_color[el]
        fig = plt.figure(
            FigureClass=Waffle,
            rows=10,
            columns=10,
            values=waffle_dict,
            colors=[str(el) for el in waffle_dict_new.values()],
            icon_style='solid',
            icon_legend=True,
            icons=['sun', 'sun', 'sun', 'sun', 'cloud-showers-heavy', 'cloud-showers-heavy', 'cloud-showers-heavy', 'cloud-showers-heavy'],
            block_arranging_style='snake',
            legend={
                'labels': [f"{k} ({v}%)" for k, v in waffle_dict.items()],
                'loc': 'upper left',
                'bbox_to_anchor': (1, 1),
                'framealpha': 0,
                'fontsize': 9,
            },
        )
        for item in [fig, ax]:
            item.patch.set_visible(False)
        st.pyplot(fig)
with tab2:
    col1, _ = st.columns([2, 1])
    with col1:
        fig = px.treemap(
            df_n_days,
            path=[px.Constant("all"), 'emotion_type', 'emotion'],
            values='value',
            color='emotion',
            color_discrete_map=dict_emotion_color_extended,
        )
        fig.update_layout(
            height=380,
            margin=dict(t=20, b=0, r=50),
        )
        fig.update_traces(
            marker=dict(cornerradius=2),
            marker_line_width=1,
            marker_line_color='black'
        )
        fig.data[0].textinfo = 'label+text+percent entry'
        fig.data[0].textinfo = 'label+text+percent entry'
        fig.data[0].hovertemplate = 'emotion=%{label}<br>number of days=%{value}'

        st.plotly_chart(fig, config=config_modebar)

####################

# Trend over time
st.markdown("""<hr style="height:1px; border:none; color:#333; background-color:#333;"/>""", unsafe_allow_html=True)
st.subheader('2. Trend over time')

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    This visualization shows how emotions change over time, displaying the number of days each emotion is felt in different months.
    The widget on the right lets you select and highlight specific emotions.
    """)
with col2:
    sel_status = st.multiselect("Pick one or more emotions:", emotion_list, [])
fig = px.line(
    df_month_emotion,
    x="month",
    y="value",
    color="emotion",
    color_discrete_map=dict_emotion_color,
    template="simple_white"
)
if len(sel_status) >= 1:
    for d in fig['data']:
        if d['name'] in sel_status:
            d['line']['color'] = dict_emotion_color[d['name']]
            d['line']['width'] = 3
        if d['name'] not in sel_status:
            d['line']['color'] = 'lightgrey'
fig.update_layout(
    font=dict(
        family="IBM Plex Sans",
        size=12
    ),
    legend_title_font_color="black",
    height=380,
    xaxis_title="",
    yaxis_title="number of days",
    xaxis=dict(showgrid=True, tickcolor='black', color='black'),
    yaxis=dict(showgrid=True, tickcolor='black', color='black'),
    margin=dict(t=20),
)
fig.update_xaxes(showline=True, linewidth=1, linecolor='black')
fig.update_yaxes(showline=True, linewidth=1, linecolor='black')
st.plotly_chart(fig, config=config_modebar)

st.markdown("##### Visualizing totals")
st.markdown("""
    This visualization captures the emotional composition of each month by summing up all the emotions.
    The two visual models, designed with identical data and purpose, are for comparison and experimentation *–and
    because, for different reasons, I liked both* (which one do you think works better?).
""")
with st.expander("Some thoughts:"):
    st.markdown("""
           - The bar chart is very effective in providing a complete picture of the data,
           despite the challenge of comparing internal values that do not share a common baseline.
           - On the other hand, the radial chart is aesthetically more pleasing and interesting
           ([why do we find circles so beautiful?](https://www.sciencefocus.com/science/why-do-we-find-circles-so-beautiful)).
           However, upon closer look, you can see how it really distorts reality:
           the way it's set up, the inner groups don't get enough representation, which makes the whole data
           look skewed. (more about the importance of the inner circle
           [here](https://www.data-to-viz.com/caveat/circular_bar_yaxis.html)).
       """)

tab1, tab2 = st.tabs(["Stacked bar chart", "Radial stacked bar chart"])
with tab1:
    fig = px.bar(
        df_month_emotion,
        x="month",
        y="value",
        color="emotion",
        color_discrete_map=dict_emotion_color,
        template="simple_white",
    )
    fig.update_layout(
        font=dict(
            family="IBM Plex Sans",
            size=12,
        ),

        legend_title_font_color="black",
        height=380,
        xaxis_title="",
        yaxis_title="number of days",
        xaxis=dict(showgrid=True, tickcolor='black', color='black'),
        yaxis=dict(showgrid=True, tickcolor='black', color='black'),
        margin=dict(t=20),
        bargap=0
    )
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black')
    st.plotly_chart(fig, config=config_modebar)
with tab2:
    hole_val = st.slider(
        "How much changing the size of the inner circle affect the proportion of the colored areas?",
        min_value=0.0, max_value=1.0, value=0.0
    )
    fig = px.bar_polar(
        df_month_emotion,
        r="value",
        theta="month",
        color="emotion",
        color_discrete_map=dict_emotion_color
    )
    fig.update_layout(
        font=dict(
            family="IBM Plex Sans",
            size=12,
        ),
        margin=dict(t=20),
        height=380,
        legend_title_font_color="black",
        polar=dict(
            bgcolor="white",
            hole=hole_val,
            radialaxis=dict(
                gridcolor='lightgray',
                griddash='dot',
                tickcolor='black',
                tickfont_color='black'
                ),
            angularaxis=dict(
                linecolor='black',
                gridcolor='gray',
            )
        ),
    )
    if hole_val > 0.05:
        fig.update_polars(radialaxis_ticks="")
        fig.update_polars(radialaxis_showticklabels=False)
    st.plotly_chart(fig, config=config_modebar)