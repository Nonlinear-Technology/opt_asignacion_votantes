# Librerias generales
import streamlit as st
import pickle
from streamlit_folium import folium_static

#Funciones
from Postprocessing.Postprocess import postprocessing, metricas, create_circuitos_map_with_labels

# Componentes
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
    st.header('Propuesta de Asignación de Votantes')
    st.caption('El objetivo del proyecto es optimizar la asignación de votantes a escuelas habilitadas de la ciudad de Santa Fe minimizando las distancias')
    
    if st.button(f':material/public: :orange[**Ver circuitos**]', type='tertiary'):
        circuitos_electorales()

st.session_state.circuitos = ['10', '20', '30', '40', '50', '60', '70', '80', '90', '100', '110', '115', '120', '130', '140', '142', '150', '152', '160', '161', '162', '165', '170', '171', '172', '175', '180', '185']
# colSegmentacion, _ = st.columns([1,5])
colSeleccion, _, colMapaSeleccion = st.columns([1,3,2])
with colSeleccion:
    circuitos_seleccionados = st.selectbox(label = f'**Seleccionar circuitos**', options = st.session_state.circuitos)
    circuitos_seleccionados = [circuitos_seleccionados]
# with colMapaSeleccion:
#     actual_nueva = st.pills(label = f'**Seleccionar mapa**', options = ['Actual', 'Optimo mesas fijas', 'Optimo mesas libres'])

try:
    if len(circuitos_seleccionados) == len(st.session_state.circuitos):
        # postprocessing()
        distancia_total_nueva, distancia_total_actual, distancia_total_nueva_2, cantidad_votantes, distancia_maxima_nueva, distancia_maxima_actual, distancia_maxima_nueva_2  = metricas()
    else:
        # postprocessing(circuitos = list(circuitos_seleccionados), mapa_completo=False)
        distancia_total_nueva, distancia_total_actual, distancia_total_nueva_2, cantidad_votantes, distancia_maxima_nueva, distancia_maxima_actual, distancia_maxima_nueva_2  = metricas(circuitos = list(circuitos_seleccionados), mapa_completo=False)
except Exception as e:
    st.error(f'Error: {e}')
    
colActual, colNueva, colNueva2 = st.columns([2,2,2]) 
circuito = circuitos_seleccionados[0]        
        
with colActual:
#     colMetrica1Actual, colMetrica2Actual = st.columns([1,1])
#     with colMetrica1Actual:
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
        custom_metric(label = f'Distancia total recorrida', valor_total = f'{distancia_total_actual:.0f} km')
        # with colMetrica2Actual:
        st.write('')
        custom_metric(label = f'Distancia promedio por persona', valor_total = f'{distancia_total_actual/cantidad_votantes:.2f} km')
        st.write('')
        custom_metric(label = f'Distancia máxima recorrida', valor_total = f'{distancia_maxima_actual:.2f} km')
    
    with colHistorgramaActual:
        with open(f'Postprocessing/histogram_actual_{circuito}.pkl', 'rb') as f:
            histograma_actual = pickle.load(f)
            with st.spinner('Generando histograma...'):
                st.plotly_chart(histograma_actual)
