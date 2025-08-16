import sys

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import yaml
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils import local_css
# from annotated_text import annotation
from itertools import product
import plotly.express as px
from pywaffle import Waffle
import datetime
from time import strptime

# Custom plots
from viz_functions import days_emotion_chart

## Setting
st.set_page_config(
    page_title="Hello",
    page_icon="🟧",
    layout="wide"
)
# st.image("pics/cover.png")
#set_bg_hack('pics/cover_v.png')

sys.path.insert(0, "..")
local_css("style.css")

st.sidebar.subheader('🔍 How to read')

st.sidebar.markdown("""
    **Color legend** – Below are the colors used in the visualizations, which are based on the
    **emotion wheel** developed by [Human Systems](https://humansystems.co/emotionwheels/).
    """)
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

with st.sidebar.expander("See the emotion wheel:"):
    st.image("pics/emotion-wheel.png")# width=300)
st.sidebar.markdown("""<hr style="height:2px; border:none; color:#333; background-color:#333;"/>""", unsafe_allow_html=True)

st.sidebar.subheader('🌸 About me')
# st.sidebar.image("pics/profile_pic.png", width=250)
st.sidebar.markdown("""
    My name is Martina, I'm from Italy and currently based in Utrecht (NL). After studying statistics and working as data scientist
    for 5+ years, I am pursuing a PhD in Information and Computing Sciences at the University of Utrecht, as part of the 
    [VIG group](https://www.projects.science.uu.nl/ics-vig/Main/HomePage) (to know more about my research project: [VR4eVR](https://vr4evr.nl/)).
    """)
st.sidebar.subheader('💌 Contacts')
st.sidebar.markdown("""
    If you have any questions, feedback of any kind, I'd be delighted to connect.
    Feel free to reach out to me!
    - martinadossi.hello at gmail.com
    - [Personal website](https://martina-dossi.notion.site/Hi-I-m-Martina-6c1e9636b59245cd8cfedc1fffd05a1b),
    [LinkedIn](https://www.linkedin.com/in/martina-dossi/), [Instagram](https://www.instagram.com/adatastory_/), [Behance](https://www.behance.net/martinadossi)
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
    - [Happy Coding blog](https://happycoding.io/blog/year-in-pixels-2019), Happy Coding Blog.
    - [Celebrating Daily Joys](https://public.tableau.com/app/profile/qingyue.li8346/viz/CelebratingDailyJoysFindingLoveinEverydayLifeIronviz2024_Qingyue/Dashboard1), Qingyue Li.
    """
    )
st.sidebar.image("pics/feelings.jpeg")
st.sidebar.caption("Mansi Jikadara B [@thetypewriterdaily](https://www.instagram.com/thetypewriterdaily/)")
st.sidebar.subheader("Made with 🫶 in Streamlit.")
st.sidebar.markdown(
    "[![Made with Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)"
)

st.markdown(
    """
    <style>
    .big-font {
        font-size: 100px !important;

    }
    </style>
    """,
    unsafe_allow_html=True,
)
#st.markdown("<p class='big-font'>😊</p>", unsafe_allow_html=True)

text_1 = "This is my 2024 "
text_2 = " collection."
st.header('Hello! 🌞')
#st.markdown("### " + text_1 + str(annotation(" personal data", "", "#fea"))
#            + text_2, unsafe_allow_html=True)

st.subheader('Welcome to my 2024 personal data collection & visualization.')
st.markdown("""
    All through 2024, I collected tiny bits of data each day, using a simple form I set up at the start 
    of the year. What started as a five-minute daily experiment in self-reflection slowly turned into a
    habit I didn’t want to skip.
    Now, with a year’s worth of little traces behind me, I’m excited to dig
    in and see the patterns that may have quietly unfolded along the way. ✨
    """)  

col1, col2 = st.columns([1, 1], gap='large')
with col1:
    with st.container(border=True):
        st.markdown("""
            #### ⚠️ Heads up! 👀
            - For full functionality, please view this on a desktop –some features might look a bit off on mobile.
            - Keep in mind: the sidebar on the left is often part of the visualizations.        
        """)
with col2:
    st.markdown('#### Check out the other pages for the full story:')
    st.page_link("pages/1_💫_Everything.py", label="Everything", icon="💫")
    st.page_link("pages/2_🌈100_Happy_Days_challenge.py", label="100 Happy Days challenge", icon="🌈")
    st.page_link("pages/3_📌Notes.py", label="Notes", icon="📌")

st.markdown("""<hr style="height:1px; border:none; color:#333; background-color:#333;"/>""", unsafe_allow_html=True)

# st.markdown("<h3>" + text + str(annotation("apple", "", "#fea")) + "</h3>", unsafe_allow_html=True)
# st.write(st.secrets['connections'])
# import streamlit.components.v1 as components
# components.html("""<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """)

