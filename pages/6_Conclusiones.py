import streamlit as st

st.set_page_config(page_title="Conclusiones", page_icon=":material/check:", layout="wide", initial_sidebar_state="expanded")

st.logo('Logo-normal.svg', icon_image='Logo-iso chico.svg')

# Estilos visuales
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-size: 18px;
        font-family: 'Segoe UI', sans-serif;
        line-height: 1.6;
    }
    h1 {
        color: #a13e5d;
    }
    h2 {
        color: #c75d71;
        margin-top: 2em;
    }
    .highlight {
        background-color: #fff5f8;
        padding: 0.8em;
        border-left: 6px solid #a13e5d;
        border-radius: 8px;
        margin-bottom: 1.5em;
    }
    ul, ol {
        margin-left: 1.5em;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal con emoji de conclusión
st.markdown("<h1>✅ Conclusiones</h1>", unsafe_allow_html=True)

# Resumen global
st.markdown("""
<div class="highlight">
En términos globales, si todos vamos a votar, se recorren actualmente <strong>235 mil kilómetros</strong>, 
mientras que en la asignación óptima esto se reduce en <strong>101 mil kilómetros</strong>, es decir un <strong>44% menos en general</strong>. 
Si lo cuantificamos en tiempo, esto representa más de <strong>15 mil horas de movimiento</strong> 
(asumiendo que la mitad vamos caminando y la mitad en auto).
</div>
""", unsafe_allow_html=True)

# Mejoras en la asignación
st.markdown("<h2>Mejoras en la Asignación</h2>", unsafe_allow_html=True)
st.markdown("""
Además, se mejora mucho la asignación para personas que antes tenían que trasladarse mucho. Algunos ejemplos:
""")

st.markdown("""
<ol>
<li><strong>Zona del Parque Garay y Avenida Freyre:</strong> Muchas personas en esta zona caminaban hasta <strong>1.5km</strong>, mientras que en la solución óptima 
muy pocos caminan más de <strong>5 cuadras</strong> y el promedio es <strong>3 cuadras</strong>.</li>
<li><strong>Barrio Las Flores y Nueva Pompeya:</strong> En estas zonas, algunas personas caminaban hasta <strong>4 y 5km</strong> para ir a votar, mientras que en la solución óptima 
el promedio pasa de <strong>1km</strong> a <strong>5 cuadras</strong>.</li>
<li><strong>Zona de Siete Jefes y Candioti Sur y Norte:</strong> En esta zona, el promedio baja de <strong>6.5 cuadras</strong> a menos de <strong>3 cuadras por persona</strong>, 
mientras que muchas personas antes caminaban <strong>1.5km</strong>, ahora casi todas tienen que recorrer menos de <strong>5 cuadras</strong>.</li>
</ol>
""", unsafe_allow_html=True)