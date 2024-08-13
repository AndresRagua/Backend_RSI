import psycopg2

try:
    conn = psycopg2.connect(
        dbname="rsi",
        user="postgres",
        password="123456",
        host="localhost",
        port="5432"
    )
    print("Conexión exitosa")
    conn.close()
except Exception as e:
    print(f"Error al conectar: {e}")
