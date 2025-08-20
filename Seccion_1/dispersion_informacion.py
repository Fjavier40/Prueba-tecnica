import pandas as pd
from conexion import get_db_connection


# Conectar a PostgreSQL
conn = get_db_connection()
cur = conn.cursor()

# -------------------------------
# 1️⃣ Crear tablas
# -------------------------------

# Tabla de compañías
cur.execute("""
CREATE TABLE IF NOT EXISTS companies (
    company_id VARCHAR(24) PRIMARY KEY,
    company_name VARCHAR(130)
)
""")

# Tabla de transacciones
cur.execute("""
CREATE TABLE IF NOT EXISTS charges (
    charge_id VARCHAR(24) PRIMARY KEY,
    company_id VARCHAR(24) NOT NULL REFERENCES companies(company_id),
    amount DECIMAL(16,2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    paid_at TIMESTAMP NULL
)
""")

conn.commit()
print("✅ Tablas 'companies' y 'charges' creadas")

df=pd.read_csv('transformed_data.csv')
df['paid_at'] = df['paid_at'].where(pd.notna(df['paid_at']), None)


# 3️⃣ Insertar compañías
# -------------------------------
companies = df[['company_id', 'company_name']].drop_duplicates()
for row in companies.itertuples(index=False):
    cur.execute("""
        INSERT INTO companies (company_id, company_name)
        VALUES (%s, %s)
        ON CONFLICT (company_id) DO NOTHING
    """, row)

# -------------------------------
# 4️⃣ Insertar transacciones
# -------------------------------
for row in df.itertuples(index=False):
    cur.execute("""
        INSERT INTO charges (charge_id, company_id, amount, status, created_at, paid_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (row.id, row.company_id, row.amount, row.status, row.created_at, row.paid_at))

conn.commit()
cur.close()
conn.close()
print("✅ Datos cargados en 'companies' y 'charges'")