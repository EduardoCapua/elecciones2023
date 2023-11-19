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


st.set_page_config(page_title="GUIA TELEFONICA",
                   layout="wide")


st.markdown(" # GUIA TELEFONICA ")


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
    geo_json_establecimientos = pathlib.Path() / "ESTABLECIMINETOS ESCOLARES.geojson"
    assert geo_json_establecimientos.exists()
    geo_json_establecimientos = gpd.read_file(geo_json_establecimientos)
    return geo_json_establecimientos
geo_json_establecimientos = load_data("ESTABLECIMINETOS ESCOLARES.geojson")

@st.cache_data
def load_data(url):
    # lectura del archivo y carga de datos
    geo_json_Dpto = pathlib.Path() / "Departamentos Politicos.geojson"
    assert geo_json_Dpto.exists()
    geo_json_Dpto = gpd.read_file(geo_json_Dpto)
    return geo_json_Dpto

geo_json_Dpto = load_data("Departamentos Politicos.geojson")



@st.cache_data 
def load_data(url):
    df = pd.read_excel("dpto politico.xlsx")
    df = df.sort_values(by=["id"],ascending=[True])
    return df

df = load_data("dpto politico.xlsx")

@st.cache_data 
def load_data(url):
    listado_establecimientos = pd.read_excel("LISTADO DE ESCUELAS.xlsx")
    return listado_establecimientos
listado_establecimientos = load_data("LISTADO DE ESCUELAS.xlsx")


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
            options=["LISTADO DE TELEFONOS", "MAPA"],  # required
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
        )
        return selected



selected = streamlit_menu(example=EXAMPLE_NO)

if selected == "LISTADO DE TELEFONOS":
    st.title(f"{selected}")
    
    col1, col2 = st.columns(2)

    with col1:
       st.write("agregar algo")
    with col2:
       st.write("agregar algo") 

    
if selected == "MAPA":
    st.title(f"{selected}")

    with st.container():
        
        mapa_guia = folium.Map(tiles=None, zoom_control= False)
        folium.TileLayer(name="OpenStreetMap",tiles="OpenStreetMap").add_to(mapa_guia)
        
        
    
        
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
        
        Departamentos_politicos = folium.GeoJson(data=geo_json_Dpto,
                                    name="Departamentos politicos",
                                    zoom_on_click=True,
                                    tooltip=tooltip,
                                    style_function=lambda feature: {
                                    "fillColor": "#ffff00",
                                    "color": "black",
                                    "weight": 2,
                                    "dashArray": "5, 5",
                                    },
                                    highlight_function=lambda feature: {
                                    "fillColor": (
                                    "green" if "e" in feature["properties"]["fna"].lower() else "#ffff00"
                                    ),
                                    },
                                    )
        
        
        Departamentos_politicos.add_to(mapa_guia)
        
        Circuitos_politicos = folium.GeoJson(data=geo_json_circuito,
                                    name="Circuitos",
                                    zoom_on_click=True,
                                    show=False,
                                    style_function=lambda feature: {
                                    "fillColor": "#ff3300",
                                    "color": "black",
                                    "weight": 2,
                                    "dashArray": "3, 3",
                                    },
                                    highlight_function=lambda feature: {
                                    "fillColor": (
                                    "green" if "e" in feature["properties"]["circuito"].lower() else "#00ffff"
                                    ),
                                    },
                                    )
        Circuitos_politicos.add_to(mapa_guia)
        
        def style_function(feature):
            props = feature.get('properties')
            markup = f"""
                <div style="font-size: 0.8em;">
                <div style="width: 10px;
                height: 10px;
                border: 1px solid black;
                border-radius: 5px;
                background-color: orange;">
                </div>
            """
            return {"html": markup}


        establecimiento_escolar = folium.GeoJson(
        data=geo_json_establecimientos,
        name="establecimientos escolares",
        marker=folium.Marker(icon=folium.DivIcon()),
        tooltip=folium.GeoJsonTooltip(fields=["name", "FUNCIONARIO"]),
        popup=folium.GeoJsonPopup(fields=["name", "FUNCIONARIO"]),
        style_function=style_function,
        zoom_on_click=True,
        show=True
        )
        establecimiento_escolar.add_to(mapa_guia)
        
        filtro=folium.LayerControl(position="topleft")
        filtro.add_to(
                    parent=mapa_guia,
                    name="Filtro",
                    
        )

        agrandar_mapa=plugins.Fullscreen(
                        position="topleft",
                        title="Ampliar",
                        title_cancel="Salir",
                        force_separate_button=True,
                        )
        agrandar_mapa.add_to(mapa_guia)

        
        herramienta_busqueda=plugins.Search(layer=establecimiento_escolar, search_label="name", geom_type="Point",collapsed=True, search_zoom=13)
        herramienta_busqueda.add_to(mapa_guia)
        
        
        
        #mostrar el mapa
        st_folium(
                mapa_guia,
                use_container_width=any,
                center=[-27.807300, -63.232700],
                zoom=7,
                )    
## MENU HORIZONTAL





