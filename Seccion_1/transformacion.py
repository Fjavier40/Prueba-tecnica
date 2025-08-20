import pandas as pd
from conexion import get_db_connection

# Transformaciones realizadas:
# 1. Renombrar columnas para mantener consistencia ('name' a 'company_name').
# 2. Ajuste de longitudes de strings para cumplir con los límites de las columnas en la BD.
# 3. Conversión de tipos de datos:
#    - 'amount' a numerico y luego filtrado por el máximo permitido en DECIMAL(16,2)
#    - 'created_at' y 'paid_at' a datetime, con NaT convertidos a None para que se guarden como NULL
# 4. Eliminación de filas incompletas (por ejemplo, si 'id', 'company_id', 'amount', 'status' o 'created_at' eran nulos)

# Retos encontrados:
# - Fechas en formatos mixtos (yyyy-mm-dd, dd/mm/yyyy, y yyyyMMdd) que requerían conversión personalizada.
# - Los valores nulos en fechas que Pandas convierte a NaT y no se guardaban como NULL en la BD.
# - Valores numéricos extremadamente grandes que excedían el límite de DECIMAL(16,2), requiriendo filtrado.
# - Evitar que campos vacíos de texto se conviertan en la cadena 'None' al guardar en la base de datos.


# Se carga de la tabla cruda los datos
df = pd.read_csv("raw_data_extracted.csv")  # Ajusta la ruta si es necesario

# Renombramos el nombre de la columna para que coincida con el esquema dado
df.rename(columns={'name': 'company_name'}, inplace=True)

# Eliminar filas con nulos en columnas donde no se admiten nulos en el esquema
df = df.dropna(subset=['id', 'company_id', 'amount', 'status', 'created_at'])


# Se inicia la tranformacion de los datos en el formato del esquema

# Ajustar longitudes de strings al esquema
df['id'] = df['id'].astype(str).str[:24]
df['company_id'] = df['company_id'].astype(str).str[:24]

# Como company_name tiene valores nulos y en el esquema se aceptan, los transformamos a none
df['company_name'] = df['company_name'].where(df['company_name'].notna(), None)

# Despues los transformamos a string con una longitud maxima de 130
df['company_name'] = df['company_name'].astype(str).str[:130] 

# Como los datos nulos se transforron a none y luego estos en cadena 'None', remplazamos los None por tipo None para que posgrest los guarde como nulo
df['company_name'] = df['company_name'].replace('None', None)

# Ajustar longitudes de strings al esquema
df['status'] = df['status'].astype(str).str[:30]


# Convertir 'amount' a decimal
# Existen valores que superan los 16 digitos permitidos por el esquema
max_amount = 99999999999999.99  # límite de DECIMAL(16,2)
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')  # convierte strings a números
df = df[df['amount'] <= max_amount]  # elimina filas con valores demasiado grandes
# df['amount'] = pd.to_numeric(df['amount'].round(2))


# Convertir fechas
df['paid_at'] = pd.to_datetime(df['paid_at'], errors='coerce')  # Asigna NaT donde falla
df['paid_at'] = df['paid_at'].astype(object)                     # cambia a object
df['paid_at'] = df['paid_at'].where(pd.notna(df['paid_at']), None)  # reemplaza NaT por None


# Creamos una función para convertirlos las fechas que tienen otro formato al de la mayoría

def parse_fecha(x):
    try:
        # Principal: dd/mm/yyyy
        return pd.to_datetime(x)
    except:
        # Formatos específicos sin dayfirst
        for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y%m%d"):
            try:
                return pd.to_datetime(x, format=fmt)
            except:
                continue
        return pd.NaT

df['created_at'] = df['created_at'].apply(parse_fecha)


# Se guardan en csv los datos_transformados que cumplen con el esquema dado en las instrucciones de la prueba
df.to_csv('transformed_data.csv')


# Se crea la tabla conforme al esquema y se confirma que los datos se puedan cargar
conn = get_db_connection()

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS transformed_data (
    id VARCHAR(24) NOT NULL,
    company_name VARCHAR(130) NULL,
    company_id VARCHAR(24) NOT NULL,
    amount DECIMAL(16,2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    paid_at TIMESTAMP NULL
)
""")
conn.commit()
print("✅ Tabla 'transformed_data' creada")

for row in df.itertuples(index=False):
    cur.execute("""
        INSERT INTO transformed_data (id, company_name, company_id, amount, status, created_at, paid_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """,  row)

conn.commit()
cur.close()
conn.close()
print("✅ CSV cargado en la tabla 'transformed_dta'")
