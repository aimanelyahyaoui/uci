import json
import psycopg2 # <-- NUEVO: Librería de PostgreSQL
from kafka import KafkaConsumer

# 1. Conexión a la "caja" de la Base de Datos
conexion_db = psycopg2.connect(
    host="localhost",
    database="hospital_uci",
    user="admin",
    password="adminpassword",
    port="5432"
)
cursor = conexion_db.cursor()

# 2. Creamos la tabla (Igual que en SQLite)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS historial_constantes (
        id SERIAL PRIMARY KEY,
        paciente_id VARCHAR(50),
        ritmo_cardiaco INT,
        timestamp TIMESTAMP
    )
""")
conexion_db.commit()
print("🗄️  Base de datos conectada y tabla lista.")

# 3. Conexión a la "caja" de Kafka
consumer = KafkaConsumer(
    'sensores_uci',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("🩺 Monitor encendido. Escuchando a Kafka y guardando en PostgreSQL...")
print("-" * 60)

# 4. El bucle infinito: Leer de Kafka -> Guardar en DB
for mensaje in consumer:
    datos = mensaje.value
    
    paciente = datos['paciente_id']
    pulsaciones = datos['ritmo_cardiaco']
    hora = datos['timestamp']
    
    # <-- NUEVO: Insertamos el dato en la tabla
    cursor.execute(
        "INSERT INTO historial_constantes (paciente_id, ritmo_cardiaco, timestamp) VALUES (%s, %s, %s)",
        (paciente, pulsaciones, hora)
    )
    conexion_db.commit() # Guardamos los cambios definitivamente
    
    print(f"💾 Guardado en DB -> PACIENTE: {paciente} | PULSACIONES: {pulsaciones} bpm")