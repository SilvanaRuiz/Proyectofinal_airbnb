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

# Cargar variables de entorno y configurar la página
load_dotenv()
st.set_page_config(page_title="Análisis de Mercado de Airbnb", layout="wide")

# Inicializar el estado de la sesión
if 'anuncios_analizados' not in st.session_state:
    st.session_state.anuncios_analizados = pd.DataFrame()
if 'modelo' not in st.session_state:
    st.session_state.modelo = None

# Funciones auxiliares (se mantienen igual)
def conectar_a_base_de_datos():
    pass

def ejecutar_proceso_etl():
    pass

@st.cache_data
def cargar_datos():
    # Datos de ejemplo
    return pd.DataFrame({
        'ciudad': np.random.choice(['Barcelona', 'Madrid', 'Valencia'], 1000),
        'precio': np.random.randint(20, 500, 1000),
        'tipo_habitacion': np.random.choice(['Habitación privada', 'Apartamento entero', 'Habitación compartida'], 1000),
        'numero_resenas': np.random.randint(0, 100, 1000),
        'barrio': np.random.choice(['Centro', 'Eixample', 'Gràcia', 'Sants', 'Sant Martí'], 1000),
        'latitud': np.random.uniform(41.3, 41.5, 1000),
        'longitud': np.random.uniform(2.1, 2.3, 1000),
        'habitaciones': np.random.randint(1, 5, 1000),
        'huespedes': np.random.randint(1, 8, 1000),
        'banos': np.random.randint(1, 4, 1000),
    })





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

    # Iterar sobre cada ciudad y mostrar la imagen y los datos individuales de cada Airbnb
    for ciudad in ciudades_unicas:
        # Obtener la URL de la imagen de Unsplash para la ciudad
        imagen_url = obtener_imagen_ciudad(ciudad)
        
        # Filtrar el DataFrame por la ciudad actual y limitar a dos ejemplos
        df_ciudad = predicciones_df[predicciones_df['city'] == ciudad].head(2)

        # Crear columnas: imagen a la izquierda, datos a la derecha
        col1, col2 = st.columns([1, 2])  # Ajusta las proporciones si es necesario

        # Mostrar imagen en la primera columna
        with col1:
            if imagen_url:
                st.image(imagen_url, caption=ciudad, use_column_width=True)

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
    
    df = cargar_datos()
    
    X = df[['habitaciones', 'huespedes', 'banos']]
    y = df['precio']
    
    # Dividir datos
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    if st.button("Entrenar Modelo"):
        # Entrenar modelo
        modelo = RandomForestRegressor(n_estimators=100, random_state=42)
        modelo.fit(X_train, y_train)
        
        # Guardar modelo en el estado de la sesión
        st.session_state.modelo = modelo
        
        # Hacer predicciones
        y_pred = modelo.predict(X_test)
        
        # Evaluar modelo
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        st.success("Modelo entrenado con éxito!")
        st.write(f"Error Cuadrático Medio: {mse:.2f}")
        st.write(f"Puntuación R-cuadrado: {r2:.2f}")
        
        # Importancia de características
        importancia_caracteristicas = pd.DataFrame({'caracteristica': X.columns, 'importancia': modelo.feature_importances_})
        importancia_caracteristicas = importancia_caracteristicas.sort_values('importancia', ascending=False)
        
        st.subheader("Importancia de Características")
        fig = px.bar(importancia_caracteristicas, x='caracteristica', y='importancia')
        st.plotly_chart(fig)
    
    # Predicción interactiva
    st.subheader("Predicción de Precio")
    col1, col2, col3 = st.columns(3)
    with col1:
        habitaciones = st.number_input("Número de habitaciones", min_value=1, max_value=10, value=2)
    with col2:
        huespedes = st.number_input("Número de huéspedes", min_value=1, max_value=16, value=4)
    with col3:
        banos = st.number_input("Número de baños", min_value=1, max_value=8, value=1)
    
    if st.button("Predecir Precio"):
        if st.session_state.modelo:
            precio_predicho = st.session_state.modelo.predict([[habitaciones, huespedes, banos]])[0]
            st.success(f"El precio predicho es: ${precio_predicho:.2f}")
        else:
            st.error("El modelo no está entrenado. Por favor, entrena el modelo primero.")

# Aplicación principal
def main():
    st.sidebar.title("Índice")
    page = st.sidebar.selectbox("Selecciona una página", ("Inicio", "Panel Principal", "Análisis de Reseñas", "Herramienta de Análisis de IA", "Modelo de Predicción"))
    

    if page == "Análisis de Reseñas":
        analisis_resenas()
  
    elif page == "Modelo de Predicción":
        modelo_prediccion()

if __name__ == "__main__":
    main()
