# Importar bibliotecas
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv('csv_files/ArchivoSanFrancisco2limpio.csv') 

#Agraga los archivos
csv_files = {
    "Austin": "csv_files/Archivoaustin1limpio.csv",
    "Charlotte": "csv_files/Archivocharlotte1limpio.csv",
    "San Francisco": "csv_files/ArchivoSanFrancisco2limpio.csv"
    
}

selected_city = st.selectbox("Selecciona el archivo para analizar:", list(csv_files.keys()))

selected_file_path = csv_files[selected_city]
df = pd.read_csv(selected_file_path)

# Muestra
st.write(f"Archivo seleccionado: {selected_city}")

#estilos
sns.set(style="whitegrid")  # Fondo claro
palette = ['#FF5A5F', '#FFB400', '#00A699', '#FC642D']  # Paleta Airbnb

# Título
st.title("Visualización de Datos de Airbnb:")

# Sidebar ( por si lo usare)
st.sidebar.title("Información General")
st.sidebar.markdown("Esta aplicación permite explorar datos clave de alojamientos en Airbnb.")
st.sidebar.markdown("Histogramas y gráficos de barras:  ")
st.sidebar.markdown("Estos gráficos muestran cómo están distribuidos los valores en cada variable, permitiendo detectar si siguen una distribución normal o si presentan sesgos, datos atípicos o asimetrías.")
st.sidebar.markdown("Gráficos de densidad:  ")
st.sidebar.markdown("Ayudan a visualizar las distribuciones de manera más detallada que los histogramas, lo cual es útil para variables numéricas continuas y para comparar distribuciones entre subgrupos.")









#######################################################################

# Distribución de Calificación
st.header("Distribución de Calificación")
st.markdown("Este gráfico muestra la distribución de las calificaciones de los alojamientos en la plataforma, permitiendo ver su concentración.")
plt.figure(figsize=(10, 6))
sns.histplot(df['rating'], kde=True, bins=20, color=palette[0], edgecolor='black')
sns.kdeplot(df['rating'], color=palette[2], lw=2.5)
plt.title('Distribución de Calificación', fontsize=18, weight='bold', color=palette[0])
plt.xlabel('Rating', fontsize=14)
plt.ylabel('Frecuencia', fontsize=14)
st.pyplot(plt.gcf())

# Distribución de Precio
st.header("Distribución de Precio")
st.markdown("Este gráfico muestra cómo se distribuyen los precios, resaltando la media para ver la tendencia general.")
plt.figure(figsize=(10, 6))
sns.histplot(df['price'], kde=True, bins=20, color=palette[0], edgecolor='black')
mean_price = df['price'].mean()
plt.axvline(mean_price, color=palette[1], linestyle='--', lw=2)
plt.title('Distribución de Precio', fontsize=18, weight='bold', color=palette[0])
plt.xlabel('Precio', fontsize=14)
plt.ylabel('Frecuencia', fontsize=14)
st.pyplot(plt.gcf())

# Distribución de Precio por Tipo de Anfitrión
st.header("Distribución de Precio por Tipo de Anfitrión")
st.markdown("Visualiza cómo varía el precio según el tipo de anfitrión, mostrando la dispersión de precios en cada categoría.")
plt.figure(figsize=(10, 7))
sns.violinplot(x='type_host', y='price', data=df, inner=None, palette="coolwarm", cut=0)
sns.swarmplot(x='type_host', y='price', data=df, color='black', alpha=0.6)
plt.title('Distribución de Precio por Tipo de Anfitrión', fontsize=18, weight='bold', color=palette[0])
plt.xlabel('Tipo de Anfitrión', fontsize=14)
plt.ylabel('Precio', fontsize=14)
st.pyplot(plt.gcf())

# Relación entre Precio y Calificación
st.header("Relación entre Precio y Calificación")
st.markdown("Este gráfico hexbin muestra la relación entre el precio y la calificación de los alojamientos.")
plt.figure(figsize=(10, 7))
plt.hexbin(df['price'], df['rating'], gridsize=30, cmap='viridis', mincnt=1)
plt.colorbar(label='Frecuencia')
plt.title('Relación entre Precio y Calificación', fontsize=18, weight='bold')
plt.xlabel('Precio', fontsize=14)
plt.ylabel('Calificación', fontsize=14)
st.pyplot(plt.gcf())

