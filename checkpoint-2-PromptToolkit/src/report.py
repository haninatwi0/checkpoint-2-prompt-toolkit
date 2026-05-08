"""
report.py — Relatório Comparativo com Tabelas e Gráficos
Referência: Aula 07 (temperatura) + Aula 09 (avaliação)

Gera: tabela CSV, gráficos de acurácia/custo/temperatura, recomendação.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os


OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
GRAFICOS_DIR = os.path.join(OUTPUT_DIR, "graficos")


def _garantir_dirs():
    os.makedirs(GRAFICOS_DIR, exist_ok=True)


def gerar_tabela(resultados: list[dict]) -> pd.DataFrame:
    """
    Gera DataFrame com todos os resultados e salva como CSV.

    Cada resultado deve ter: tarefa, tecnica, input, resposta,
    acuracia, tokens_prompt, tokens_resposta, tempo_ms
    """
    _garantir_dirs()
    df = pd.DataFrame(resultados)
    csv_path = os.path.join(OUTPUT_DIR, "resultados.csv")
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"📊 Tabela salva em: {csv_path}")
    return df


def grafico_acuracia(df: pd.DataFrame):
    """Gráfico de barras: acurácia média por técnica para cada tarefa."""
    _garantir_dirs()

    pivot = df.pivot_table(
        index="tarefa", columns="tecnica", values="acuracia", aggfunc="mean"
    )

    ax = pivot.plot(kind="bar", figsize=(12, 6), width=0.75, edgecolor="white")
    ax.set_title("Acurácia por Técnica × Tarefa", fontsize=16, fontweight="bold", pad=20)
    ax.set_xlabel("Tarefa", fontsize=12)
    ax.set_ylabel("Acurácia Média", fontsize=12)
    ax.set_ylim(0, 1.1)
    ax.legend(title="Técnica", fontsize=10)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=15, ha="right")
    plt.tight_layout()

    path = os.path.join(GRAFICOS_DIR, "acuracia_por_tecnica.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"📈 Gráfico salvo: {path}")


def grafico_custo(df: pd.DataFrame):
    """Gráfico de barras: tokens médios por técnica."""
    _garantir_dirs()

    custo = df.groupby("tecnica")[["tokens_prompt", "tokens_resposta"]].mean()

    ax = custo.plot(kind="bar", stacked=True, figsize=(10, 6), edgecolor="white",
                    color=["#ED145B", "#3D9CCC"])
    ax.set_title("Custo Médio (Tokens) por Técnica", fontsize=16, fontweight="bold", pad=20)
    ax.set_xlabel("Técnica", fontsize=12)
    ax.set_ylabel("Tokens Médios", fontsize=12)
    ax.legend(["Tokens Prompt", "Tokens Resposta"], fontsize=10)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=15, ha="right")
    plt.tight_layout()

    path = os.path.join(GRAFICOS_DIR, "custo_por_tecnica.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"📈 Gráfico salvo: {path}")


def grafico_temperatura(resultados_temp: dict):
    """Gráfico de barras: consistência por temperatura."""
    _garantir_dirs()

    temps = list(resultados_temp.keys())
    consist = [resultados_temp[t]["consistencia"] for t in temps]
    cores = ["#29AF8C", "#D58C2E", "#C9492C"]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar([str(t) for t in temps], consist, color=cores[:len(temps)],
                  edgecolor="white", linewidth=0.5)

    for bar, val in zip(bars, consist):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                f"{val:.0f}%", ha="center", fontweight="bold", fontsize=13)

    ax.set_title("Consistência por Temperatura", fontsize=16, fontweight="bold", pad=20)
    ax.set_xlabel("Temperatura", fontsize=12)
    ax.set_ylabel("Consistência (%)", fontsize=12)
    ax.set_ylim(0, 115)
    plt.tight_layout()

    path = os.path.join(GRAFICOS_DIR, "temperatura_consistencia.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"📈 Gráfico salvo: {path}")


def recomendar(df: pd.DataFrame) -> dict:
    """
    Para cada tarefa, recomenda a melhor técnica.
    Critério: maior acurácia; em empate, menor custo (tokens).
    """
    recomendacoes = {}

    for tarefa in df["tarefa"].unique():
        sub = df[df["tarefa"] == tarefa]
        resumo = sub.groupby("tecnica").agg(
            acuracia_media=("acuracia", "mean"),
            tokens_medio=("tokens_prompt", "mean"),
        ).sort_values(["acuracia_media", "tokens_medio"], ascending=[False, True])

        melhor = resumo.index[0]
        acc = resumo.loc[melhor, "acuracia_media"]
        tok = resumo.loc[melhor, "tokens_medio"]

        recomendacoes[tarefa] = {
            "melhor_tecnica": melhor,
            "acuracia": round(acc, 2),
            "tokens_medio": round(tok),
            "justificativa": (
                f"'{melhor}' teve a maior acurácia ({acc:.0%}) "
                f"com custo médio de {tok:.0f} tokens."
            ),
        }

    return recomendacoes


def imprimir_relatorio(df: pd.DataFrame, recomendacoes: dict, resultados_temp: dict):
    """Imprime relatório completo no terminal."""
    print("\n" + "=" * 70)
    print("📊 RELATÓRIO DO PROMPT TOOLKIT")
    print("=" * 70)

    # Tabela resumida
    resumo = df.groupby(["tarefa", "tecnica"]).agg(
        acuracia=("acuracia", "mean"),
        tokens=("tokens_prompt", "mean"),
    ).round(2)
    print("\n📋 Resumo por Tarefa × Técnica:")
    print(resumo.to_string())

    # Recomendações
    print("\n\n🏆 RECOMENDAÇÕES:")
    print("-" * 50)
    for tarefa, rec in recomendacoes.items():
        print(f"  {tarefa}: → {rec['justificativa']}")

    # Temperatura
    print("\n\n🌡️  TESTE DE TEMPERATURA:")
    print("-" * 50)
    for temp, dados in resultados_temp.items():
        print(f"  Temp {temp}: {dados['consistencia']:.0f}% consistência")

    print("\n" + "=" * 70)
    print("📁 Arquivos gerados em output/")
    print("=" * 70)
