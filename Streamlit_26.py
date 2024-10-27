import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
import requests
from bs4 import BeautifulSoup
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
import os
from creacion_reseñas import extraer_datos_y_unir_2
from sklearn.preprocessing import OneHotEncoder
import pickle
import zipfile

# Cargar variables de entorno y configurar la página
load_dotenv()
st.set_page_config(page_title="Análisis de Mercado de Airbnb", layout="wide")

# Inicializar el estado de la sesión
if 'anuncios_analizados' not in st.session_state:
    st.session_state.anuncios_analizados = pd.DataFrame()
if 'modelo' not in st.session_state:
    st.session_state.modelo = None


try:
    # Intentar cargar el archivo CSV
    df = pd.read_csv('Airbnb.csv')
    print("Archivo CSV cargado exitosamente.")
except FileNotFoundError:
    print("Archivo 'Airbnb.csv' no encontrado. Intentando descomprimir 'Airbnb.csv.zip'...")
    
    # Intentar descomprimir el archivo zip
    try:
        with zipfile.ZipFile('Airbnb.csv.zip', 'r') as zip_ref:
            zip_ref.extractall()  # Extrae todos los archivos en el directorio actual
        print("Archivo descomprimido exitosamente.")

        # Intentar cargar el CSV nuevamente después de descomprimir
        df = pd.read_csv('Airbnb.csv')
        print("Archivo CSV cargado exitosamente después de descomprimir.")
        
    except FileNotFoundError:
        print("Archivo 'Airbnb.csv.zip' no encontrado. Verifica que el archivo esté en el directorio.")
    except zipfile.BadZipFile:
        print("El archivo 'Airbnb.csv.zip' está dañado o no es un archivo ZIP válido.")

# Convertir el resultado de unique() a una lista
ciudades = df['city'].unique().tolist()



def obtener_imagen_ciudad(city):
    """
    Función para obtener una imagen de una ciudad usando la API de Unsplash.
    """

    UNSPLASH_ACCESS_KEY = "qIKU6eUBiJ8lMpCHpqcodHhixpEMvX-yh6UVam0whxQ"
    # Agregar "city" al término de búsqueda para especificar que queremos una imagen de la ciudad
    query = f"{city} city"
    url = f"https://api.unsplash.com/search/photos?query={query}&client_id={UNSPLASH_ACCESS_KEY}&per_page=1"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            return data["results"][0]["urls"]["regular"]
        else:
            st.write(f"No se encontraron imágenes para la ciudad: {city}")
            return None
    else:
        st.write("Error al conectarse a la API de Unsplash.")
        return None
