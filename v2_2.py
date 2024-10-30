# Importar bibliotecas
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
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
        plt.figure(figsize=(10, 6))
        sns.histplot(df['rating'], kde=True, bins=20, color=palette[0], edgecolor='white')
        sns.kdeplot(df['rating'], color=palette[2], lw=2.5)
        plt.title('Distribución de Calificación', fontsize=18, color=palette[1], weight='bold')
        plt.xlabel('Rating', fontsize=14, color='white')
        plt.ylabel('Frecuencia', fontsize=14, color='white')
        st.pyplot(plt.gcf())

    elif chart_type == "Distribución de Precio":
        st.header("Distribución de Precio")
        plt.figure(figsize=(10, 6))
        sns.histplot(df['price'], kde=True, bins=20, color=palette[3], edgecolor='white')
        mean_price = df['price'].mean()
        plt.axvline(mean_price, color=palette[1], linestyle='--', lw=2)
        plt.title('Distribución de Precio', fontsize=18, color=palette[3], weight='bold')
        plt.xlabel('Precio', fontsize=14, color='white')
        plt.ylabel('Frecuencia', fontsize=14, color='white')
        st.pyplot(plt.gcf())

    elif chart_type == "Precio por Tipo de Anfitrión":
        st.header("Distribución de Precio por Tipo de Anfitrión")
        plt.figure(figsize=(10, 7))
        sns.violinplot(x='type_host', y='price', data=df, inner=None, palette="coolwarm", cut=0)
        sns.swarmplot(x='type_host', y='price', data=df, color='black', alpha=0.6)
        plt.title('Distribución de Precio por Tipo de Anfitrión', fontsize=18, color=palette[2], weight='bold')
        plt.xlabel('Tipo de Anfitrión', fontsize=14, color='white')
        plt.ylabel('Precio', fontsize=14, color='white')
        st.pyplot(plt.gcf())

    elif chart_type == "Relación Precio-Calificación":
        st.header("Relación entre Precio y Calificación")
        plt.figure(figsize=(10, 7))
        plt.hexbin(df['price'], df['rating'], gridsize=30, cmap='plasma', mincnt=1)
        plt.colorbar(label='Frecuencia')
        plt.title('Relación entre Precio y Calificación', fontsize=18, color=palette[1], weight='bold')
        plt.xlabel('Precio', fontsize=14, color='white')
        plt.ylabel('Calificación', fontsize=14, color='white')
        st.pyplot(plt.gcf())

    elif chart_type == "Tiempo de Hospedaje":
        st.header("Distribución del Tiempo de Hospedaje")
        plt.figure(figsize=(10, 6))
        sns.histplot(df['hosting_time'], kde=True, bins=20, color=palette[2], edgecolor='white')
        median_time = df['hosting_time'].median()
        plt.axvline(median_time, color=palette[1], linestyle='--', lw=2)
        plt.title('Distribución del Tiempo de Hospedaje', fontsize=18, color=palette[2], weight='bold')
        plt.xlabel('Años de Hospedaje', fontsize=14, color='white')
        plt.ylabel('Frecuencia', fontsize=14, color='white')
        st.pyplot(plt.gcf())

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
# Importar bibliotecas
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
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
        plt.figure(figsize=(10, 6))
        sns.histplot(df['rating'], kde=True, bins=20, color=palette[0], edgecolor='white')
        sns.kdeplot(df['rating'], color=palette[2], lw=2.5)
        plt.title('Distribución de Calificación', fontsize=18, color=palette[1], weight='bold')
        plt.xlabel('Rating', fontsize=14, color='white')
        plt.ylabel('Frecuencia', fontsize=14, color='white')
        st.pyplot(plt.gcf())

    elif chart_type == "Distribución de Precio":
        st.header("Distribución de Precio")
        plt.figure(figsize=(10, 6))
        sns.histplot(df['price'], kde=True, bins=20, color=palette[3], edgecolor='white')
        mean_price = df['price'].mean()
        plt.axvline(mean_price, color=palette[1], linestyle='--', lw=2)
        plt.title('Distribución de Precio', fontsize=18, color=palette[3], weight='bold')
        plt.xlabel('Precio', fontsize=14, color='white')
        plt.ylabel('Frecuencia', fontsize=14, color='white')
        st.pyplot(plt.gcf())

    elif chart_type == "Precio por Tipo de Anfitrión":
        st.header("Distribución de Precio por Tipo de Anfitrión")
        plt.figure(figsize=(10, 7))
        sns.violinplot(x='type_host', y='price', data=df, inner=None, palette="coolwarm", cut=0)
        sns.swarmplot(x='type_host', y='price', data=df, color='black', alpha=0.6)
        plt.title('Distribución de Precio por Tipo de Anfitrión', fontsize=18, color=palette[2], weight='bold')
        plt.xlabel('Tipo de Anfitrión', fontsize=14, color='white')
        plt.ylabel('Precio', fontsize=14, color='white')
        st.pyplot(plt.gcf())

    elif chart_type == "Relación Precio-Calificación":
        st.header("Relación entre Precio y Calificación")
        plt.figure(figsize=(10, 7))
        plt.hexbin(df['price'], df['rating'], gridsize=30, cmap='plasma', mincnt=1)
        plt.colorbar(label='Frecuencia')
        plt.title('Relación entre Precio y Calificación', fontsize=18, color=palette[1], weight='bold')
        plt.xlabel('Precio', fontsize=14, color='white')
        plt.ylabel('Calificación', fontsize=14, color='white')
        st.pyplot(plt.gcf())

    elif chart_type == "Tiempo de Hospedaje":
        st.header("Distribución del Tiempo de Hospedaje")
        plt.figure(figsize=(10, 6))
        sns.histplot(df['hosting_time'], kde=True, bins=20, color=palette[2], edgecolor='white')
        median_time = df['hosting_time'].median()
        plt.axvline(median_time, color=palette[1], linestyle='--', lw=2)
        plt.title('Distribución del Tiempo de Hospedaje', fontsize=18, color=palette[2], weight='bold')
        plt.xlabel('Años de Hospedaje', fontsize=14, color='white')
        plt.ylabel('Frecuencia', fontsize=14, color='white')
        st.pyplot(plt.gcf())

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
    plot_chart(selected_chart)
