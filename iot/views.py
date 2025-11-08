# iot/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction  # IMPORT CRÍTICO PARA SEGURANÇA
from .models import Device, SensorReading
import json


@csrf_exempt
@transaction.atomic  # Garante que a leitura só é salva se a transação for concluída
def registrar_leitura(request):
    """Recebe leitura via POST do Worker MQTT e inicia a automação"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            device_id = data.get('device_id')

            device = Device.objects.filter(device_id=device_id).first()
            if not device:
                return JsonResponse({'erro': f'Dispositivo {device_id} não encontrado'}, status=404)  # [cite: 918]

            SensorReading.objects.create(
                device=device,
                tipo_sensor=data.get('tipo_sensor'),
                valor=data.get('valor'),
                unidade_medida=data.get('unidade_medida', 'C')  # Usa a nova unidade
            )

            # Profissionalização: Aqui deve ser disparada a Celery Task para processar a Regra de Automação
            # Ex: processar_regras_automacao.delay(device_id) 

            return JsonResponse({'status': 'ok', 'message': 'Leitura registrada com sucesso'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'erro': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=500)

    return JsonResponse({'erro': 'Método inválido'}, status=405)  # [cite: 919]