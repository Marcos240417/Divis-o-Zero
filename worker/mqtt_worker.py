# worker/mqtt_worker.py
import paho.mqtt.client as mqtt
import requests, json
from requests.exceptions import RequestException

BROKER = "192.168.1.50"  # [cite: 921]
TOPIC = "flori/sensor/#"  # [cite: 921]
DJANGO_API = "http://127.0.0.1:8000/api/iot/registrar-leitura/"  # [cite: 921]


def on_connect(client, userdata, flags, rc):
    print("Conectado ao broker:", rc)  # [cite: 921]
    client.subscribe(TOPIC)  # [cite: 921]


def on_message(client, userdata, msg):
    """Recebe o payload do ESP32 e o envia via POST para o Django."""
    try:
        payload = json.loads(msg.payload.decode())
        print("Leitura recebida:", payload)

        # Envio HTTP com tratamento de falhas e timeout
        r = requests.post(DJANGO_API, json=payload, timeout=10)
        r.raise_for_status()  # Lança exceção para status codes 4xx/5xx

        print(f"Sucesso, status Django: {r.status_code}")

    except json.JSONDecodeError:
        print("ERRO: Payload recebido não é um JSON válido.")
    except RequestException as e:
        # Captura erros de rede/conexão com o Django
        print(f"ERRO CRÍTICO: Falha ao enviar ao Django (possivelmente offline): {e}")
        print(f"ERRO CRÍTICO: Falha ao enviar ao Django (possivelmente offline): {e}")
    except Exception as e:
        print(f"ERRO INESPERADO: {e}")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, 1883)

print("Worker MQTT iniciado. Pronto para receber mensagens...")
client.loop_forever()  # [cite: 921]