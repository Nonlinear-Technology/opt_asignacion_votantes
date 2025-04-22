# Librerias generales
import streamlit as st
import pickle
from streamlit_folium import folium_static

#Funciones
from Postprocessing.Postprocess import postprocessing

st.set_page_config(page_title="Asignación votantes", page_icon=":material/home:", layout="wide", initial_sidebar_state="expanded")

st.logo('Logo-normal.svg', icon_image='Logo-iso chico.svg')

col1, col2 = st.columns([4,1])

# with col2:
#     st.image('Logo-normal.svg', width=300)

with col1:
    st.header('Propuesta de Asignación de Votantes')
    st.caption('El objetivo del proyecto es optimizar la asignación de votantes a escuelas habilitadas de la ciudad de Santa Fe minimizando las distancias')

circuitos = ['152', '171']
colSegmentacion, _ = st.columns([1,1])
with colSegmentacion:
    circuitos_seleccionados = st.multiselect(label = 'Seleccionar circuitos', options = circuitos, default = circuitos)

try:
    if len(circuitos_seleccionados) == len(circuitos):
        postprocessing()
    else:
        postprocessing(circuitos = list(circuitos_seleccionados), mapa_completo=False)
except Exception as e:
    st.error(f'Error: {e}')
    
colActual, colPropuesta = st.columns(2)

with colActual:
    st.subheader(f':grey[**Asignación actual**]')
    with open('Postprocessing/mapa_actual.pkl', 'rb') as f:
        map_actual = pickle.load(f)
        folium_static(map_actual)

with colPropuesta:
    st.subheader(f':green[**Asignación propuesta**]')
    with open('Postprocessing/mapa_nuevo.pkl', 'rb') as f:
        map_nueva = pickle.load(f)
        folium_static(map_nueva)


