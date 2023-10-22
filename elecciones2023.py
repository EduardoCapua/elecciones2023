

import streamlit as st

import folium
from folium import plugins
import pandas as pd
from streamlit_folium import st_folium
import datetime  # para poder realizar el query
import pathlib
import geopandas as gpd
from plotly.offline import iplot



# ventana y titulos
st.set_page_config(page_title="ELECCIONES GENERALES 2023",
                   initial_sidebar_state="expanded", layout="centered")
st.subheader(body="ELECCIONES GENERALES 2023", divider=True, anchor="50")


@st.cache_data
def load_data(url):
    # lectura del archivo y carga de datos
    geo_json_sgo = pathlib.Path() / "Santiago del Estero.geojson"
    assert geo_json_sgo.exists()
    geo_json_sgo = gpd.read_file(geo_json_sgo)
    return geo_json_sgo


geo_json_sgo = load_data("Santiago del Estero.geojson")


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




# bins = list(data_DptoPolitico["MOSTRAR"].quantile([0, 0.25, 0.5, 0.75, 1]))

df["MOSTRAR"] = pd.to_numeric(
    df["MOSTRAR"], errors="coerce")

bins = list(df["MOSTRAR"].quantile([0, 0.25, 0.50, 0.75, 1]))


#st.dataframe(data_DptoPolitico)

with st.container():
    st.title("MAPA INTERACTIVO")

with st.container():
    mapa_prueba = folium.Map(tiles=None)

    folium.TileLayer(name="OpenStreetMap",
                     tiles="OpenStreetMap").add_to(mapa_prueba)

    #folium.GeoJson(data=geo_json_sgo, name="Prov. de Sgo. del Estero",
    #               show=False).add_to(mapa_prueba)

    folium.Choropleth(geo_data=geo_json_Dpto, data=df, columns=["id", "MOSTRAR"], key_on="feature.properties.id_Dpto", name="Departamento Politico",
                      fill_color="BuPu", fill_opacity=0.7, line_opacity=0.5, legend_name="porcentaje de electores (%)", reset=True, show=True).add_to(mapa_prueba)

    folium.LayerControl().add_to(parent=mapa_prueba, name="Filtro")

    plugins.Fullscreen(position="topright", title="Ampliar",
                       title_cancel="Salir", force_separate_button=True).add_to(mapa_prueba)

    st_data3 = st_folium(mapa_prueba, use_container_width=any,
                         center=[-27.8014259, -64.2855237], zoom=7, height=700, width=700)

st.dataframe(df)