def analisis_resenas():
    """
    Función para mostrar un análisis de las predicciones frente a los valores reales en Streamlit,
    mostrando el título de cada Airbnb individualmente con sus tablas respectivas.
    """
    
    st.header('Confrontando Ratings: Un Análisis Comparativo entre Opiniones de Usuarios y Calificaciones de Airbnb según Sentimiento en Reseñas')
    st.markdown("⚠️ *Warning: Estas métricas fueron previamente calculadas, dada la carga computacional que requiere no se puede hacer en el momento.*")

    # Extraer los datos
    predicciones_df = extraer_datos_y_unir_2()

    # Obtener las ciudades únicas de la columna 'city'
    ciudades_unicas = predicciones_df['city'].unique()

    # Sidebar para selección de ciudad y navegación
    st.sidebar.title("🏙️ Selecciona una ciudad")
    
    # Usar las ciudades únicas en el selectbox de la barra lateral
    ciudad_seleccionada = st.sidebar.selectbox("Ciudad", ciudades_unicas)

    # Filtrar el DataFrame por la ciudad seleccionada
    df_ciudad = predicciones_df[predicciones_df['city'] == ciudad_seleccionada].head(2)

    # Obtener la URL de la imagen de Unsplash para la ciudad seleccionada
    imagen_url = obtener_imagen_ciudad(ciudad_seleccionada)

    # Crear columnas: imagen a la izquierda, datos a la derecha
    col1, col2 = st.columns([1, 2])  # Ajusta las proporciones si es necesario

    # Mostrar imagen en la primera columna
    with col1:
        if imagen_url:
            st.image(imagen_url, caption=ciudad_seleccionada, use_column_width=True)

    # Mostrar los datos de los Airbnbs en la segunda columna
    with col2:
        for idx, row in df_ciudad.iterrows():
            # Subtítulo con el título de cada Airbnb
            st.subheader(f"Título: {row['title']}")

            # Crear DataFrame para Predicción NLP y Rating Real
            tabla_pred = pd.DataFrame({
                "Rating Real": [row['Valor Real']],
                "Predicción NLP": [row['Predicción']]
            })

            # Estilo para la tabla de predicciones
            tabla_pred = tabla_pred.reset_index(drop=True)
            tabla_pred_style = tabla_pred.style.set_properties(**{
                'border-color': 'black',
                'border-width': '1px',
                'border-style': 'solid'
            }).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#f0f0f0'), ('color', 'black'), ('font-weight', 'bold'), ('border', '1px solid black')]}
            ])
            st.write(tabla_pred_style.to_html(), unsafe_allow_html=True)

            # Crear DataFrame con características adicionales
            tabla_caracteristicas = pd.DataFrame({
                "Precio": [int(row['price'])],
                "Tipo de Huésped": [row['type_host']],
                "Número de Reseñas": [int(row['number_reviews'])],
                "Número de Huéspedes": [int(row['number_guest'])],
                "Número de Habitaciones": [int(row['number_bedroom'])],
                "Número de Camas": [int(row['number_beds'])],
                "Tipo de Baño": [row['type_bathroom']],
                "Número de Baños": [int(row['number_bathroom'])]
            })

            # Estilo para la tabla de características adicionales
            tabla_caracteristicas = tabla_caracteristicas.reset_index(drop=True)
            tabla_caracteristicas_style = tabla_caracteristicas.style.set_properties(**{
                'border-color': 'black',
                'border-width': '1px',
                'border-style': 'solid'
            }).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#f0f0f0'), ('color', 'black'), ('font-weight', 'bold'), ('border', '1px solid black')]}
            ])
            st.write(tabla_caracteristicas_style.to_html(), unsafe_allow_html=True)

