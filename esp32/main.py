# Compatibilidade: usa módulos do MicroPython quando disponíveis, senão fornece stubs para desenvolvimento/IDE.
try:
    import network
except ImportError:
    # Stub mínimo para CPython
    class _StubWLAN:
        def __init__(self, iface):
            self._connected = False

        def active(self, val=True):
            return None

        def connect(self, ssid, pwd):
            self._connected = True

        def isconnected(self):
            return self._connected

        def ifconfig(self):
            return ("127.0.0.1", "255.0.0.0", "0.0.0.0", "0.0.0.0")

    class _StubNetwork:
        STA_IF = 0

        @staticmethod
        def WLAN(iface):
            return _StubWLAN(iface)

import time

try:
    import ujson as json
except ImportError:
    import json

# Defina sempre sua própria classe MQTTClient para evitar conflitos de tipo
class MQTTClient:
    def __init__(self, client_id, server, port=0, user=None, password=None, keepalive=0, ssl=False, ssl_params={}):
        self._client_id = client_id
        self._server = server
        self._cb = None

    def set_callback(self, f):
        self._cb = f

    def connect(self):
        print("MQTTClient stub: connect() called")

    def subscribe(self, topic):
        print("MQTTClient stub: subscribe()", topic)

    def publish(self, topic, msg):
        print("MQTTClient stub: publish()", topic, msg)

    def check_msg(self):
        return None

class Pin:
    OUT = 0
    IN = 1
    PULL_UP = 2
    PULL_DOWN = 3
    OPEN_DRAIN = 4
    WAKE_LOW = 5
    WAKE_HIGH = 6

    def __init__(self, pin_no, mode=None, pull=None, value=None):
        self.pin_no = pin_no
        self._value = value if value is not None else 0
        self._mode = mode
        self._pull = pull

    from typing import Optional

    def value(self, v: Optional[int] = None) -> int:
        if v is None:
            return self._value
        self._value = v
        return self._value

def reset():
    print("Simulação de reset do dispositivo.")
    exit(0)

# --- CONFIGURAÇÕES ---
WIFI_SSID = "SUA_REDE_WIFI"
WIFI_PASS = "SUA_SENHA_WIFI"
BROKER = "192.168.1.50"
CLIENT_ID = "esp32_01"
TOPIC_SENSOR = b"flori/sensor/" + CLIENT_ID.encode()
TOPIC_CMD = b"flori/cmd/" + CLIENT_ID.encode()

# --- VARIÁVEIS GLOBAIS ---
relay = Pin(2, Pin.OUT)
relay.value(0)
client = MQTTClient(CLIENT_ID, BROKER)

# --- FUNÇÕES ---
def conecta_wifi():
    try:
        wlan = network.WLAN(network.STA_IF)
    except NameError:
        wlan = _StubNetwork.WLAN(_StubNetwork.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)
    max_wait = 20
    while max_wait > 0:
        if wlan.isconnected():
            print("Conectado! IP:", wlan.ifconfig()[0])
            return
        max_wait -= 1
        print("Aguardando conexão Wi-Fi...")
        time.sleep(1)

    print("Falha na conexão Wi-Fi. Reiniciando...")
    time.sleep(5)
    reset()

def comando(topic, msg):
    print(f"Comando recebido em {topic.decode()}")
    try:
        data = json.loads(msg.decode('utf-8'))
        acao = data.get("acao")

        if acao == "ligar":
            relay.value(1)
            print("Atuador: LIGADO.")
        elif acao == "desligar":
            relay.value(0)
            print("Atuador: DESLIGADO.")
        else:
            print("Comando desconhecido:", acao)

    except Exception as e:
        print(f"Erro ao processar comando JSON: {e}")

def main():
    conecta_wifi()

    try:
        client.set_callback(comando)
        client.connect()
        client.subscribe(TOPIC_CMD)
        print(f"MQTT conectado e ouvindo: {TOPIC_CMD.decode()}")
    except OSError as e:
        print(f"Falha ao conectar/subscrever MQTT: {e}")
        time.sleep(5)
        reset()

    counter = 0
    while True:
        client.check_msg()

        if counter % 10 == 0:
            valor_temp = 24.0 + (time.time() % 5) / 2
            leitura = {
                "device_id": CLIENT_ID,
                "tipo_sensor": "temperatura",
                "valor": round(valor_temp, 2),
                "unidade_medida": "C"
            }
            client.publish(TOPIC_SENSOR, json.dumps(leitura))
            print(f"Publicado: {leitura['valor']}°C")

        counter += 1
        time.sleep(1)

if __name__ == '__main__':
    main()
