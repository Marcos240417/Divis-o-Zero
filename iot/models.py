# iot/models.py
from django.db import models
from django.conf import settings

# Escolhas mais específicas para o tipo de hardware
DEVICE_TYPE_CHOICES = [
    ('sensor_temp', 'Sensor de Temperatura'),
    ('atuador_rele', 'Atuador - Relé'),
    ('sensor_umidade', 'Sensor de Umidade'),
]

class Store(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stores') # [cite: 915]
    name = models.CharField(max_length=100) # [cite: 915]
    cep = models.CharField(max_length=9)
    # ...

class Device(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='devices') # [cite: 915]
    device_id = models.CharField(max_length=50, unique=True) # ID Único para MQTT [cite: 915]
    name = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=DEVICE_TYPE_CHOICES, default='sensor_temp') # Detalhado
    ativo = models.BooleanField(default=True) # [cite: 915]

class SensorReading(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='leituras') # [cite: 915]
    tipo_sensor = models.CharField(max_length=50) # Ex: 'temperatura' [cite: 915]
    valor = models.FloatField() # [cite: 915]
    unidade_medida = models.CharField(max_length=10, default='C') # NOVO: Essencial para relatórios
    timestamp = models.DateTimeField(auto_now_add=True) # [cite: 915]

class RegraAutomacao(models.Model):
    # ... (campos existentes) [cite: 916]
    limite_min = models.FloatField()
    limite_max = models.FloatField()
    acao = models.CharField(max_length=20, choices=[('ligar','Ligar'),('desligar','Desligar')]) # [cite: 916]
    # Restringe a escolha apenas para atuadores do tipo Relé
    atuador = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='regras', limit_choices_to={'tipo': 'atuador_rele'}) 
    habilitada = models.BooleanField(default=True) # [cite: 916]
    delay_minutos = models.IntegerField(default=5) # NOVO: Histerese para estabilidade