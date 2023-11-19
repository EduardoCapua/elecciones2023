# Estas son declaraciones de importación en Python que importan varias bibliotecas y módulos. Aquí hay
# un desglose de lo que hace cada declaración de importación:

import streamlit as st
import folium
from folium import plugins
import pandas as pd
from streamlit_folium import st_folium
import pathlib
import geopandas as gpd
from streamlit_option_menu import option_menu
from streamlit_gsheets import GSheetsConnection
from st_aggrid import AgGrid

# ventana y titulos
st.set_page_config(page_title = "PORCENTAJE ESTABLECIMIENTOS ESCOLARES",
                   initial_sidebar_state = "expanded", layout = "wide")
st.markdown(" ## ESTADO DE ESTABLECIMIENTOS ESCOLARES ")





# conexión con google sheets

# El código `conn = st.connection("gsheets", type=GSheetsConnection)` establece una conexión a un
# documento de Google Sheets utilizando el complemento `gsheets` en Streamlit. El parámetro
# `type=GSheetsConnection` especifica el tipo de conexión que se realizará.

conn = st.connection("gsheets", type=GSheetsConnection)

estado_establecimiento = conn.read(worksheet="escuelas (estado)",usecols=list(range(5)), nrows = 19, ttl=1)
mesa_establecimiento = conn.read(worksheet="escuelas (mesas)",usecols=list(range(5)), nrows = 19, ttl=1)






#MENU HORIZONTAL

EXAMPLE_NO = 2
# 1=sidebar menu, 2=horizontal menu, 3=horizontal menu w/ custom menu
def streamlit_menu(example=1):
    if example == 1:
        # 1. as sidebar menu
        with st.sidebar:
            selected = option_menu(
                menu_title="Main Menu",  # required
                options=["Home", "Projects", "Contact"],  # required
                icons=["house", "book", "envelope"],  # optional
                menu_icon="cast",  # optional
                default_index=0,  # optional
            )
        return selected

    if example == 2:
        # 2. horizontal menu w/o custom style
        selected = option_menu(
            menu_title=None,  # required
            options=["ESCUELAS HABILITADAS", "MESAS HABILITADAS", "% DE VOTANTES"],  # required
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
        )
        return selected



selected = streamlit_menu(example=EXAMPLE_NO)

if selected == "ESCUELAS HABILITADAS":
    st.title(f"{selected}")
    
    col1, col2 = st.columns(2)

    with col1:

        AgGrid(estado_establecimiento)
        
    with col2:
        st.write("escribir algo")

if selected == "MESAS HABILITADAS":
    st.title(f"{selected}")

    
if selected == "% DE VOTANTES":
    st.title(f"{selected}")



## MENU HORIZONTAL





