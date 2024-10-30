# Importar bibliotecas
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy import stats

# Cargar archivos CSV
csv_files = {
    "Austin": "csv_files/Archivoaustin1limpio.csv",
    "Charlotte": "csv_files/Archivocharlotte1limpio.csv",
    "San Francisco": "csv_files/ArchivoSanFrancisco2limpio.csv"
}

selected_city = st.selectbox("Selecciona el archivo para analizar:", list(csv_files.keys()))
selected_file_path = csv_files[selected_city]
df = pd.read_csv(selected_file_path)

# Opciones de gráfico
chart_options = ["Distribución de Calificación", "Distribución de Precio", "Precio por Tipo de Anfitrión",
                 "Relación Precio-Calificación", "Tiempo de Hospedaje", "3D Interactivo"]

# Selección de gráfico
selected_chart = st.selectbox("Selecciona el gráfico que deseas ver:", chart_options)

# Paleta futurista
palette = ['#16C6F5', '#FFD700', '#FF69B4', '#7CFC00']

# Función para gráficos 2D
def plot_chart(chart_type):
    if chart_type == "Distribución de Calificación":
        st.header("Distribución de Calificación")
        fig = px.histogram(df, x='rating', nbins=20, title='Distribución de Calificación',
                           color_discrete_sequence=[palette[0]])
        fig.update_layout(xaxis_title="Calificación", yaxis_title="Frecuencia", title_x=0.5)
        st.plotly_chart(fig)

    elif chart_type == "Distribución de Precio":
        st.header("Distribución de Precio")
        fig = px.histogram(df, x='price', nbins=20, title='Distribución de Precio',
                           color_discrete_sequence=[palette[1]])
        fig.add_vline(x=df['price'].mean(), line_dash="dash", line_color=palette[2], 
                      annotation_text="Media", annotation_position="top right")
        fig.update_layout(xaxis_title="Precio", yaxis_title="Frecuencia", title_x=0.5)
        st.plotly_chart(fig)

    elif chart_type == "Precio por Tipo de Anfitrión":
        st.header("Distribución de Precio por Tipo de Anfitrión")
        fig = px.violin(df, x='type_host', y='price', box=True, points="all", title="Distribución de Precio por Tipo de Anfitrión",
                        color_discrete_sequence=[palette[3]])
        fig.update_layout(xaxis_title="Tipo de Anfitrión", yaxis_title="Precio", title_x=0.5)
        st.plotly_chart(fig)

    elif chart_type == "Relación Precio-Calificación":
        st.header("Relación entre Precio y Calificación")
        fig = px.density_heatmap(df, x='price', y='rating', title="Relación entre Precio y Calificación",
                                 color_continuous_scale='Plasma')
        fig.update_layout(xaxis_title="Precio", yaxis_title="Calificación", title_x=0.5)
        st.plotly_chart(fig)

    elif chart_type == "Tiempo de Hospedaje":
        st.header("Distribución del Tiempo de Hospedaje")
        fig = px.histogram(df, x='hosting_time', nbins=20, title='Distribución del Tiempo de Hospedaje',
                           color_discrete_sequence=[palette[2]])
        fig.add_vline(x=df['hosting_time'].median(), line_dash="dash", line_color="red", 
                      annotation_text="Mediana", annotation_position="top right")
        fig.update_layout(xaxis_title="Años de Hospedaje", yaxis_title="Frecuencia", title_x=0.5)
        st.plotly_chart(fig)

# Gráfico 3D Interactivo
def plot_3d():
    st.header("Gráfico 3D Interactivo")
    x_axis = st.selectbox("Selecciona el eje X:", df.columns, index=list(df.columns).index('rating'))
    y_axis = st.selectbox("Selecciona el eje Y:", df.columns, index=list(df.columns).index('price'))
    z_axis = st.selectbox("Selecciona el eje Z:", df.columns, index=list(df.columns).index('number_reviews'))
    color_option = st.selectbox("Selecciona la variable de color:", df.columns)

    fig = px.scatter_3d(df, x=x_axis, y=y_axis, z=z_axis, color=color_option,
                        size_max=18, opacity=0.8,
                        color_continuous_scale='Viridis',
                        title=f'Relación entre {x_axis}, {y_axis}, y {z_axis}')
    st.plotly_chart(fig)

# Mostrar gráfico seleccionado
if selected_chart == "3D Interactivo":
    plot_3d()
else:
    plot_chart(selected_chart)
