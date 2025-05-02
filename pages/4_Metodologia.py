import streamlit as st
# Configurar la página
st.set_page_config(page_title="Metodología", layout="wide")

# st.logo('Logo-normal.svg', icon_image='Logo-iso chico.svg')
st.logo('Logo-normal.svg', icon_image='Logo-iso chico.svg')


# Estilos personalizados: tamaño de letra, colores, separación
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-size: 18px;
        font-family: 'Segoe UI', sans-serif;
        line-height: 1.6;
    }
    h1 {
        color: #1f5e99;
    }
    h2 {
        color: #2c7c9f;
        margin-top: 2em;
    }
    h3 {
        color: #3c9f7c;
        margin-top: 1.5em;
    }
    .highlight {
        background-color: #f0f8ff;
        padding: 0.5em;
        border-radius: 8px;
        border-left: 6px solid #1f5e99;
    }
    ul {
        margin-left: 1.5em;
    }
    </style>
""", unsafe_allow_html=True)

# Título
st.markdown("<h1>Metodología</h1>", unsafe_allow_html=True)

# Descripción inicial
st.markdown("""
<div class="highlight">
Este proyecto aborda el problema de asignar votantes a centros de votación de manera eficiente en la ciudad de <strong>Santa Fe Capital</strong>, con el objetivo de <strong>minimizar las distancias</strong> que deben recorrer para ejercer su derecho al voto. 

Para ello, se desarrolló un modelo de optimización matemática que considera tanto la ubicación de los votantes como la capacidad disponible en cada establecimiento educativo habilitado como centro de votación.
</div>
""", unsafe_allow_html=True)

# Enfoque de Optimización
st.markdown("<h2>Enfoque de Optimización</h2>", unsafe_allow_html=True)
st.markdown("""
La asignación se formula como un problema de <strong>programación lineal entera (PLE)</strong>, cuya función objetivo busca <strong>minimizar la suma total de las distancias</strong> entre los domicilios de los votantes y los centros de votación asignados, respetando la capacidad máxima de cada establecimiento.

Esta estrategia permite obtener una distribución más equitativa y eficiente, con potencial para reducir significativamente el desplazamiento promedio en contextos electorales reales.
""", unsafe_allow_html=True)

# Procesamiento de Datos
st.markdown("<h2>Procesamiento de Datos</h2>", unsafe_allow_html=True)
st.markdown("""
El proceso comienza con la recopilación del <strong>Registro Nacional de Electores</strong> en formato PDF para cada circuito de la sección electoral <em>“1 - La Capital”</em>.

Posteriormente se realiza:

- Lectura automatizada y filtrado de datos relevantes  
- Georreferenciación de domicilios y centros de votación  
- Cálculo de distancias reales para alimentar el modelo de optimización  
""", unsafe_allow_html=True)

# Desarrollo e Implementación
st.markdown("<h2>Desarrollo e Implementación</h2>", unsafe_allow_html=True)
st.markdown("""
Los algoritmos fueron desarrollados en lenguaje <strong>Python</strong> y permiten modelar, resolver y analizar diferentes escenarios de asignación.

Una vez obtenida la solución óptima, esta se contrasta con la asignación actual para detectar oportunidades de mejora en la logística electoral.
""", unsafe_allow_html=True)

# Línea divisoria
st.markdown("---")

# Hipótesis y Observaciones
st.markdown("<h1>Hipótesis y Observaciones</h1>", unsafe_allow_html=True)

# Calidad de direcciones
st.markdown("<h2>Calidad y Formato de las Direcciones</h2>", unsafe_allow_html=True)
st.markdown("""
Uno de los principales desafíos radica en que las direcciones del padrón electoral no fueron diseñadas para ser interpretadas automáticamente.

Para resolverlo, se diseñó un sistema de coincidencia por palabras clave que permite <strong>identificar de manera unívoca los nombres de calles</strong>. A pesar de su efectividad, ciertos registros con errores u omisiones no pudieron ser localizados correctamente.
""", unsafe_allow_html=True)

# Circuitos excluidos
st.markdown("<h3>Circuitos excluidos del análisis</h3>", unsafe_allow_html=True)
st.markdown("""
Fueron excluidos por falta de datos utilizables:

- Circuito 190 (**Barrio El Pozo**)  
- Circuito 192 (**Alto Verde**)  
- Circuito 194 (**Colastiné Norte**)  
- Circuito 196 (**La Guardia**)  
""")

st.markdown("""
El resto de los circuitos alcanza una <strong>cobertura promedio del 90%</strong>. Esto significa que aproximadamente el <strong>10% de los votantes</strong> no fueron incluidos en el análisis debido a la imposibilidad de georreferenciar sus domicilios con precisión.
""", unsafe_allow_html=True)

# Cálculo de distancias
st.markdown("<h2>Consideraciones sobre el Cálculo de Distancias</h2>", unsafe_allow_html=True)
st.markdown("""
Se utilizó la <strong>distancia geodésica</strong> para estimar el trayecto más corto entre dos puntos sobre la superficie terrestre. Si bien ofrece una buena aproximación general, podría introducir cierto margen de error en ciudades como Santa Fe, donde la disposición en cuadrícula de las calles impone trayectos no rectilíneos.
""", unsafe_allow_html=True)