# st.markdown("""<hr style="height:1px; border:none; color:#333; background-color:#333;"/>""", unsafe_allow_html=True)

# connection to g spreadsheet and data loading
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

# config
with open("config.yml", 'r') as f:
    cfg = yaml.safe_load(f)

dict_emotion_id = cfg['map_emotion_id']
dict_emotion_color = cfg['map_emotion_color']
config_modebar = {'displayModeBar': False}

# Movies & journaling
df_movies = load_data("journaling_movies", 3, 45)
st.session_state.df_movies = df_movies

df_place = load_data("where_i_am", 13, 31)
st.session_state.df_place = df_place

# Emotion df
df_emotion = load_data("pixel_year", 13, 31)
df_emotion = (
    df_emotion
    .rename(columns={'day/month': 'id_day'})
    .set_index('id_day')
    .fillna('0')
)
st.session_state.df_emotion = df_emotion

month_list = list(df_emotion.columns)
emotion_list = list(dict_emotion_color.keys())[2:]
positive_emotion_list = emotion_list[:4]
negative_emotion_list = emotion_list[4:]

# Emotion intensity
df_intensity = load_data("pixel_year_intensity", 13, 31)
df_intensity = (
    df_intensity
    .rename(columns={'day/month': 'id_day'})
    .set_index('id_day')
    .fillna('0')
)
st.session_state.df_intensity = df_intensity

# Mapping emotions to numbers
df_emotion_id = (
    pd.DataFrame([df_emotion[col].map(dict_emotion_id) for col in df_emotion.columns])
    .transpose()
    .fillna(0)
    .astype(int)
)
st.session_state.df_emotion_id = df_emotion_id

# Title
st.markdown("# A Year in :rainbow[Pixel]")

# Visualization
col1, col2 = st.columns([1, 1], gap='large')
with col1:
    st.markdown("""
        A *pixel year* is a visual representation of personal emotions throughout a year,
        where each day is associated with a color that reflects the dominant mood or feeling of that day.
        For this project, I used the emotion wheel in the sidebar as my primary reference.
        I primarily relied on its eight core emotions (four positive and four negative) to classify each day,
        using the outer emotions to capture subtle variations in feelings, even if they were not explicitly recorded.
        """)
with col2:
    st.markdown("""
        Each day, I tracked both the prevailing feeling and the related intensity (see the two tabs below). 
        Squares without any smile are just neutral, whereas positive pixels may be good `:)` or very good `:))` days,
        as well as negative ones can be bad `:(` or very bad `:((` days.
        """)
