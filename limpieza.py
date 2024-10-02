def clean_airbnb_data(df):
    #Eliminamos columna unnamed
    df = df.drop(columns='Unnamed: 0')
    
    #Convertir 'rating' a float
    df.replace({'rating':'reviews'}, np.nan, inplace=True)
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

    #Extraemos el currency y creamos nueva columna
    df['currency'] = df['price'].str.extract(r'([^\d.,]+)')
    #Limpiar y convertir la columna 'price' en valores numéricos
    df['price'] = df['price'].str.replace(r'[^\d.,]', '', regex=True)
    df['price'] = pd.to_numeric(df['price'].str.replace(',', ''), errors='coerce')

    #Convertir el hosting time a meses, para tener una medida uniforme
    def convert_to_months(time_str):
        if 'year' in time_str:
            years = int(re.findall(r'(\d+)', time_str)[0])
            months = years * 12
        elif 'month' in time_str:
            months = int(re.findall(r'(\d+)', time_str)[0])
        else:
            months = 0
        return months
    
    df['hosting_time']= df['hosting_time'].apply(convert_to_months)
    
    #'type_host' a categoría y eliminamos lo de bathroom
    df['type_host'] = df['type_host'].str.replace(r' · (Shared bathroom|Shared half bathroom|No bathroom)', '', regex=True)
    df.replace({'type_host':''}, np.nan, inplace=True)
    df.replace({'type_host':np.nan}, 'no_category', inplace=True)

    #Por problemas de scrapping hay datos que no hemos podido obtener pero obtendremos, por el momento eliminaremos las colundas con Nan
    for i, row in df.iterrows():
        if row.isnull().any(): 
            df.drop(i, inplace=True)
   
    #Reordenar columnas
    column_order = ['guest_favorite', 'rating', 'number_reviews', 'type_host', 
                    'hosting_time', 'price','currency',  'all_reviews']
    df = df[column_order]
    
    return df
df_clean = clean_airbnb_data(df)
