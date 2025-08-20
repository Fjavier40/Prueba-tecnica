from conexion import get_db_connection


# Conexión a la base de datos
conn = get_db_connection()

cur = conn.cursor()

# Crear la vista
cur.execute("""
CREATE OR REPLACE VIEW daily_company_totals AS
SELECT
    c.company_name,
    ch.created_at::date AS transaction_date,
    SUM(ch.amount) AS total_amount
FROM
    charges ch
JOIN
    companies c ON ch.company_id = c.company_id
GROUP BY
    c.company_name,
    ch.created_at::date
ORDER BY
    c.company_name,
    transaction_date;
""")

conn.commit()
cur.close()
conn.close()

print("✅ Vista 'daily_company_totals' creada")

