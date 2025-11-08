# utils/cep_utils.py
import requests


def buscar_cep(cep: str):
    """Consulta o ViaCEP e retorna um dicionário formatado."""
    cep = cep.replace("-", "").strip()  # Limpeza do CEP [cite: 912]
    url = f"https://viacep.com.br/ws/{cep}/json/"  # [cite: 912]

    try:
        resp = requests.get(url, timeout=5)  # Timeout para evitar travamento em falha de rede [cite: 912]
        resp.raise_for_status()  # Lança exceção para erros HTTP (4xx ou 5xx)
        data = resp.json()

        if data.get("erro"):
            return None  # Retorna None se o CEP for inválido [cite: 912]

        return {
            "cep": data["cep"],
            "logradouro": data["logradouro"],
            "bairro": data["bairro"],
            "localidade": data["localidade"],
            "uf": data["uf"]
        }
    except requests.exceptions.RequestException:
        # Captura erros de rede ou timeout
        return None