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
        
        

global_actual, global_nuevo, ahorro_global, ahorro_promedio, ahorro_promedio_actual, ahorro_promedio_nuevo, ahorro_tiempo_global, ahorro_tiempo_promedio, tiempo_promedio_actual, tiempo_promedio_nuevo = calculate_global_and_average_saving()

colAhorroGlobal, colTiempoGlobal, colAhorroPromedio, colTiempoPromedio, _ = st.columns([1,1,1,1,2])
with colAhorroGlobal:
    custom_metric(label = f'Ahorro global', valor_total = f'{ahorro_global:.2f} km')
with colTiempoGlobal:
    custom_metric(label = f'Ahorro tiempo global', valor_total = f'{ahorro_tiempo_global:.2f} hs')
with colAhorroPromedio:
    custom_metric(label = f'Ahorro promedio por persona', valor_total = f'{ahorro_promedio:.2f} km')
with colTiempoPromedio:
    custom_metric(label = f'Ahorro tiempo promedio por persona', valor_total = f'{(ahorro_tiempo_promedio*60):.2f} min')

colActual, colNueva, colMapa = st.columns([2,2,2])
with colActual:
    st.write('')
    st.markdown(
        """
        <div style="
            font-size: 20px;
            font-weight: bold;
            background-color: #f0f0f0;
            border-radius: 10px;
            padding: 10px;
            text-align: center;">
            ACTUAL
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write('')
    
    colMetricasActual, colHistorgramaActual = st.columns([1,1])
    with colMetricasActual:
        custom_metric(label = f'Distancia total', valor_total = f'{global_actual:.2f} km')
        st.write('')
        custom_metric(label = f'Ahorro promedio por persona', valor_total = f'{ahorro_promedio_actual:.2f} km')
        st.write('')
        custom_metric(label = f'Tiempo promedio por persona', valor_total = f'{(tiempo_promedio_actual*60):.2f} min')
    with colHistorgramaActual:
        with open(f'Postprocessing/histogram_actual_all.pkl', 'rb') as f:
            histogram_actual = pickle.load(f)
        st.plotly_chart(histogram_actual, use_container_width=True)
with colNueva:
    st.write('')
    st.markdown(
        """
        <div style="
            font-size: 20px;
            font-weight: bold;
            background-color: #f0f0f0;
            border-radius: 10px;
            padding: 10px;
            text-align: center;">
            OPTIMO
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write('')
    
    colMetricasPropuesta, colHistorgramaPropuesta = st.columns([1,1])
    with colMetricasPropuesta:
        custom_metric(label = f'Distancia total', valor_total = f'{global_nuevo:.2f} km')
        st.write('')
        custom_metric(label = f'Ahorro promedio por persona', valor_total = f'{ahorro_promedio_nuevo:.2f} km')
        st.write('')
        custom_metric(label = f'Tiempo promedio por persona', valor_total = f'{(tiempo_promedio_nuevo*60):.2f} min')
    with colHistorgramaPropuesta:
        with open(f'Postprocessing/histogram_nueva_all.pkl', 'rb') as f:
            histogram_nueva = pickle.load(f)
        st.plotly_chart(histogram_nueva, use_container_width=True)
        
with colMapa:
    fig = create_heatmap_with_savings()
    folium_static(fig)
        
    
# colMetricas, colMapa = st.columns([2,3])
# global_actual, global_nuevo, ahorro_global, ahorro_promedio, ahorro_promedio_actual, ahorro_promedio_nuevo = calculate_global_and_average_saving()
# with colMetricas:
#     colPrimera, colSegunda = st.columns([1,1])
#     with colPrimera:
#         custom_metric(label = f'Ahorro global', valor_total = f'{ahorro_global:.2f} km')
#         # custom_metric(label = f'Distancia total actual', valor_total = f'{global_actual:.2f} km')
#         # st.write('')
#         # custom_metric(label = f'Distancia total propuesta', valor_total = f'{global_nuevo:.2f} km')
#     with colSegunda:
#         custom_metric(label = f'Ahorro promedio por persona', valor_total = f'{ahorro_promedio:.2f} km')
    
#     st.divider()
    
#     colActual, colNueva = st.columns([1,1])
#     with colActual:
#         custom_metric(label = f'Distancia total actual', valor_total = f'{global_actual:.2f} km')
        
#         with open(f'Postprocessing/histogram_actual_all.pkl', 'rb') as f:
#             histogram_actual = pickle.load(f)
#         st.plotly_chart(histogram_actual, use_container_width=True)
#     with colNueva:
#         custom_metric(label = f'Distancia total propuesta', valor_total = f'{global_nuevo:.2f} km')
        
#         with open(f'Postprocessing/histogram_nueva_all.pkl', 'rb') as f:
#             histogram_nueva = pickle.load(f)
#         st.plotly_chart(histogram_nueva, use_container_width=True)
    
    
# with colMapa:
#     fig = create_heatmap_with_savings()
#     folium_static(fig)