

import streamlit as st
from streamlit_option_menu import option_menu


st.set_page_config(page_title="ELECCIONES 2023",
                   layout="wide")
st.sidebar.success("selcciona la pagina", icon="✅")

st.markdown(" # ELECCIONES 2023 ")


# 1=sidebar menu, 2=horizontal menu, 3=horizontal menu w/ custom menu
EXAMPLE_NO = 2



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
            default_index=0,  # optional
            orientation="horizontal",
        )
        return selected

 

selected = streamlit_menu(example=EXAMPLE_NO)

if selected == "ESCUELAS HABILITADAS":
    st.title(f"{selected}")
if selected == "MESAS HABILITADAS":
    st.title(f"{selected}")


if selected == "% DE VOTANTES":
    st.title(f"{selected}")