import pandas as pd
from conexion import get_db_connection

# Extracción de información

"""
Se utilizó Python para procesar y extraer los datos de la fuente original.
Se eligió Python porque permite manipular fácilmente los datos con Pandas y revisar los datos con jupyter notebook,convertir formatos, 
manejar nulos y preparar la información antes de guardarla.
El formato final elegido fue CSV, por su compatibilidad con múltiples herramientas y bases de datos.
Reto: Los campos de fecha y nulos requieren tratamiento especial para mantener consistencia antes de cargar en la base de datos.
"""

# -----------------------------
# Conectarse a la base de datos
# -----------------------------
conn = get_db_connection()

# -----------------------------
# Leer la tabla raw_data
# -----------------------------
query = "SELECT * FROM raw_data"
df = pd.read_sql(query, conn)

conn.close()
print("✅ Datos extraídos desde la base de datos")

# # -----------------------------
# # Guardar en formato CSV
# # -----------------------------

df.to_csv("raw_data_extracted.csv", index=False)
print("✅ Datos guardados en 'raw_data_extracted.csv'")