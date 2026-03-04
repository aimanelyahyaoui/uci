import time
import json
import random
from datetime import datetime, timezone

ritmo_cardiaco = 75
while True:
    ritmo_cardiaco += random.choice([-1, 0, 1])
    ritmo_cardiaco = max(60, min(140, ritmo_cardiaco))
    datos_paciente = {
        "paciente_id": "CAMA-001",
        "ritmo_cardiaco": ritmo_cardiaco,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    mensaje_json = json.dumps(datos_paciente)

    print(mensaje_json)

    time.sleep(2)