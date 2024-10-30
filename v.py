# Importar bibliotecas
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import numpy as np
from scipy import stats

# Configuración de archivo
csv_files = {
    "Austin": "csv_files/Archivoaustin1limpio.csv",
    "Charlotte": "csv_files/Archivocharlotte1limpio.csv",
    "San Francisco": "csv_files/ArchivoSanFrancisco2limpio.csv"
}
selected_city = st.selectbox("Selecciona el archivo para analizar:", list(csv_files.keys()))
selected_file_path = csv_files[selected_city]
df = pd.read_csv(selected_file_path)

# Estilos futuristas
sns.set(style="whitegrid")  # Fondo claro para contraste
palette = ['#16C6F5', '#FFD700', '#FF69B4', '#7CFC00']  # Colores brillantes y neón

# Título
st.title("Visualización de Datos de Airbnb: Estilo Futurista")

# Sidebar de información
st.sidebar.title("Información General")
st.sidebar.markdown("Esta aplicación permite explorar datos clave de alojamientos en Airbnb en estilo futurista.")
st.sidebar.markdown("Distribución de calificaciones, precios y más, en gráficos futuristas con paletas brillantes.")

# Gráficas futuristas
#######################################################################

# Distribución de Calificación
st.header("Distribución de Calificación")
st.markdown("Distribución de calificaciones de los alojamientos.")
plt.figure(figsize=(10, 6))
sns.histplot(df['rating'], kde=True, bins=20, color=palette[0], edgecolor='white')
sns.kdeplot(df['rating'], color=palette[2], lw=2.5)
plt.title('Distribución de Calificación', fontsize=18, color=palette[1], weight='bold')
plt.xlabel('Rating', fontsize=14, color='white')
plt.ylabel('Frecuencia', fontsize=14, color='white')
plt.grid(color='grey', linestyle='--', linewidth=0.3)
st.pyplot(plt.gcf())

# Distribución de Precio
st.header("Distribución de Precio")
st.markdown("Distribución de precios, resaltando la media.")
plt.figure(figsize=(10, 6))
sns.histplot(df['price'], kde=True, bins=20, color=palette[3], edgecolor='white')
mean_price = df['price'].mean()
plt.axvline(mean_price, color=palette[1], linestyle='--', lw=2)
plt.title('Distribución de Precio', fontsize=18, color=palette[3], weight='bold')
plt.xlabel('Precio', fontsize=14, color='white')
plt.ylabel('Frecuencia', fontsize=14, color='white')
plt.grid(color='grey', linestyle='--', linewidth=0.3)
st.pyplot(plt.gcf())

# Distribución de Precio por Tipo de Anfitrión
st.header("Distribución de Precio por Tipo de Anfitrión")
plt.figure(figsize=(10, 7))
sns.violinplot(x='type_host', y='price', data=df, inner=None, palette="coolwarm", cut=0)
sns.swarmplot(x='type_host', y='price', data=df, color='black', alpha=0.6)
plt.title('Distribución de Precio por Tipo de Anfitrión', fontsize=18, color=palette[2], weight='bold')
plt.xlabel('Tipo de Anfitrión', fontsize=14, color='white')
plt.ylabel('Precio', fontsize=14, color='white')
plt.grid(color='grey', linestyle='--', linewidth=0.3)
st.pyplot(plt.gcf())

# Relación entre Precio y Calificación
st.header("Relación entre Precio y Calificación")
plt.figure(figsize=(10, 7))
plt.hexbin(df['price'], df['rating'], gridsize=30, cmap='plasma', mincnt=1)
plt.colorbar(label='Frecuencia')
plt.title('Relación entre Precio y Calificación', fontsize=18, color=palette[1], weight='bold')
plt.xlabel('Precio', fontsize=14, color='white')
plt.ylabel('Calificación', fontsize=14, color='white')
plt.grid(color='grey', linestyle='--', linewidth=0.3)
st.pyplot(plt.gcf())

# Distribución del Tiempo de Hospedaje
st.header("Distribución del Tiempo de Hospedaje")
plt.figure(figsize=(10, 6))
sns.histplot(df['hosting_time'], kde=True, bins=20, color=palette[2], edgecolor='white')
median_time = df['hosting_time'].median()
plt.axvline(median_time, color=palette[1], linestyle='--', lw=2)
plt.title('Distribución del Tiempo de Hospedaje', fontsize=18, color=palette[2], weight='bold')
plt.xlabel('Años de Hospedaje', fontsize=14, color='white')
plt.ylabel('Frecuencia', fontsize=14, color='white')
plt.grid(color='grey', linestyle='--', linewidth=0.3)
st.pyplot(plt.gcf())

# Relación entre Tiempo de Hospedaje y Precio
st.header("Relación entre Tiempo de Hospedaje y Precio")
plt.figure(figsize=(10, 7))
sns.regplot(x='hosting_time', y='price', data=df, scatter_kws={'color': palette[0]}, line_kws={'color': palette[1]}, ci=95)
plt.title('Relación entre Tiempo de Hospedaje y Precio', fontsize=18, color=palette[0], weight='bold')
plt.xlabel('Tiempo de Hospedaje (Años)', fontsize=14, color='white')
plt.ylabel('Precio', fontsize=14, color='white')
plt.grid(color='grey', linestyle='--', linewidth=0.3)
st.pyplot(plt.gcf())

# Comparación de Distribuciones con Curvas Ideales
st.header("Comparación de Distribuciones con Curvas Ideales")
variables = ['price', 'rating', 'number_reviews', 'hosting_time']
plt.figure(figsize=(12, 10))
for i, var in enumerate(variables):
    plt.subplot(2, 2, i + 1)
    sns.kdeplot(df[var], fill=True, color=palette[3], alpha=0.6, label='Distribución Observada')
    mu, std = np.mean(df[var]), np.std(df[var])
    x = np.linspace(min(df[var]), max(df[var]), 100)
    p = stats.norm.pdf(x, mu, std) / stats.norm.pdf(x, mu, std).max() * max(plt.ylim())
    plt.plot(x, p, 'r--', label='Distribución Ideal (Normal)', lw=2)
    plt.title(f'Distribución de {var.capitalize()}', fontsize=14, color='white')
    plt.legend()
    plt.grid(color='grey', linestyle='--', linewidth=0.3)
st.pyplot(plt.gcf())

# Mapa de Calor de Correlación entre Variables
st.header("Mapa de Calor de Correlación entre Variables")
plt.figure(figsize=(12, 10))
sns.heatmap(df[['rating', 'number_reviews', 'hosting_time', 'price']].corr(), annot=True, cmap='cool', linewidths=0.5, fmt=".2f", cbar_kws={'label': 'Correlación'})
plt.title('Mapa de Calor de Correlación', fontsize=20, color='white', weight='bold')
plt.grid(color='grey', linestyle='--', linewidth=0.3)
st.pyplot(plt.gcf())
