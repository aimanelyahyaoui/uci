import time
import json
import random
from datetime import datetime, timezone
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

ritmo_cardiaco = 75
while True:
    ritmo_cardiaco += random.choice([-1, 0, 1])
    ritmo_cardiaco = max(60, min(140, ritmo_cardiaco))
    datos_paciente = {
        "paciente_id": "CAMA-001",
        "ritmo_cardiaco": ritmo_cardiaco,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    producer.send('sensores_uci', value=datos_paciente)
    print(f"Enviado a Kafka: {datos_paciente}")

    time.sleep(2)