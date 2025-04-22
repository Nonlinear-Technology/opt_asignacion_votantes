import streamlit as st

st.set_page_config(page_title="Asignación votantes", page_icon=":material/home:", layout="wide", initial_sidebar_state="expanded")

st.logo('Logo-normal.svg', icon_image='Logo-iso chico.svg')

st.subheader(f"**Conoce más sobre nosotros en nuestra página web**")
st.page_link("https://nonlinear.com.ar/", label=f":orange[**Nonlinear**]", icon=":material/web_traffic:")