with colNueva:
    # colMetrica1Nueva, colMetrica2Nueva = st.columns([1,1])
    # with colMetrica1Nueva:
    st.markdown(
        """
        <div style="
            font-size: 20px;
            font-weight: bold;
            background-color: #f0f0f0;
            border-radius: 10px;
            padding: 10px;
            text-align: center;">
            OPTIMO Mesas Fijas
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write('')
    
    colMetricasPropuesta, colHistorgramaPropuesta = st.columns([1,1])
    
    with colMetricasPropuesta:
        custom_metric(label = f'Distancia total recorrida', valor_total = f'{distancia_total_nueva:.0f} km', cambio_porcentual = distancia_total_nueva/distancia_total_actual)
        # with colMetrica2Nueva:
        st.write('')
        custom_metric(label = f'Distancia promedio por persona', valor_total = f'{distancia_total_nueva/cantidad_votantes:.2f} km')
        st.write('')
        custom_metric(label = f'Distancia máxima recorrida', valor_total = f'{distancia_maxima_nueva:.2f} km')
    
    with colHistorgramaPropuesta:
        with open(f'Postprocessing/histogram_nueva_{circuito}.pkl', 'rb') as f:
            histograma_nueva = pickle.load(f)
            with st.spinner('Generando histograma...'):
                st.plotly_chart(histograma_nueva)

with colNueva2:
    st.markdown(
        """
        <div style="
            font-size: 20px;
            font-weight: bold;
            background-color: #f0f0f0;
            border-radius: 10px;
            padding: 10px;
            text-align: center;">
            OPTIMO Mesas Libres
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write('')
    
    colMetricasPropuesta, colHistorgramaPropuesta = st.columns([1,1])
    
    with colMetricasPropuesta:
        custom_metric(label = f'Distancia total recorrida', valor_total = f'{distancia_total_nueva_2:.0f} km', cambio_porcentual = distancia_total_nueva_2/distancia_total_actual)
        # with colMetrica2Nueva:
        st.write('')
        custom_metric(label = f'Distancia promedio por persona', valor_total = f'{distancia_total_nueva_2/cantidad_votantes:.2f} km')
        st.write('')
        custom_metric(label = f'Distancia máxima recorrida', valor_total = f'{distancia_maxima_nueva_2:.2f} km')
    
    with colHistorgramaPropuesta:
        with open(f'Postprocessing/histogram_nueva_2_{circuito}.pkl', 'rb') as f:
            histograma_nueva = pickle.load(f)
            with st.spinner('Generando histograma...'):
                st.plotly_chart(histograma_nueva)
                
colMapa1, colMapa2 = st.columns([1,1])

with colMapa1:

    actual_nueva_1 = st.pills(label = f'**Seleccionar mapa**', options = ['Actual', 'Optimo mesas fijas', 'Optimo mesas libres'], key='pills_1', default = 'Actual')
    
    if actual_nueva_1 == 'Actual':
        with open(f'Postprocessing/mapa_actual_{circuito}.pkl', 'rb') as f:
            map_actual = pickle.load(f)
            with st.spinner('Generando mapa...'):
                folium_static(map_actual)

    if actual_nueva_1 == 'Optimo mesas fijas':
        with open(f'Postprocessing/mapa_nuevo_{circuito}.pkl', 'rb') as f:
            map_nueva = pickle.load(f)
            with st.spinner('Generando mapa...'):
                folium_static(map_nueva)

    if actual_nueva_1 == 'Optimo mesas libres':
        with open(f'Postprocessing/mapa_nuevo_2_{circuito}.pkl', 'rb') as f:
            map_nueva_2 = pickle.load(f)
            with st.spinner('Generando mapa...'):
                folium_static(map_nueva_2)
                
with colMapa2:
    
    actual_nueva_2 = st.pills(label = f'**Seleccionar mapa**', options = ['Actual', 'Optimo mesas fijas', 'Optimo mesas libres'], key='pills_2', default = 'Optimo mesas fijas')
    
    if actual_nueva_2 == 'Actual':
        with open(f'Postprocessing/mapa_actual_{circuito}.pkl', 'rb') as f:
            map_actual = pickle.load(f)
            with st.spinner('Generando mapa...'):
                folium_static(map_actual)

    if actual_nueva_2 == 'Optimo mesas fijas':
        with open(f'Postprocessing/mapa_nuevo_{circuito}.pkl', 'rb') as f:
            map_nueva = pickle.load(f)
            with st.spinner('Generando mapa...'):
                folium_static(map_nueva)

    if actual_nueva_2 == 'Optimo mesas libres':
        with open(f'Postprocessing/mapa_nuevo_2_{circuito}.pkl', 'rb') as f:
            map_nueva_2 = pickle.load(f)
            with st.spinner('Generando mapa...'):
                folium_static(map_nueva_2)
        

# with colData:
#     circuito = circuitos_seleccionados[0]
#     actual_nueva = st.pills(label = f'**Seleccionar asignación**', options = ['Actual', 'Propuesta'])
    
#     if actual_nueva == 'Actual':
#         custom_metric(label = f'Distancia total recorrida', valor_total = f'{distancia_total_actual:.2f} km')
#         st.write('')
#         custom_metric(label = f'Distancia promedio por persona', valor_total = f'{distancia_total_actual/cantidad_votantes:.2f} km')
            
#         with colMapa:
#            with open(f'Postprocessing/mapa_actual_{circuito}.pkl', 'rb') as f:
#                 map_actual = pickle.load(f)
#                 with st.spinner('Generando mapa...'):
#                     folium_static(map_actual)
                
#     if actual_nueva == 'Propuesta':
#         custom_metric(label = f'Distancia total recorrida', valor_total = f'{distancia_total_nueva:.2f} km')
#         st.write('')
#         custom_metric(label = f'Distancia promedio por persona', valor_total = f'{distancia_total_nueva/cantidad_votantes:.2f} km')
        
#         with colMapa:
#             with open(f'Postprocessing/mapa_nuevo_{circuito}.pkl', 'rb') as f:
#                 map_nueva = pickle.load(f)
#                 with st.spinner('Generando mapa...'):
#                     folium_static(map_nueva)
    



# colAhorro, colAhorroPromedio, _ = st.columns([1,1,2])
# with colAhorro:
#     st.metric(label = f':green[**AHORRO DE DISTANCIA TOTAL**]', value = f'{(distancia_total_actual - distancia_total_nueva):.2f} km')
# with colAhorroPromedio:
#     st.metric(label = f':green[**AHORRO DE DISTANCIA PROMEDIO**]', value = f'{(distancia_total_actual/cantidad_votantes - distancia_total_nueva/cantidad_votantes):.2f} km')

# colActual, colPropuesta = st.columns(2)

# with colActual:
#     st.subheader(f':grey[**Asignación actual**]')
    
#     colDistTotalActual, colDistPromedioActual = st.columns(2)
#     with colDistTotalActual:
#         st.metric(label = f':orange[**Distancia total recorrida**]', value = f'{distancia_total_actual:.2f} km')
#     with colDistPromedioActual:
#         st.metric(label = f':orange[**Distancia promedio por persona**]', value = f'{distancia_total_actual/cantidad_votantes:.2f} km')    
    
#     with open('Postprocessing/mapa_actual.pkl', 'rb') as f:
#         map_actual = pickle.load(f)
#         folium_static(map_actual)

# with colPropuesta:
#     st.subheader(f':grey[**Asignación propuesta**]')
    
#     colDistTotalNueva, colDistPromedioNueva = st.columns(2)
#     with colDistTotalNueva:
#         st.metric(label = f':orange[**Distancia total recorrida**]', value = f'{distancia_total_nueva:.2f} km')
#     with colDistPromedioNueva:
#         st.metric(label = f':orange[**Distancia promedio por persona**]', value = f'{distancia_total_nueva/cantidad_votantes:.2f} km')
        
#     with open('Postprocessing/mapa_nuevo.pkl', 'rb') as f:
#         map_nueva = pickle.load(f)
#         folium_static(map_nueva)



# circuitos = ['10', '20', '30', '40', '50', '60', '70', '80', '90', '100', '110', '120', '130', '140', '142', '150', '152', '160', '161', '162', '165', '171', '172']

# for circuito in circuitos:
#     circuito = [circuito]
#     postprocessing(circuitos = list(circuitos_seleccionados), mapa_completo=False)
#     st.write('listo')