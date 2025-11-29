# api_fastapi/database.py
import mysql.connector
from mysql.connector import pooling

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "braulio", 
    "database": " paquexpress" 
}

# Usaremos un Pool de Conexiones para manejar las conexiones de manera eficiente
try:
    db_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="paquexpress_pool",
        pool_size=5, # Número máximo de conexiones
        **DB_CONFIG
    )
    print("Pool de conexiones a MySQL creado exitosamente.")

except mysql.connector.Error as err:
    print(f"Error al conectar a MySQL: {err}")
    db_pool = None

# Función generadora para obtener y liberar la conexión
def get_db():
    """Obtiene una conexión del pool y la libera al finalizar."""
    if db_pool is None:
        raise Exception("No se pudo establecer el pool de la base de datos.")
        
    conn = None
    try:
        # Obtener una conexión del pool
        conn = db_pool.get_connection()
        # El 'yield' hace que el código después del 'finally' se ejecute cuando la función que llama termina
        yield conn 
    except Exception as e:
        print(f"Error en la transacción de base de datos: {e}")
        # Puedes relanzar la excepción para que FastAPI la maneje
        raise 
    finally:
        # Devolver la conexión al pool
        if conn:
            conn.close()