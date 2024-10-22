import pandas as pd
from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid  #Modulo para generar identificadores únicos

import pandas as pd
from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import sessionmaker, declarative_base
import pymysql
import uuid  # Importar el módulo uuid para generar IDs únicos

# Crear la base declarativa para el ORM de SQLAlchemy
Base = declarative_base()

# Definir la clase Airbnb que mapea a la tabla airbnb_listings_1
class Airbnb(Base):
    __tablename__ = 'airbnb_listings_1'

    # unique_id ahora es la clave primaria
    unique_id = Column(String(50), primary_key=True, unique=True)  # UUID como clave primaria
    title = Column(String(200))
    city = Column(String(200))
    guest_favorite = Column(String(200))
    rating = Column(Text)
    number_reviews = Column(String(200))
    type_host = Column(String(200))
    hosting_time = Column(String(200))
    price = Column(String(200))
    all_reviews = Column(LONGTEXT)
    complete_data_list = Column(Text)
    url = Column(Text)  # Columna para almacenar la URL completa
    id_url = Column(String(100))  # Columna para almacenar el ID extraído de la URL


def bd(df):
    # Reemplazar los NaN con None
    df = df.where(pd.notnull(df), None)
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
    # type_host los None son normal
    df['type_host'] = df['type_host'].apply(lambda x: 'normal' if pd.isna(x) else x)

    # Función para crear el esquema y popular la base de datos
    def create_schema_and_populate_db(df):
        # Ajusta el URI de la conexión a MySQL
        engine = create_engine('mysql+pymysql://root:password@localhost/Airbnb')

        # Crear el esquema (si no existe)
        Base.metadata.create_all(engine)

        # Crear una sesión
        Session = sessionmaker(bind=engine)
        session = Session()

        # Insertar los datos del DataFrame
        for _, row in df.iterrows():
            # Generar un unique_id usando uuid
            unique_id = str(uuid.uuid4())  # Generar un UUID único

            try:
                # Crear la entrada de Airbnb
                listing = Airbnb(
                    unique_id=unique_id,  # Asignar el UUID generado como clave primaria
                    title=row.get('title', None),
                    city=row.get('city', None),  # Usamos .get() para prevenir errores si falta la columna
                    guest_favorite=row.get('guest_favorite', None),  # Usamos .get() para obtener el valor o None si no existe
                    rating=row.get('rating', None),  # Usamos .get() para prevenir errores
                    type_host=row.get('type_host', None),
                    hosting_time=row.get('hosting_time', None),  # Si la columna no existe, devuelve None
                    price=row.get('price', None),  # Usamos .get() para prevenir errores
                    number_reviews=row.get('number_reviews', None),  # Usamos .get() para obtener el valor o None si no existe
                    all_reviews=row.get('all_reviews', None),
                    complete_data_list=row.get('complete_data_list', None),  # Nueva columna incluida
                    id_url=row.get('id_url', None),  # Guardar el ID extraído de la URL
                    url=row.get('url', None)  # Guardar la URL completa
                )

                # Usar merge para actualizar si ya existe
                session.merge(listing)

            except Exception as e:
                print(f"Error al insertar los datos: {e}")
                continue

        # Confirmar la transacción
        session.commit()

        # Cerrar la sesión
        session.close()

    # Llamar a la función para crear el esquema y popular la BD
    create_schema_and_populate_db(df)



def extract_data_from_db():
    # Ajusta el URI de la conexión a MySQL
    engine = create_engine('mysql+pymysql://root:password@localhost/Airbnb')

    # Consulta SQL para seleccionar todos los registros de la tabla airbnb_listings
    query = "SELECT * FROM airbnb_listings_1"

    # Leer los datos directamente en un DataFrame
    df = pd.read_sql(query, engine)

    return df

