import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv 
from conexion import get_db_connection
'''Primero vamos a crear una base de dstos llamada etl_db y cargar el dataset en csv proporcionado a la base de datos, en crudo, tal cual estan para 
poder manejarlos desde una base de datos 

Se eligio posgreSQL porque es gestor de base de datos relacional que viene muy bien para datos estructurados como los que se tienen en el dataset,
además de que es open source, es robusto y es el que más he usado
'''

#Carga las variables del .env
load_dotenv() 

# Obtener las variables
dbname = os.getenv("DB_NAME_DEFAULT")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")

# Conectarse a la base default 'postgres'

conn = psycopg2.connect(
    dbname= dbname,
    user= user,
    password= password,
    host= host,
    port= port
)
conn.autocommit = True  # Necesario para CREATE DATABASE
cur = conn.cursor()


# Crear la base de datos etl_db

cur.execute("DROP DATABASE IF EXISTS etl_db")
cur.execute("""
    CREATE DATABASE etl_db
    WITH ENCODING 'UTF8'
    LC_COLLATE 'Spanish_Mexico.1252'
    LC_CTYPE 'Spanish_Mexico.1252'
""")
cur.close()
conn.close()
print("✅ Base de datos 'etl_db' creada")


# Conectarse a la nueva base

conn = get_db_connection()
cur = conn.cursor()


# Crear tabla genérica para el CSV
# Se intento cargar los datos con el tipo de dato fecha y numero, pero había inconsistencias en el CSV por lo que se opto por dar a todas las 
# columnas el formato varchar y ya despues en el proceso de transformacion se arreglaran.

cur.execute("""
CREATE TABLE IF NOT EXISTS raw_data (
    id VARCHAR(64),
    name VARCHAR(130),
    company_id VARCHAR(64),
    amount VARCHAR(40),
    status VARCHAR(30),
    created_at VARCHAR(30),
    paid_at VARCHAR(30)
)
""")
conn.commit()
print("✅ Tabla 'raw_data' creada")


# Leer CSV (dataset) y cargar datos

df = pd.read_csv("data_prueba_tecnica.csv")  # Ajusta la ruta si es necesario
df = df.where(pd.notnull(df), None)

for row in df.itertuples(index=False):
    cur.execute("""
        INSERT INTO raw_data (id, name, company_id, amount, status, created_at, paid_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, row)

conn.commit()
cur.close()
conn.close()
print("✅ CSV cargado en la tabla 'raw_data'")
