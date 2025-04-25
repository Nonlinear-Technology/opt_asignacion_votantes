import streamlit as st

def custom_metric(label, valor_total=None, valor_porcentual=None,
                  background_color="#f0f2f6", text_color="#000000", shadow=True):
    box_shadow = "0px 2px 4px rvalor_totalgba(0, 0, 0, 0.15)" if shadow else "none"

    # Formateo de valores
    if valor_total:
        texto_total = f"{valor_total}"
        texto_final = texto_total
    elif valor_porcentual:
        texto_porcentual = f"{valor_porcentual * 100:.1f}%"
        texto_final = texto_porcentual

    html = f"""
    <div style="
        background-color: {background_color};
        color: {text_color};
        padding: 1rem;
        border-radius: 0rem;
        box-shadow: {box_shadow};
        text-align: center;
        width: 100%;
        ">
        <div style="font-size: 0.9rem; font-weight: 300; margin-bottom: 0.5rem;">{label}</div>
        <div style="font-size: 1.8rem; font-weight: 600;">{texto_final}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)