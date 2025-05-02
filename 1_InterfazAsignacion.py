import streamlit as st

pg = st.navigation([
    st.Page("./pages/5_Descripcion_del_problema.py", title="Descripción del problema", icon=":material/compare:"),
    st.Page("./pages/1_Interfaz_Asignacion.py", title="Resultados", icon=":material/compare:"),
    st.Page("./pages/2_Mapa_Global.py", title="Ahorro global", icon=":material/map:"),
    st.Page("./pages/3_Nosotros.py", title="Nosotros", icon=":material/help:"),
    st.Page("./pages/4_Metodologia.py", title="Metodología", icon=":material/build_circle:"),
])

pg.run()