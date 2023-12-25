import streamlit as st
import pandas as pd

import sys
from utils import *
sys.path.insert(0, "..")
local_css("style.css")

from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)
data = conn.read(
    worksheet="2024_pixel",
    ttl="10m",
    usecols=range(13),
    nrows=31
)

first_col = data.columns[0]
data = data.rename(columns={first_col: 'id_day'})
data = data.set_index('id_day')
data = data.fillna('0')
st.dataframe(data)
