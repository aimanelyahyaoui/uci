import json
from kafka import KafkaConsumer

# 1. Nos conectamos a la "caja" de Kafka
consumer = KafkaConsumer(
    'sensores_uci', # El mismo canal (topic) donde escribe el generador
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest', # Solo queremos leer los datos nuevos que lleguen
    value_deserializer=lambda x: json.loads(x.decode('utf-8')) # Desempaquetamos el JSON
)

print("🩺 Monitor de la UCI encendido. Esperando constantes vitales...")
print("-" * 50)

# 2. Nos quedamos escuchando infinitamente
for mensaje in consumer:
    datos = mensaje.value
    
    paciente = datos['paciente_id']
    pulsaciones = datos['ritmo_cardiaco']
    hora = datos['timestamp']
    
    # Imprimimos de forma bonita lo que va llegando
    print(f"PACIENTE: {paciente} | PULSACIONES: {pulsaciones} bpm | HORA: {hora}")