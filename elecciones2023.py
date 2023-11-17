

import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_gsheets import GSheetsConnection


st.set_page_config(page_title="ELECCIONES 2023",
                   layout="wide")

st.markdown(" # DATOS GENERALES - ELECCIONES 2023 ")


#CARGA DE DATOS

conn = st.connection("gsheets", type=GSheetsConnection)

estado_establecimiento = conn.read(worksheet="escuelas (estado)",usecols=list(range(5)), nrows = 19, ttl=1)
mesa_establecimiento = conn.read(worksheet="escuelas (mesas)",usecols=list(range(4)), nrows = 19, ttl=1)
porcentaje_establecimiento = conn.read(worksheet="escuelas (%)",usecols=list(range(6)), nrows = 19, ttl=1)

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
            options=["1° ETAPA", "2° ETAPA"],  # required
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
        )
        return selected



selected = streamlit_menu(example=EXAMPLE_NO)

if selected == "1° ETAPA":
    
    #datos de la hoja de escuelas (estado)
    escuela_total = estado_establecimiento.loc[18,"TOTAL ESCUELAS"]
    escuela_habilitada = estado_establecimiento.loc[18,"ESCUELAS HABILITADAS"]
    escuela_no_habilitada = estado_establecimiento.loc[18,"ESCUELAS NO HABILITADAS"]
    escuela_sin_informar = estado_establecimiento.loc[18,"ESCUELAS SIN INFORMAR"]

    #datos de la hoja de escuelas (mesas)
    mesas_total = mesa_establecimiento.loc[18,"TOTAL DE MESAS"]
    mesas_habilitada = mesa_establecimiento.loc[18,"MESAS HABILITADAS"]
    mesas_no_habilitada = mesa_establecimiento.loc[18,"MESAS NO HABILITADAS"]

    #datos de la hoja de escuelas (porcentajes)
    porcentaje_10 = porcentaje_establecimiento.loc[18,"10:00 HS"]
    porcentaje_12 = porcentaje_establecimiento.loc[18,"12:00 HS"]
    porcentaje_14 = porcentaje_establecimiento.loc[18,"14:00 HS"]
    porcentaje_16 = porcentaje_establecimiento.loc[18,"16:00 HS"]
    porcentaje_18 = porcentaje_establecimiento.loc[18,"18:00 HS"]

    st.divider()

    with st.container():
        st.subheader("ESTABLECIMIENTOS ESCOLARES")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(label="TOTAL ESCUELAS", value=escuela_total)

        with col2:
            st.metric(label="ESCUELAS HABILITADAS", value=escuela_habilitada)

        with col3:
            st.metric(label="ESCUELAS NO HABILITADAS", value=escuela_no_habilitada)

        with col4:
            st.metric(label="ESCUELAS SIN INFORMAR", value=escuela_sin_informar)    

    st.divider()

    with st.container():
        st.subheader("ESTADO DE MESAS")
        
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(label="TOTAL DE MESAS", value=mesas_total)

        with col2:
            st.metric(label="MESAS HABILITADAS", value=mesas_habilitada)

        with col3:
            st.metric(label="MESAS NO HABILITADAS", value=mesas_no_habilitada)


    st.divider()

    with st.container():
        st.subheader("PORCENTAJE DE ESCUELAS")
        
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric(label="10:00 HS", value=porcentaje_10)

        with col2:
            st.metric(label="12:00 HS", value=porcentaje_12)

        with col3:
            st.metric(label="14:00 HS", value=porcentaje_14)

        with col4:
            st.metric(label="16:00 HS", value=porcentaje_16)

        with col5:
            st.metric(label="18:00 HS", value=porcentaje_18)

    st.divider()

if selected == "2° ETAPA":
    st.title(f"{selected}")




## MENU HORIZONTAL






