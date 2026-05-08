"""
evaluator.py — Avaliação de Qualidade dos Prompts
Referência: Aula 07 (parâmetros/temperatura) + Aula 09 (métricas)

Funções para medir acurácia, consistência, tokens e testar temperatura.
"""

import tiktoken
import time


encoder = tiktoken.get_encoding("cl100k_base")


def contar_tokens(texto: str) -> int:
    """Conta tokens usando tiktoken (cl100k_base)."""
    return len(encoder.encode(texto))


def medir_acuracia(resposta: str, esperado) -> float:
    """
    Mede acurácia da resposta comparando com o esperado.
    - Se esperado é string: match exato (case-insensitive, strip)
    - Se esperado é dict: verifica se keywords estão na resposta
    """
    resposta_limpa = resposta.strip().upper()

    if isinstance(esperado, str):
        return 1.0 if esperado.strip().upper() in resposta_limpa else 0.0

    if isinstance(esperado, dict):
        # Para extração: verificar se valores-chave estão na resposta
        total = len(esperado)
        encontrados = 0
        for chave, valor in esperado.items():
            if str(valor).lower() in resposta.lower():
                encontrados += 1
        return encontrados / max(total, 1)

    return 0.0


def medir_consistencia(respostas: list[str]) -> float:
    """
    Mede consistência: mesma pergunta N vezes → respostas iguais?
    Retorna porcentagem de respostas iguais à mais frequente.
    """
    if not respostas:
        return 0.0

    normalizadas = [r.strip().upper()[:50] for r in respostas]
    mais_comum = max(set(normalizadas), key=normalizadas.count)
    iguais = normalizadas.count(mais_comum)

    return iguais / len(normalizadas) * 100


def testar_temperatura(llm_client, prompt: str, system_prompt: str = None,
                       temperaturas: list = None, repeticoes: int = 3) -> dict:
    """
    Testa o mesmo prompt com diferentes temperaturas.
    Ref: Aula 07 — Parâmetros

    Returns:
        dict: {temp: {"respostas": [...], "consistencia": float}}
    """
    if temperaturas is None:
        temperaturas = [0.1, 0.5, 1.0]

    resultados = {}

    for temp in temperaturas:
        respostas = []
        for _ in range(repeticoes):
            r = llm_client.chat(prompt, system_prompt=system_prompt, temperature=temp)
            respostas.append(r["resposta"])
            time.sleep(1)

        consistencia = medir_consistencia(respostas)
        resultados[temp] = {
            "respostas": respostas,
            "consistencia": consistencia,
        }

    return resultados
