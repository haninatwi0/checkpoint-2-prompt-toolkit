# 🧰 Prompt Toolkit — Checkpoint 02

**Disciplina:** Prompt Engineering and Artificial Intelligence  
**Instituição:** FIAP — Ciência da Computação 2026  
**Professor:** Jorge Luiz Gomes  
**Módulo:** 2 — Prompt Engineering Básico (Aulas 05 a 08)  
**Grupo:** [GABARITO DO PROFESSOR]  
**Domínio:** E-commerce (TechStore Brasil)

---

## 📋 Sobre o Projeto

O **Prompt Toolkit** é uma ferramenta Python que aplica automaticamente 4 técnicas de Prompt Engineering a tarefas de negócio, compara resultados e recomenda a melhor abordagem.

### Problema Resolvido

A TechStore Brasil recebe centenas de reviews e reclamações diariamente. Hoje, a análise é manual. Este toolkit automatiza a escolha da melhor técnica de prompting para cada tipo de tarefa (classificação, extração, geração).

---

## 🏗️ Arquitetura

```
inputs.json → prompt_builder → techniques (ZS/FS/CoT/Role) → llm_client (Ollama) → evaluator → report → output/
```

```
prompt-toolkit/
├── main.py                    # Ponto de entrada
├── requirements.txt           # Dependências
├── .env.example               # Variáveis de ambiente
├── src/
│   ├── llm_client.py          # Conexão Ollama API (Aula 05)
│   ├── prompt_builder.py      # Montar prompts por anatomia (Aula 05)
│   ├── techniques.py          # 4 técnicas: ZS, FS, CoT, Role (Aulas 06+07)
│   ├── tasks.py               # 3 tarefas do domínio (Aula 08)
│   ├── evaluator.py           # Métricas + temperatura
│   └── report.py              # Tabelas pandas + gráficos matplotlib
├── data/
│   └── inputs.json            # 5 inputs reais por tarefa
├── prompts/
│   └── system_prompts.json    # 2 personas detalhadas
├── output/
│   ├── resultados.csv         # Resultados da execução
│   └── graficos/              # PNGs dos gráficos
└── docs/
    └── CP02_Gabarito.pdf      # Documentação
```

---

## ⚙️ Stack Técnica

| Tecnologia | Uso | Versão |
|---|---|---|
| Python | Linguagem | 3.10+ |
| Ollama | LLM local | gpt-oss:120b |
| requests | Chamadas REST API | 2.31+ |
| tiktoken | Contagem de tokens | 0.7+ |
| pandas | Tabelas e análise | 2.1+ |
| matplotlib | Gráficos | 3.8+ |
| python-dotenv | Variáveis de ambiente | 1.0+ |

---

## 🚀 Como Executar

### 1. Pré-requisitos

- Python 3.10+
- Ollama instalado e rodando com o modelo `gpt-oss:120b`

```bash
# Instalar Ollama: https://ollama.com
ollama pull gpt-oss:120b
ollama serve
```

### 2. Instalar dependências

```bash
cd prompt-toolkit
pip install -r requirements.txt
```

### 3. Configurar ambiente

```bash
cp .env.example .env
# Editar .env se o Ollama não estiver em localhost:11434
```

### 4. Executar

```bash
python main.py
```

### 5. Resultados

- `output/resultados.csv` — Tabela completa
- `output/graficos/acuracia_por_tecnica.png` — Gráfico de acurácia
- `output/graficos/custo_por_tecnica.png` — Gráfico de custo (tokens)
- `output/graficos/temperatura_consistencia.png` — Gráfico de temperatura

---

## 📊 Técnicas Implementadas

| Técnica | Aula | Descrição |
|---|---|---|
| **Zero-Shot** | 06 | Prompt direto sem exemplos |
| **Few-Shot** | 06 | Prompt com 2-3 exemplos do domínio |
| **Chain-of-Thought** | 06 | Raciocínio passo a passo explícito |
| **Role Prompting** | 07 | Persona especialista via system prompt |

## 📋 Tarefas do Domínio (Aula 08)

| Tarefa | Tipo | Descrição |
|---|---|---|
| Classificação de Sentimento | classificação | Classificar reviews como POSITIVO/NEGATIVO/NEUTRO/MISTO |
| Extração de Reclamações | extração | Extrair produto, preço, defeito e urgência em JSON |
| Geração de Descrições | geração | Criar descrição de venda a partir de specs técnicas |

---

## 📚 Referências

- **Aula 05** — Anatomia de um Prompt (FIAP, 2026)
- **Aula 06** — Zero-Shot, Few-Shot e CoT (FIAP, 2026)
- **Aula 07** — Role Prompting e Parâmetros (FIAP, 2026)
- **Aula 08** — Prompts para Tarefas Específicas (FIAP, 2026)
- Brown et al., "Language Models are Few-Shot Learners" (2020)
- Wei et al., "Chain-of-Thought Prompting" (2022)
- OpenAI Prompt Engineering Guide
- Anthropic Claude Prompt Guide
- promptingguide.ai/pt
