# example/st_app.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection

url = "https://docs.google.com/spreadsheets/d/1_ZuAYVX1KMWZz5DnhmwhdaUC49o7bM7mpTmQkgFNBKg/edit?usp=sharing"

conn = st.experimental_connection("gsheets", type=GSheetsConnection)
data = conn.read(spreadsheet=url, usecols=list(range(7)), worksheet="120401593", ttl=0.5)

st.dataframe(data)

