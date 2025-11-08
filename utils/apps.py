from django.apps import AppConfig
import requests


def buscar_cep(cep: str):
    """Consulta o ViaCEP e retorna um dicionário formatado"""
    cep = cep.replace("-", "").strip()
    url = f"https://viacep.com.br/ws/{cep}/json/"
    resp = requests.get(url, timeout=5)
    data = resp.json()
    if data.get("erro"):
        return None
    return {
        "cep": data["cep"],
        "logradouro": data["logradouro"],
        "bairro": data["bairro"],
        "localidade": data["localidade"],
        "uf": data["uf"]
    }
