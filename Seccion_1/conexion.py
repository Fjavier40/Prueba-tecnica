from dotenv import load_dotenv
import os
import psycopg2

# Cargar variables del .env
load_dotenv()

def get_db_connection():
    """
    Devuelve una conexión a la base de datos PostgreSQL usando datos del .env.
    """
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST", "localhost"),  # por defecto localhost
            port=os.getenv("DB_PORT", "5432")        # por defecto 5432
        )
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None