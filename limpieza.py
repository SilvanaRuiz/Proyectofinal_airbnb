def clean_airbnb_data(df):
    #Eliminamos columna unnamed
    df = df.drop(columns='Unnamed: 0')
    
    #Convertir 'rating' a float
    
    df.replace({'rating':'reviews'}, np.nan, inplace=True)
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    #Extraemos el currency
    df['currency'] = df['price'].str.extract(r'([^\d.,]+)')
    #Limpiar y convertir la columna 'price' en valores numéricos
    df['price'] = df['price'].str.replace(r'[^\d.,]', '', regex=True)
    df['price'] = pd.to_numeric(df['price'].str.replace(',', ''), errors='coerce')
    
    #Extraer el número de años de 'hosting_time'
    df['hosting_time'] = df['hosting_time'].str.extract(r'(\d+)').astype(float)
    
    #'type_host' a categoría y eliminamos lo de bathroom
    df['type_host'] = df['type_host'].str.replace(r' · (Shared bathroom|Shared half bathroom|No bathroom)', '', regex=True)
    df.replace({'type_host':''}, np.nan, inplace=True)
    df.replace({'type_host':np.nan}, 'no_category', inplace=True)
   
    #Reordenar columnas
    column_order = ['guest_favorite', 'rating', 'number_reviews', 'type_host', 
                    'hosting_time', 'price','currency',  'all_reviews']
    df = df[column_order]
    
    return df
df_clean = clean_airbnb_data(df)