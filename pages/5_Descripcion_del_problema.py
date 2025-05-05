import streamlit as st

st.set_page_config(page_title="Asignación votantes", page_icon=":material/home:", layout="wide", initial_sidebar_state="expanded")

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

# Contenido con formato
st.markdown("""
<div class="highlight">
En Argentina, la asignación de votantes a escuelas varía según el tipo de elección y el municipio. En los más grandes, como <strong>Santa Fe</strong>, se agrupa a los votantes por zonas electorales (<em>circuitos</em>) y luego se los distribuye entre las escuelas de cada zona.
</div>

Un método comúnmente utilizado consiste en <strong>ordenar alfabéticamente el padrón</strong> y asignar grupos de votantes a escuelas hasta completar su capacidad. Este procedimiento puede derivar en que algunas personas deban votar en <strong>escuelas alejadas</strong>, a pesar de tener otras más cercanas disponibles.

<h2>Enfoque propuesto</h2>

A partir de <strong>datos oficiales</strong>, desde <strong>Nonlinear</strong> proponemos un enfoque basado en <strong>rigurosidad matemática</strong> y <strong>herramientas informáticas</strong> para obtener una asignación óptima de votantes al colegio más cercano, respetando las zonas electorales y las capacidades de las mesas.

Además, desarrollamos un modelo aún más eficiente que permite <strong>adaptar la cantidad de mesas</strong> según la cercanía de las escuelas a la mayor concentración de votantes.

<h2>Contenido del sitio</h2>

En las siguientes páginas encontrarán:

<ol>
<li><strong>Comparativa de propuestas:</strong> Comparativa a nivel circuito (estos se pueden visualizar en <em>Ver circuitos</em>).</li>
<li><strong>Ahorro global:</strong> Comparativa a nivel del sector electoral (Santa Fe Ciudad).</li>
<li><strong>Nosotros:</strong> Información sobre la empresa.</li>
<li><strong>Metodología:</strong> La ciencia detrás de la propuesta, junto con las hipótesis realizadas y otras observaciones.</li>
</ol>
""", unsafe_allow_html=True)
