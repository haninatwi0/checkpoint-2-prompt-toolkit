"""
main.py — Prompt Toolkit: Ponto de Entrada
Checkpoint 02 · FIAP · Ciência da Computação 2026
Prof. Jorge Luiz Gomes

Domínio: E-commerce (TechStore Brasil)
Stack: Python 3.10+ · Ollama (gpt-oss:120b) · tiktoken · matplotlib · pandas

Execução:
    python main.py           # Roda tudo (análise completa)
    python main.py --help    # Mostra ajuda
"""

import json
import time
import sys

from src.llm_client import LLMClient
from src.techniques import TECNICAS
from src.tasks import TAREFAS, DOMINIO, EMPRESA, DESCRICAO
from src.evaluator import contar_tokens, medir_acuracia, testar_temperatura
from src.report import (
    gerar_tabela,
    grafico_acuracia,
    grafico_custo,
    grafico_temperatura,
    recomendar,
    imprimir_relatorio,
)


def carregar_inputs() -> dict:
    """Carrega inputs de teste de data/inputs.json."""
    with open("data/inputs.json", "r", encoding="utf-8") as f:
        return json.load(f)


def carregar_personas() -> dict:
    """Carrega personas de prompts/system_prompts.json."""
    with open("prompts/system_prompts.json", "r", encoding="utf-8") as f:
        return json.load(f)


def executar_toolkit():
    """Executa o Prompt Toolkit completo."""

    print("=" * 70)
    print("🧰 PROMPT TOOLKIT — Checkpoint 02")
    print(f"🏢 Domínio: {DOMINIO}")
    print(f"🤖 Stack: Ollama + gpt-oss:120b")
    print("=" * 70)

    # ── 1. Inicializar ──
    client = LLMClient()

    if not client.health_check():
        print("\n❌ Ollama não está rodando!")
        print("   Execute: ollama serve")
        print("   E depois: ollama pull gpt-oss:120b")
        sys.exit(1)

    print("✅ Ollama conectado!")

    inputs = carregar_inputs()
    personas = carregar_personas()
    resultados = []

    # ── 2. Para cada TAREFA × TÉCNICA × INPUT ──
    for tarefa in TAREFAS:
        nome_tarefa = tarefa["nome"]
        inputs_tarefa = inputs.get(nome_tarefa, [])

        print(f"\n{'─' * 60}")
        print(f"📋 Tarefa: {nome_tarefa} ({tarefa['tipo']})")
        print(f"   Inputs: {len(inputs_tarefa)} textos de teste")
        print(f"{'─' * 60}")

        for tecnica_key, tecnica_info in TECNICAS.items():
            nome_tecnica = tecnica_info["nome"]
            func = tecnica_info["funcao"]

            print(f"\n  🔧 Técnica: {nome_tecnica}")

            for i, item in enumerate(inputs_tarefa):
                input_texto = item["input"]
                esperado = item["esperado"]

                # Montar prompt com a técnica
                if tecnica_info["usa_persona"]:
                    prompt, system_prompt = func(tarefa, input_texto, personas)
                else:
                    prompt, system_prompt = func(tarefa, input_texto)

                # Chamar LLM
                resultado_llm = client.chat(
                    prompt,
                    system_prompt=system_prompt,
                    temperature=0.1 if tarefa["tipo"] != "geracao" else 0.7,
                )

                # Medir qualidade
                acuracia = medir_acuracia(resultado_llm["resposta"], esperado)

                # Contar tokens (via tiktoken como fallback se Ollama não retornar)
                tok_prompt = resultado_llm["tokens_prompt"] or contar_tokens(prompt)
                tok_resp = resultado_llm["tokens_resposta"] or contar_tokens(resultado_llm["resposta"])

                # Registrar
                resultados.append({
                    "tarefa": nome_tarefa,
                    "tecnica": nome_tecnica,
                    "input_resumo": input_texto[:50],
                    "resposta_resumo": resultado_llm["resposta"][:80],
                    "acuracia": acuracia,
                    "tokens_prompt": tok_prompt,
                    "tokens_resposta": tok_resp,
                    "tempo_ms": resultado_llm["tempo_ms"],
                })

                status = "✅" if acuracia >= 0.5 else "❌"
                print(f"    [{i+1}] {status} acc={acuracia:.0%} | {tok_prompt}+{tok_resp} tok | {resultado_llm['tempo_ms']}ms")

                time.sleep(1)  # Evitar sobrecarga

    # ── 3. Gerar relatório ──
    print(f"\n{'=' * 70}")
    print("📊 GERANDO RELATÓRIO...")
    print(f"{'=' * 70}")

    df = gerar_tabela(resultados)
    grafico_acuracia(df)
    grafico_custo(df)

    recomendacoes = recomendar(df)

    # ── 4. Teste de temperatura ──
    print("\n🌡️  Testando temperatura com o melhor prompt...")

    # Usar primeiro input da primeira tarefa
    tarefa_teste = TAREFAS[0]
    input_teste = inputs[tarefa_teste["nome"]][0]["input"]
    prompt_teste, _ = TECNICAS["few_shot"]["funcao"](tarefa_teste, input_teste)

    resultados_temp = testar_temperatura(
        client, prompt_teste, temperaturas=[0.1, 0.5, 1.0], repeticoes=3
    )
    grafico_temperatura(resultados_temp)

    # ── 5. Relatório final ──
    imprimir_relatorio(df, recomendacoes, resultados_temp)

    print("\n✅ Prompt Toolkit finalizado!")
    print(f"   Resultados em: output/resultados.csv")
    print(f"   Gráficos em: output/graficos/")


if __name__ == "__main__":
    executar_toolkit()
