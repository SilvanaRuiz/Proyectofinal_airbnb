import streamlit as st

import requests

def intro():
    st.title(":blue[_Bienvenido a tu app de Airbnb_]")
    st.markdown("Esta aplicación te permitirá realizar un estudio de mercado a través de la exploración de distintos alojamientos de Airbnb en la ciudad de tu elección. Con ella, podrás analizar datos clave para obtener una visión más clara sobre tendencias, precios y oportunidades del mercado en tu área de interés.")
    # Solicitar al usuario que ingrese el nombre de su ciudad
    

    # Mostrar el nombre de la ciudad ingresada

    # API de Unsplash (necesitas tu propia API key)
    UNSPLASH_ACCESS_KEY = "qIKU6eUBiJ8lMpCHpqcodHhixpEMvX-yh6UVam0whxQ"

    # Solicitar el nombre de la ciudad
    city = st.text_input("Inserte el nombre de su ciudad:")

    if city:
        # Endpoint de Unsplash para buscar fotos de la ciudad
        url = f"https://api.unsplash.com/search/photos?query={city}&client_id={UNSPLASH_ACCESS_KEY}&per_page=1"

        # Realizar la solicitud a Unsplash
        response = requests.get(url)

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            data = response.json()
            if data["results"]:
                # Obtener la URL de la primera imagen
                image_url = data["results"][0]["urls"]["regular"]
                st.image(image_url, caption=f"Foto de {city}")
            else:
                st.write("No se encontraron imágenes para la ciudad solicitada.")
        else:
            st.write("Error al conectarse a la API de Unsplash.")


def page_1():
    st.title("Prueba")

st.sidebar.title("Indice")
page = st.sidebar.selectbox("Selecciona una página", ("Inicio", "Prueba"))

if page == "Inicio":
    intro()
elif page == "Contacto":
    page_1()