def modelo_prediccion():
    st.header("Modelo de Predicción de Precios")
      # Cargar el modelo de clasificación entrenado
    with open('objetos/modelo_clasificacion.pkl', 'rb') as file:
        modelo_clasificacion = pickle.load(file)
    
    # Cargar los modelos de regresión entrenados para cada clúster
    with open('objetos/modelo_c0.pkl', 'rb') as file:
        modelo_c0 = pickle.load(file)
    with open('objetos/modelo_c1.pkl', 'rb') as file:
        modelo_c1 = pickle.load(file)
    with open('objetos/modelo_c2.pkl', 'rb') as file:
        modelo_c2 = pickle.load(file)
    
    # Cargar los percentiles del error absoluto para cada modelo
    with open('objetos/percentiles_modelo0.pkl', 'rb') as file:
        percentil_inferior0, percentil_superior0 = pickle.load(file)
    with open('objetos/percentiles_modelo1.pkl', 'rb') as file:
        percentil_inferior1, percentil_superior1 = pickle.load(file)
    with open('objetos/percentiles_modelo2.pkl', 'rb') as file:
        percentil_inferior2, percentil_superior2 = pickle.load(file)

    # Cargar los encoders y columnas
    with open('objetos/encoder_city.pkl', 'rb') as file:
        encoder_city = pickle.load(file)
    with open('objetos/city_columns.pkl', 'rb') as file:
        city_columns = pickle.load(file)
    with open('objetos/encoder_bathroom.pkl', 'rb') as file:
        encoder_bathroom = pickle.load(file)
    with open('objetos/bathroom_columns.pkl', 'rb') as file:
        bathroom_columns = pickle.load(file)
    with open('objetos/columnas_X.pkl', 'rb') as file:
        columnas_X = pickle.load(file)

    # Input del usuario para ingresar los datos de predicción
    st.title("Estimación de Rango de Precios")
    
    # Seleccionar las ciudades desde el DataFrame
    ciudades = df['city'].unique()
    city = st.selectbox("Ciudad", ciudades)
    type_bathroom = st.selectbox("Tipo de baño", ["private", "shared"])
    number_bedroom = st.number_input("Número de habitaciones", min_value=0, step=1)
    number_beds = st.number_input("Número de camas", min_value=0, step=1)
    number_guest = st.number_input("Número de huéspedes", min_value=1, step=1)

    # Botón de predicción
    if st.button("Calcular Rango de Precios"):
        # Crear un DataFrame con los datos del usuario
        nuevos_datos = {
            "city": [city],
            "type_bathroom": [type_bathroom],
            "number_bedroom": [number_bedroom],
            "number_beds": [number_beds],
            "number_guest": [number_guest]
        }
        df_nuevos_datos = pd.DataFrame(nuevos_datos)

        # Aplicar las transformaciones de One-Hot Encoding
        city_encoded = encoder_city.transform(df_nuevos_datos[['city']]).toarray()
        city_df = pd.DataFrame(city_encoded, columns=city_columns)
        
        bathroom_encoded = encoder_bathroom.transform(df_nuevos_datos[['type_bathroom']]).toarray()
        bathroom_df = pd.DataFrame(bathroom_encoded, columns=bathroom_columns)

        # Combinar todas las columnas
        df_nuevos_datos = pd.concat([df_nuevos_datos.reset_index(drop=True), city_df, bathroom_df], axis=1)
        df_nuevos_datos = df_nuevos_datos.reindex(columns=columnas_X, fill_value=0)

        # **Paso 1**: Predecir el clúster usando el modelo de clasificación
        cluster_predicho = modelo_clasificacion.predict(df_nuevos_datos)[0]
        
        # **Paso 2**: Seleccionar el modelo de regresión adecuado y sus percentiles
        if cluster_predicho == 0:
            modelo_regresion = modelo_c0
            percentil_superior = percentil_superior0
            percentil_inferior = percentil_inferior0
        elif cluster_predicho == 1:
            modelo_regresion = modelo_c1
            percentil_superior = percentil_superior1
            percentil_inferior = percentil_inferior1
        else:
            modelo_regresion = modelo_c2
            percentil_superior = percentil_superior2
            percentil_inferior = percentil_inferior2

        # **Paso 3**: Realizar la predicción con el modelo de regresión
        prediccion = modelo_regresion.predict(df_nuevos_datos)

        # Calcular el rango de precios usando los percentiles
        intervalo_inferior = prediccion[0] - percentil_superior
        intervalo_superior = prediccion[0] + percentil_superior

        # Mostrar el resultado en Streamlit
        st.write(f"**Precio estimado:** ${prediccion[0]:.2f}")
        st.write(f"**Rango de precios estimado:** ${intervalo_inferior:.2f} - ${intervalo_superior:.2f}")



# Aplicación principal
def main():
    st.sidebar.title("Índice")
    page = st.sidebar.selectbox("Selecciona una página", ("Inicio", "Análisis de Reseñas", "Modelo de Predicción"))
    
    st.title(f"🏠 Bienvenido a Airbnb Insights")
    st.markdown("""
    <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
    <h3 style='color: #1e3d59;'>Descubre el potencial de Airbnb en tu ciudad</h3>
    <p>Esta aplicación te ofrece un análisis detallado del mercado de Airbnb, incluyendo:</p>
    <ul>
        <li>Análisis exploratorio de datos</li>
        <li>Análisis de sentimiento de reseñas</li>
        <li>Calculadora para estimar ingresos potenciales</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    if page == "Análisis de Reseñas":
        analisis_resenas()
  
    elif page == "Modelo de Predicción":
        modelo_prediccion()

if __name__ == "__main__":
    main()
