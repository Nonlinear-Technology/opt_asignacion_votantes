# Librerias generales
import streamlit as st
import pickle
from streamlit_folium import folium_static

#Funciones
from Postprocessing.Postprocess import create_heatmap_with_savings, calculate_global_and_average_saving, create_circuitos_map_with_labels
from utils.components import custom_metric

st.set_page_config(page_title="Asignación votantes", page_icon=":material/home:", layout="wide", initial_sidebar_state="expanded")

st.logo('Logo-normal.svg', icon_image='Logo-iso chico.svg')

@st.dialog('Circuitos electorales de Santa Fe')
def circuitos_electorales():
    fig_circuitos = create_circuitos_map_with_labels()
    folium_static(fig_circuitos)

col1, col2 = st.columns([4,1])

# with col2:
#     st.image('Logo-normal.svg', width=300)

with col1:
    st.header('Ahorro global')
    st.caption('Se muestra el ahorro de distancia total por circuito en la asignación de votantes a escuelas habilitadas de la ciudad de Santa Fe')
    
    if st.button(f':material/public: :orange[**Ver circuitos**]', type='tertiary'):
        circuitos_electorales()
    
colAhorros, colMapa = st.columns([1,4])
ahorro_global, ahorro_promedio = calculate_global_and_average_saving()
with colAhorros:
    custom_metric(label = f'Ahorro global', valor_total = f'{ahorro_global:.2f} km')
    st.write('')
    custom_metric(label = f'Ahorro promedio por circuito', valor_total = f'{ahorro_promedio:.2f} km')
    
with colMapa:
    fig = create_heatmap_with_savings()
    folium_static(fig)