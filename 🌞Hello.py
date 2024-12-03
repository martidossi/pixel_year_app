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
import plotly.graph_objects as go
from pywaffle import Waffle
import datetime
from time import strptime


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

#set_bg_hack('pics/cover_v.png')

sys.path.insert(0, "..")
local_css("style.css")

st.sidebar.subheader('(A Year in Pixel) legend')
st.sidebar.markdown("The colors below are those used in the *pixel-year-related* visualizations and are based on the "
                    "**emotion wheel** developed by [Human Systems](https://humansystems.co/emotionwheels/).")
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
    My name is Martina and I am currently based in Italy, where I work as data scientist.
    I'm a statistician by background and, over the past years, I developed a strong interest in information design and data visualization. 
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
    - [Happy Coding blog](https://happycoding.io/blog/year-in-pixels-2019), Happy Coding Blog.
    - [Celebrating Daily Joys](https://public.tableau.com/app/profile/qingyue.li8346/viz/CelebratingDailyJoysFindingLoveinEverydayLifeIronviz2024_Qingyue/Dashboard1), Qingyue Li.
    """
    )
st.sidebar.subheader('Made with 🫶 in [Streamlit](https://streamlit.io/)')


st.title("🌞 Ciao!")
text_1 = "Welcome to my 2024 "
text_2 = " collection"
st.markdown("### " + text_1 + str(annotation(" personal data", "", "#fea"))
            + text_2, unsafe_allow_html=True)
# st.markdown("<h3>" + text + str(annotation("apple", "", "#fea")) + "</h3>", unsafe_allow_html=True)
# st.write(st.secrets['connections'])

st.markdown("""<hr style="height:1px; border:none; color:#333; background-color:#333;"/>""", unsafe_allow_html=True)

#import streamlit.components.v1 as components
#components.html("""<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """)
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
    st.markdown(
        f"""
        🫧 Some relationships I aim to explore—my personal research questions—include:
        - How do I feel throughout the year? Is there a correlation between my emotions and months, days, or weekends?
        - What is my favourite days? How do I feel during weekends? Which season brings me the most happiness?
        - Are my emotions influenced by my physical location? For example, how does going to the office affect my mood?
        - Is there a connection between watching movies and my emotional state?
        - What about cross-influences? For instance, do specific days of the year correlate with movies, or do cities and movies affect each other?
        """, unsafe_allow_html=True)
    st.markdown("**Explore the other pages:**")
    st.page_link("pages/1_🎞Movies.py", label="Movies", icon="🎞")
    st.page_link("pages/2_🌈100_Happy_days_challenge.py", label="100 Happy days challenge", icon="🌈")
    st.page_link("pages/3_📌Take-aways.py", label="Take-aways", icon="📌")

st.markdown("""<hr style="height:1px; border:none; color:#333; background-color:#333;"/>""", unsafe_allow_html=True)

# Title
st.markdown("# A Year in :rainbow[Pixel]")
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
col1, col2 = st.columns([1, 1], gap='large')
with col1:
    st.markdown("""
        A *pixel year* is a visual representation of personal emotions over the course of a year, 
        where each day is assigned to the color that reflects the dominant mood or feeling of that day.
        I considered the emotion wheel in the sidebar as main reference for the project.
        In particular, I relied on its eight core emotions (four positive, four negative) to classify each day, 
        with the outer emotions helping to capture different shades of feeling. 
        """)
with col2:
    st.markdown("""
        Each day, I tracked both the prevailing feeling and the related intensity (see the two tabs). 
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
st.markdown("Luckily, I've been happy most of the time!")
st.markdown("""
*A quick note on what I mean by *happy*, as these emotions reflect the predominant feeling in the
background of each day, and not its intensity. For that, I used the smiley scale (see the chart above) 
that captures peak moments, whether positive or negative. So, *happy* days without an intensity marker
are simply days when I felt *okay*, with an overall sense of calm and balance.
""")

####################

# Trend over time
st.markdown("""<hr style="height:1px; border:none; color:#333; background-color:#333;"/>""", unsafe_allow_html=True)
st.subheader('Trend over time')
st.markdown("""
How have I been feeling over time?
This chart shows how my emotions have changed month by month, counting the days I felt each one.
Surprisingly, even though I'm a winter person, it looks like I really enjoyed the summer months,
especially July —which turned out to be the happiest month!
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

######## days viz
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
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

df_agg_weekday = df_days.weekday.value_counts().reset_index()
df_agg_weekday.columns = ['weekday', 'n_weekday']
df_agg_emotion = df_days.emotion.value_counts().reset_index()
df_agg_weekday.columns = ['emotion', 'n_emotion']
#st.dataframe(df_agg_weekday)
#st.dataframe(df_agg_emotion)
#st.dataframe(df_days_counts)
df_days_counts = df_days_counts.merge(df_agg_weekday, on='weekday', how='left')
#df_days_counts = df_days_counts.set_index('weekday').join(df_agg_weekday.set_index('weekday'), how='left', lsuffix='_left', rsuffix='_right').reset_index()
df_days_counts = df_days_counts.merge(df_agg_emotion, on='emotion', how='left')
#df_days_counts = df_days_counts.set_index('emotion').join(df_agg_emotion.set_index('emotion'), how='left', lsuffix='_left', rsuffix='_right').reset_index()
st.dataframe(df_days_counts)
df_days_counts['perc_emotion'] = df_days_counts['count']*100/df_days_counts['n_emotion']
df_days_counts['perc_weekday'] = df_days_counts['count']*100/df_days_counts['n_weekday']
df_days_counts['emotion_color'] = df_days_counts.emotion.map(dict_emotion_color)

def days_emotion_chart(df_days_counts, perc_feature):
    fig = go.Figure()

    # Add the scatter trace
    fig.add_trace(
        go.Scatter(
            x=df_days_counts.weekday,
            y=df_days_counts.emotion,
            mode='markers',
            marker=dict(
                symbol='square',
                color=df_days_counts.emotion_color,
                size=df_days_counts[perc_feature],
                sizemode='area',
                sizeref=2. * max(df_days_counts[perc_feature]) / (40. ** 2),
                sizemin=4
            ),
            text=df_days_counts['count'],  # Optional if you want additional hover details
            hovertemplate=(
                "weekday=%{x}<br>"
                "emotion=%{y}<br>"
                "number of times=%{text}<br>"  # Absolute value
                "percentage=%{marker.size:.2f}%"  # Use size for percentage
            )
        )
    )

    # Set the aspect ratio to 1:1
    fig.update_layout(
        xaxis=dict(
            categoryorder="array",  # Sort by array order
            categoryarray=days,  # Specify the order
        ),
        yaxis=dict(
            categoryorder="array",  # Sort by array order
            categoryarray=list(dict_emotion_id_2.keys()),  # Specify the order
        ),
        autosize=False,
        width=300,  # Fixed width
        height=400,  # Fixed height
        margin=dict(l=0, r=0, t=0, b=60),  # Margins
        template="plotly_white",  # Clean look
        scene=dict(aspectmode="cube")  # Enforce equal scaling for all axes
    )
    return st.plotly_chart(fig, config=config_modebar, dpi=500, use_container_width=True)

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
        tab1, tab2 = st.tabs(["Count normalized by day of the week:", "-"])
        with tab1:
            days_emotion_chart(df_days_counts, perc_feature='perc_weekday')
    with col2:
        tab1, tab2 = st.tabs(["Count normalized by emotion:", "-"])
        with tab1:
            days_emotion_chart(df_days_counts, perc_feature='perc_emotion')

st.markdown("##### Ranking by month")
col1, _ = st.columns([3, 1])
with col1:
    st.markdown("""
        In these visualizations, the focus shifts to the monthly trend of each emotion.
        By default, data are ranked by month. The button below allows to switch the visualizations to sort 
        by percentage values.
        """)
    sorting_criteria = 'month'
    on = st.toggle("Sort each series by prevailing emotion (🧘this can take a while)")
    if on:
        sorting_criteria = 'emotion'
    fig, ax = plt.subplots(3, 2, figsize=(15, 16))
    ax = ax.flatten()
    emotions = [
        'Happy',
        'Loved',
        'Confident',
        'Playful',
        'Scared',
        'Sad'
    ]
    sorted_month = list(df_emotion.columns)
    sorted_month.reverse()
    for i, emotion in enumerate(emotions):
        df_filt = df_melt[df_melt.emotion == emotion]
        if sorting_criteria == 'month':
            df_plot = (df_filt.month.value_counts() / df_filt.shape[0]).reindex(sorted_month).fillna(0).reset_index()
        if sorting_criteria == 'emotion':
            df_plot = (df_filt.month.value_counts() / df_filt.shape[0]).reindex(sorted_month).fillna(
                0).reset_index().sort_values(by='count')
        range_plot = range(1, 1 + df_plot.shape[0])
        ax[i].hlines(y=range_plot, xmin=0, xmax=df_plot['count'], color=dict_emotion_color[emotion])
        ax[i].plot(df_plot['count'], range_plot, "o", color=dict_emotion_color[emotion])
        ax[i].set_yticks(range(1, 1 + df_plot.shape[0]), df_plot['month'])
        ax[i].set_xlabel(f'Percentage of "{emotion.lower()}" days')
        ax[i].spines['top'].set_visible(False)
        ax[i].spines['right'].set_visible(False)
        ax[i].grid(axis='x', ls=':')
        vals = ax[i].get_xticks()[1:-1]
        ax[i].set_xticks(vals, ['{:,.0%}'.format(x) for x in vals])
    st.pyplot(fig, dpi=500, use_container_width=True)