col1, _ = st.columns([4, 2], gap='large')
with col1:
    tab1, tab2 = st.tabs(["Prevailing feeling", "Intensity"])
    with tab1:
        fig, ax = plt.subplots(figsize=(10, 10))
        ax = sns.heatmap(
            df_emotion_id.transpose(),
            cmap=list(dict_emotion_color.values()),
            cbar=False,
            linewidths=1.4,
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
        st.pyplot(fig, dpi=1000, use_container_width=True)
        #st.markdown('#')

    with tab2:
        labels = df_intensity.transpose().replace('0', '').replace('Missing', '').replace(':|', '')
        fig, ax = plt.subplots(figsize=(10, 10))
        ax = sns.heatmap(
            df_emotion_id.transpose(),
            cmap=list(dict_emotion_color.values()),
            cbar=False,
            linewidths=1.4,
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
        st.pyplot(fig, dpi=1000, use_container_width=True)


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
st.subheader('How often have I experienced each feeling?')
st.markdown("""
    These visualizations offer two compact views to inspect the weight of each emotion over all observed days, 
    grouped into positive and negative categories.
    """)
df_n_days = df_month_emotion.groupby('emotion').agg({'value': sum}).reindex(emotion_list).reset_index()
df_n_days_pos = df_n_days[df_n_days.emotion.isin(positive_emotion_list)]
df_n_days_neg = df_n_days[df_n_days.emotion.isin(negative_emotion_list)]

df_n_days['perc_value'] = round(100*df_n_days.value/df_n_days.value.sum()).astype(int)
df_n_days['emotion_type'] = list(np.repeat('positive emotion', 4)) + list(np.repeat('negative emotion', 4))

dict_emotion_color_extended = dict_emotion_color
dict_emotion_color_extended.update({'(?)': 'white'})

df_n_days['perc_value'] = round(100 * df_n_days['value'] / df_n_days['value'].sum()).astype(int)
df_n_days['emotion_type'] = list(np.repeat('positive emotion', 4)) + list(np.repeat('negative emotion', 4))
df_waffle = df_n_days.sort_values(by=['emotion_type', 'perc_value'], ascending=[False, False])
waffle_dict = df_waffle.set_index('emotion')[['perc_value']].to_dict()['perc_value']
waffle_dict_new = {}
for el in waffle_dict:
    waffle_dict_new[el] = dict_emotion_color[el]

col1, col2 = st.columns([1, 2], gap="large")
with col1:
    tab1, tab2 = st.tabs(["A waffle chart", "Just percentages"])
    with tab1:
        fig = plt.figure(figsize=(4, 5))
        ax = fig.add_subplot(111)
        ax.set_aspect(aspect="equal")
        Waffle.make_waffle(
            ax=ax,
            FigureClass=Waffle,
            rows=10,
            columns=10,
            values=waffle_dict,
            colors=[str(el) for el in waffle_dict_new.values()],
            icon_style='solid',
            icon_legend=True,
            icon_size='large',
            icons=['sun', 'sun', 'sun', 'sun', 'cloud-showers-heavy', 'cloud-showers-heavy', 'cloud-showers-heavy',
                   'cloud-showers-heavy'],
            block_arranging_style='snake',
            # legend={
            #    'labels': [f"{k} ({v}%)" for k, v in waffle_dict.items()],
            #   'loc': 'upper left',
            #    'bbox_to_anchor': (1, 1),
            #    'framealpha': 0,
            #    'fontsize': 5,
            # }
        )
        ax.get_legend().remove()
        for item in [fig, ax]:
            item.patch.set_visible(False)
        st.pyplot(fig, dpi=1000, use_container_width=True)
    with tab2:
        col11, col12, _ = st.columns([1, 1, 1])
        col11.metric(list(waffle_dict.keys())[0], f'{list(waffle_dict.values())[0]}%')
        col11.metric(list(waffle_dict.keys())[1], f'{list(waffle_dict.values())[1]}%')
        col11.metric(list(waffle_dict.keys())[2], f'{list(waffle_dict.values())[2]}%')
        col11.metric(list(waffle_dict.keys())[3], f'{list(waffle_dict.values())[3]}%')
        col12.metric(list(waffle_dict.keys())[4], f'{list(waffle_dict.values())[4]}%')
        col12.metric(list(waffle_dict.keys())[5], f'{list(waffle_dict.values())[5]}%')
        col12.metric(list(waffle_dict.keys())[6], f'{list(waffle_dict.values())[6]}%')
        col12.metric(list(waffle_dict.keys())[7], f'{list(waffle_dict.values())[7]}%')
with col2:
    col1, _ = st.columns([3, 1])
    with col1:
        tab1, tab2 = st.tabs(["A tree map", "-"])
        with tab1:
            fig = px.treemap(
                df_n_days,
                path=[px.Constant("all"), 'emotion_type', 'emotion'],
                values='value',
                color='emotion',
                color_discrete_map=dict_emotion_color_extended,
            )
            fig.update_layout(
                height=300,
                margin=dict(t=1, b=0, r=1)
            )
            fig.update_traces(
                marker=dict(cornerradius=2),
                marker_line_width=1,
                marker_line_color='black'
            )
            fig.data[0].textinfo = 'label+text+percent entry'
            fig.data[0].textinfo = 'label+text+percent entry'
            fig.data[0].hovertemplate = 'emotion=%{label}<br>number of days=%{value}'
            st.plotly_chart(fig, config=config_modebar, use_container_width=True)
st.markdown("From the chart, it seems I've been *happy* most of the time. But what do I mean by *happy*?")
st.markdown("""
    These emotions reflect the predominant feeling that shaped the background of each day, rather than its intensity.
    For intensity, I referred to the *smiley* scale (see the chart above), which captures peak moments,
    both positive and negative. Therefore, happy days without an intensity marker are simply days when I felt *okay*,
    with a general sense of calm and balance.
    """)

####################

# Trend over time
st.markdown("""<hr style="height:1px; border:none; color:#333; background-color:#333;"/>""", unsafe_allow_html=True)
st.subheader('Trend over time')
st.markdown("""
How have I been feeling over time?
This chart shows how my emotions have changed month by month, tracking the number of days I experienced each one.
I was surprised to see how happy I felt during the summer months, even though I usually feel most at ease during
winter and cold weather (here, other hidden factors played a major role).
""")
col1, _ = st.columns([2, 1])
with col1:
    #sel_status = st.multiselect("Pick one or more emotions:", emotion_list, [])
    sel_status = []
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
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        legend_title_font_color="black",
        height=380,
        xaxis_title="",
        yaxis_title="number of days",
        xaxis=dict(showgrid=False, tickcolor='black', color='black', linewidth=1, gridwidth=1, gridcolor='darkgray'),
        yaxis=dict(showgrid=True, tickcolor='black', color='black', linewidth=1, gridwidth=1, gridcolor='darkgray'),
        margin=dict(t=20),
        showlegend=False
    )
    st.plotly_chart(fig, config=config_modebar, dpi=1000, use_container_width=True)

st.markdown("##### Visualizing totals")
st.markdown("""
    These visualizations capture the emotional composition of each month by summing up all the emotions.
    The two visual models, designed with identical data and purpose, are for comparison and experimentation.
    For different reasons, I like both of them, although they work quite differently
    (which one do you think works better?).
""")

col1, _ = st.columns([2, 1])
with col1:
    tab1, tab2, tab3 = st.tabs(["Stacked bar chart", "Radial stacked bar chart", "Thoughts"])
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
            plot_bgcolor="rgba(0, 0, 0, 0)",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            legend_title_font_color="black",
            height=380,
            xaxis_title="",
            yaxis_title="number of days",
            xaxis=dict(showline=True, linewidth=1, linecolor='black', showgrid=False),
            yaxis=dict(showline=True, linewidth=1, linecolor='black', showgrid=False),
            margin=dict(t=20),
            bargap=0,
            showlegend=False
        )
        st.plotly_chart(fig, config=config_modebar)
    with tab2:
        hole_val = st.slider(
            "Explore how much changing the size of the inner circle affect the proportion of the colored areas. 👇",
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
            plot_bgcolor="rgba(0, 0, 0, 0)",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            showlegend=False,
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

    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
                - The bar chart is very effective in providing a complete picture of the data,
                despite the challenge of comparing internal values that do not share a common baseline.
                   """)
        with col2:
            st.markdown("""
                - The radial chart is aesthetically more pleasing and interesting
                ([why do we find circles so beautiful?](https://www.sciencefocus.com/science/why-do-we-find-circles-so-beautiful)).
                This said, it distorts reality: by construction, the inner groups are never well represented, which makes
                the whole data look skewed (more about this
                [here](https://www.data-to-viz.com/caveat/circular_bar_yaxis.html)).
               """)
        st.markdown("#")

######## days viz
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
# Dropped emotions that are not used
dict_emotion_id_2 = {
    'Happy': 1,
    'Loved': 2,
    'Confident': 3,
    'Playful': 4,
    'Scared': 5,
    'Sad': 6,
    'Angry': 7
}
df_days = df_melt.copy()
df_days['month_abb'] = [el[:3] for el in df_melt.month]
df_days['month_id'] = df_days['month_abb'].apply(lambda x: strptime(x,'%b').tm_mon)
df_days['date'] = [datetime.datetime(year=2024, month=el[0], day=el[1]) for el in zip(df_days.month_id, df_days.day)]
df_days['weekday_id'] = df_days['date'].apply(lambda x: x.weekday()+1)
df_days['weekday'] = df_days['date'].apply(lambda x: days[x.weekday()])
df_days['emotion_id'] = df_days.emotion.map(dict_emotion_id_2)
df_days_counts = df_days[['weekday', 'emotion']].value_counts().reset_index()
df_days_counts.columns = ['weekday', 'emotion', 'count']
df_agg_weekday = df_days.weekday.value_counts().reset_index()
df_agg_weekday.columns = ['weekday', 'n_weekday']
df_agg_emotion = df_days.emotion.value_counts().reset_index()
df_agg_emotion.columns = ['emotion', 'n_emotion']

df_days_counts = df_days_counts.merge(df_agg_weekday, on='weekday', how='left')
df_days_counts = df_days_counts.merge(df_agg_emotion, on='emotion', how='left')
df_days_counts['perc_emotion'] = df_days_counts['count']*100/df_days_counts['n_emotion']
df_days_counts['perc_weekday'] = df_days_counts['count']*100/df_days_counts['n_weekday']
df_days_counts['emotion_color'] = df_days_counts.emotion.map(dict_emotion_color)

st.markdown("##### Trend by weekday")
st.markdown("""
    What's my fav day of the week? 
    The two charts below both show the trends of my emotional states day by day.
    I’ve represented them twice, to get insights from different perspectives.
    In the first chart, counts are normalized by day of the week, to show the percentages
    of different emotions each day (with the sum for each day equaling 100%).
    In the second, counts are normalized by emotion, to highlight the distribution of days on
    which I felt each emotion (with the sum for each emotion also equaling 100%).
    """)
col1, _ = st.columns([4, 1])
with col1:
    col1, col2 = st.columns([1, 1])
    with col1:
        tab1, _ = st.tabs(["Count normalized by day of the week:", "-"])
        with tab1:
            days_emotion_chart(
                df_days_counts, perc_feature='perc_weekday', days_list=days, emotions_list=list(dict_emotion_id_2.keys()), config_modebar=config_modebar
            )
    with col2:
        tab1, _ = st.tabs(["Count normalized by emotion:", "-"])
        with tab1:
            days_emotion_chart(
                df_days_counts, perc_feature='perc_emotion', days_list=days, emotions_list=list(dict_emotion_id_2.keys()), config_modebar=config_modebar
            )

