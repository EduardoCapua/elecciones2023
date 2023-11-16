# Estas son declaraciones de importación en Python que importan varias bibliotecas y módulos. Aquí hay
# un desglose de lo que hace cada declaración de importación:

import streamlit as st
import folium
from folium import plugins
import pandas as pd
from streamlit_folium import st_folium
from streamlit_folium import folium_static
import datetime  # para poder realizar el query
import pathlib
import geopandas as gpd
from streamlit_option_menu import option_menu

from streamlit_gsheets import GSheetsConnection


# ventana y titulos
st.set_page_config(page_title = "PORCENTAJE ESTABLECIMIENTOS ESCOLARES",
                   initial_sidebar_state = "expanded", layout = "wide")
st.markdown(" ## PORCENTAJE ESTABLECIMIENTOS ESCOLARES ")





# conexión con google sheets

# El código `conn = st.connection("gsheets", type=GSheetsConnection)` establece una conexión a un
# documento de Google Sheets utilizando el complemento `gsheets` en Streamlit. El parámetro
# `type=GSheetsConnection` especifica el tipo de conexión que se realizará.

conn = st.connection("gsheets", type=GSheetsConnection)
estado_establecimiento = conn.read(worksheet="escuelas (estado)",usecols=list(range(5)), nrows = 18, ttl=1)



@st.cache_data
def load_data(url):
    # lectura del archivo y carga de datos
    geo_json_centroide = pathlib.Path() / "centroides_dpto.geojson"
    assert geo_json_centroide .exists()
    geo_json_centroide  = gpd.read_file(geo_json_centroide)
    return geo_json_centroide 


geo_json_centroide  = load_data("Santiago del Estero.geojson")


@st.cache_data
def load_data(url):
    # lectura del archivo y carga de datos
    geo_json_circuito = pathlib.Path() / "Circuitos.geojson"
    assert geo_json_circuito.exists()
    geo_json_circuito = gpd.read_file(geo_json_circuito)
    return geo_json_circuito


geo_json_circuito = load_data("Circuitos.geojson")


@st.cache_data
def load_data(url):
    # lectura del archivo y carga de datos
    geo_json_Dpto = pathlib.Path() / "Departamentos Politicos.geojson"
    assert geo_json_Dpto.exists()
    geo_json_Dpto = gpd.read_file(geo_json_Dpto)
    return geo_json_Dpto





geo_json_Dpto = load_data("Departamentos Politicos.geojson")



#@st.cache_data 
#def load_data(url):
#lectura del archivo y carga de datos
df = pd.read_excel("dpto politico.xlsx")
df = df.sort_values(by=["id"],ascending=[True])
  # return df

#df = load_data("dpto politico.xlsx")

st.button("Rerun")




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
        st.dataframe(data = estado_establecimiento, width = 500)
    with col2:
        st.bar_chart(estado_establecimiento)

if selected == "MESAS HABILITADAS":
    st.title(f"{selected}")

    
if selected == "% DE VOTANTES":
    st.title(f"{selected}")
        
    df["PORCENTAJE"] = pd.to_numeric(
    df["PORCENTAJE"], errors="coerce")

    bins = list(df["PORCENTAJE"].quantile([0, 0.25, 0.50, 0.75, 1]))


    with st.container():
        
        st.title("MAPA INTERACTIVO")
        
        mapa_prueba = folium.Map(tiles=None, zoom_control= False)

        
        choropleth=folium.Choropleth(
                        geo_data=geo_json_Dpto,
                        data=df,
                        columns=["id", "PORCENTAJE"],
                        key_on="feature.properties.id", name="Departamento Politico",
                        fill_color="BuPu",
                        fill_opacity=0.7,
                        nan_fill_color= "black",
                        line_opacity=0.5, legend_name="porcentaje de electores (%)",
                        reset=True,
                        show=True,
                        
                        )
        choropleth.add_to(mapa_prueba)
        
        tooltip = folium.GeoJsonTooltip(
        fields=["id", "name"],
        aliases=["id:", "nombre:"],
        localize=False,
        sticky=True,
        labels=True,
        style="""
            background-color: #00000000;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """,
        max_width=800,
        )
        
        centroides = folium.GeoJson(data=geo_json_Dpto,
                                    name="centroides",
                                    zoom_on_click=True,
                                    tooltip=tooltip,
                                    )
        centroides.add_to(mapa_prueba)
            
        
        filtro=folium.LayerControl(position="topleft")
        filtro.add_to(
                    parent=mapa_prueba,
                    name="Filtro",
                    
                    )

        agrandar_mapa=plugins.Fullscreen(
                        position="topleft",
                        title="Ampliar",
                        title_cancel="Salir",
                        force_separate_button=True,
                        )
        agrandar_mapa.add_to(mapa_prueba)

        
        herramienta_busqueda=plugins.Search(layer=centroides, search_label="name", geom_type="Polygon",collapsed=True)
        herramienta_busqueda.add_to(mapa_prueba)
        
        
        
        #mostrar el mapa
        st_folium(
                mapa_prueba,
                use_container_width=any,
                center=[-27.807300, -63.232700],
                zoom=7,
                )    
## MENU HORIZONTAL





