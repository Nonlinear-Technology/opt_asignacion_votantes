import streamlit as st

pg = st.navigation([
    st.Page("./pages/1_Interfaz_Asignacion.py", title="Comparativa de propuestas", icon=":material/compare:"),
    st.Page("./pages/2_Mapa_Global.py", title="Ahorro global", icon=":material/map:"),
    st.Page("./pages/3_Nosotros.py", title="Nosotros", icon=":material/help:"),
])

pg.run()