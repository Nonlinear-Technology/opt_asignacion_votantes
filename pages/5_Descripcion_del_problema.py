import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Descripción del problema", page_icon=":material/ballot:", layout="wide", initial_sidebar_state="expanded")

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

# Título principal con emoji de urna de votación
st.markdown("<h1>🗳️ Descripción del problema</h1>", unsafe_allow_html=True)
import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Descripción del problema", layout="wide")

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

# Título principal con emoji
st.markdown("<h1>🗳️ Descripción del problema</h1>", unsafe_allow_html=True)

# Contenido formateado
st.markdown("""
<div class="highlight">
En Argentina, la asignación de votantes a escuelas varía según el tipo de elección y el municipio. En ciudades grandes, como <strong>Santa Fe</strong>, se agrupa a los votantes por zonas electorales (<em>circuitos</em>) y luego se los distribuye entre las escuelas de cada zona.
</div>

El método comúnmente utilizado consiste en <strong>ordenar alfabéticamente el padrón</strong> e ir asignando en ese mismo orden los votantes a cada mesa de cada escuela hasta completar su capacidad. Es decir, <strong>no hay ningún criterio geográfico</strong> en la asignación. De esta manera, muchas personas deben votar en <strong>escuelas alejadas</strong>, a pesar de tener otras más cercanas disponibles.

<h2>Enfoque propuesto</h2>

A partir de <strong>datos oficiales</strong>, desde <strong>Nonlinear</strong> proponemos un enfoque basado en <strong>ciencia de datos</strong> y <strong>optimización matemática</strong> para obtener una asignación que <strong>minimice las distancias recorridas</strong>, respetando las zonas electorales y las capacidades de las mesas (<em>Modelo “Óptimo Mesas Fijas”</em>).

Además, desarrollamos un modelo aún más eficiente (<em>“Óptimo Mesas Libres”</em>) que permite <strong>modificar la cantidad de mesas</strong> de los locales buscando aún mejores soluciones para los votantes.

<h2>Contenido del sitio</h2>

En las siguientes páginas encontrarán:

<ol>
<li><strong>Resultados:</strong> Comparativa a nivel circuito (estos se pueden visualizar en <em>Ver circuitos</em>).</li>
<li><strong>Ahorro global:</strong> Comparativa a nivel del sector electoral (Santa Fe Ciudad).</li>
<li><strong>Nosotros:</strong> Información sobre la empresa.</li>
<li><strong>Metodología:</strong> La ciencia detrás de la propuesta, junto con las hipótesis realizadas y otras observaciones.</li>
</ol>
""", unsafe_allow_html=True)

