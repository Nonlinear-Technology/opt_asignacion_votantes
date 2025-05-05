import streamlit as st

def custom_metric(label, valor_total=None, valor_porcentual=None, cambio_porcentual=None,
                  background_color="#f0f2f6", text_color="#000000", shadow=True):
    """
    Custom metric component for Streamlit.

    Args:
        label (str): The label for the metric.
        valor_total (float, optional): The main numeric value to display.
        valor_porcentual (float, optional): The percentage value to display as the main value.
        cambio_porcentual (float, optional): The percentage change to display below the main value.
        background_color (str, optional): Background color of the metric box.
        text_color (str, optional): Text color of the metric box.
        shadow (bool, optional): Whether to apply a shadow effect to the box.
    """
    box_shadow = "0px 2px 4px rgba(0, 0, 0, 0.15)" if shadow else "none"

    # Format the main value
    if valor_total is not None:
        texto_total = f"{valor_total}"
        texto_final = texto_total
    elif valor_porcentual is not None:
        texto_porcentual = f"{valor_porcentual * 100:.1f}%"
        texto_final = texto_porcentual
    else:
        texto_final = ""

    # Format the percentage change
    if cambio_porcentual is not None:
        if cambio_porcentual < 1:
            percentage = (1 - cambio_porcentual) * 100
            color = "green"
            percentage_text = f'<div style="font-size: 0.8rem; color: {color}; font-weight: 500;">-{percentage:.1f}%</div>'
        elif cambio_porcentual == 1:
            percentage_text = ""
        else:
            percentage = (cambio_porcentual - 1) * 100
            color = "red"
            percentage_text = f'<div style="font-size: 0.8rem; color: {color}; font-weight: 500;">{percentage:+.1f}%</div>'
    else:
        percentage_text = ""

    # HTML for the custom metric
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
        {percentage_text} <!-- Add percentage change below the main value -->
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)