# Distribución del Tiempo de Hospedaje
st.header("Distribución del Tiempo de Hospedaje")
st.markdown("Este gráfico presenta la distribución de tiempo de hospedaje, con una línea que marca la mediana.")
plt.figure(figsize=(10, 6))
sns.histplot(df['hosting_time'], kde=True, bins=20, color=palette[3], edgecolor='black')
median_time = df['hosting_time'].median()
plt.axvline(median_time, color='red', linestyle='--', lw=2)
plt.title('Distribución del Tiempo de Hospedaje', fontsize=18, weight='bold', color=palette[3])
plt.xlabel('Años de Hospedaje', fontsize=14)
plt.ylabel('Frecuencia', fontsize=14)
st.pyplot(plt.gcf())

# Relación entre Tiempo de Hospedaje y Precio
st.header("Relación entre Tiempo de Hospedaje y Precio")
st.markdown("Este gráfico muestra la relación entre tiempo de hospedaje y precio.")
plt.figure(figsize=(10, 7))
sns.regplot(x='hosting_time', y='price', data=df, scatter_kws={'color': palette[0]}, line_kws={'color': 'crimson'}, ci=95)
plt.title('Relación entre Tiempo de Hospedaje y Precio', fontsize=18, weight='bold', color='crimson')
plt.xlabel('Tiempo de Hospedaje (Años)', fontsize=14)
plt.ylabel('Precio', fontsize=14)
st.pyplot(plt.gcf())

# Comparación de Distribuciones con Curvas Ideales
st.header("Comparación de Distribuciones con Curvas Ideales")
st.markdown("Este gráfico compara distribuciones clave con una curva normal ideal.")
variables = ['price', 'rating', 'number_reviews', 'hosting_time']
plt.figure(figsize=(12, 10))
for i, var in enumerate(variables):
    plt.subplot(2, 2, i + 1)
    sns.kdeplot(df[var], fill=True, color='orange', alpha=0.6, label='Distribución Observada')
    mu, std = np.mean(df[var]), np.std(df[var])
    x = np.linspace(min(df[var]), max(df[var]), 100)
    p = stats.norm.pdf(x, mu, std) / stats.norm.pdf(x, mu, std).max() * max(plt.ylim())
    plt.plot(x, p, 'r--', label='Distribución Ideal (Normal)', lw=2)
    plt.title(f'Distribución de {var.capitalize()}')
    plt.legend()
st.pyplot(plt.gcf())

# Mapa de Calor de Correlación entre Variables
st.header("Mapa de Calor de Correlación entre Variables")
st.markdown("Este heatmap muestra la correlación entre diferentes variables numéricas en el conjunto de datos.")
plt.figure(figsize=(12, 10))
sns.heatmap(df[['rating', 'number_reviews', 'hosting_time', 'price']].corr(), annot=True, cmap='Pastel1', linewidths=0.5, fmt=".2f")
plt.title('Mapa de Calor de Correlación', fontsize=20, weight='bold')
st.pyplot(plt.gcf())


# # Crear el gráfico 3D
# fig = px.scatter_3d(
#     df, x='rating', y='price', z='number_reviews',
#     color='guest_favorite', size='number_reviews',
#     title='Relación Precio-Rating-Número de Reviews'
# )

# # Título de la aplicación
# st.title("Visualización 3D de Datos de Airbnb")

# # Botón para mostrar el gráfico
# if st.button("Mostrar Gráfico 3D"):
#     st.plotly_chart(fig)

# # # Gráfico 3D de Precio, Calificación y Número de Reseñas
# # st.header("Relación Precio-Rating-Número de Reseñas")
# # fig = px.scatter_3d(df, x='rating', y='price', z='number_reviews', color='guest_favorite', size='number_reviews', title='Relación Precio-Rating-Número de Reviews')
# # st.plotly_chart(fig, use_container_width=True)
