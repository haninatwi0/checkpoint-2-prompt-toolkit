# 🧰 Prompt Toolkit — Checkpoint 02

**Disciplina:** Prompt Engineering and Artificial Intelligence  
**Instituição:** FIAP — Ciência da Computação 2026  
**Professor:** Jorge Luiz Gomes  
**Módulo:** 2 — Prompt Engineering Básico (Aulas 05 a 08)  
**Grupo:** Hanin Atwi 567626  
**Domínio:** E-commerce (TechStore Brasil)

---

## 1. Introdução

O objetivo principal é analisar e comparar diferentes técnicas de engenharia de prompts aplicadas a tarefas de Processamento de Linguagem Natural (NLP), utilizando um modelo de linguagem executado localmente por meio do Ollama.

O cenário utilizado é um e-commerce fictício chamado **TechStore Brasil**, especializado na venda de produtos de tecnologia.

---

## 2. Objetivo do Projeto

O projeto busca responder às seguintes perguntas:

- Qual técnica de prompting gera os melhores resultados?
- Qual técnica utiliza menos tokens?
- Qual técnica apresenta maior consistência em diferentes temperaturas?
- Qual é o melhor equilíbrio entre custo e desempenho?

Para isso, foram comparadas diferentes estratégias de prompting em três tarefas distintas.

---

## 3. Tarefas Avaliadas

### 3.1 Classificação de Sentimento

O modelo recebe avaliações de clientes e deve classificá-las como:

- Positivo
- Negativo
- Neutro

**Exemplo:**  
"Entrega rápida e produto excelente." → Positivo

---

### 3.2 Extração de Reclamações

O modelo deve identificar o principal problema mencionado pelo cliente.

**Exemplo:**  
"O notebook chegou com a tela quebrada." → Tela quebrada

---

### 3.3 Geração de Descrição de Produtos

O modelo recebe características de um produto e deve gerar uma descrição comercial atrativa.

**Exemplo:**  
"Mouse gamer RGB com 7 botões programáveis." → descrição de marketing.

---

## 4. Técnicas de Prompting Utilizadas

### Zero-Shot

O modelo recebe apenas a instrução da tarefa, sem exemplos.

### Few-Shot

O prompt inclui exemplos de entrada e saída.

### Chain-of-Thought (CoT)

O modelo é instruído a raciocinar passo a passo antes de responder.

### Role Prompting

O modelo assume um papel específico, como especialista em atendimento ao cliente ou marketing.

---

## 5. Tecnologias Utilizadas

- Python 3
- Ollama
- Modelo `qwen2.5:0.5b`
- Requests
- Pandas
- Matplotlib
- Tiktoken
- Python-dotenv

---

## 6. Estrutura do Projeto

```text
checkpoint-2-PromptToolkit/
├── data/                      # Dados de entrada para testes
├── prompts/                   # Templates de prompts
├── src/                       # Código-fonte do projeto
├── output/                    # Resultados gerados
│   └── graficos/
├── .env.example               # Exemplo de configuração
├── README.md                  # Documentação do projeto
├── main.py                    # Arquivo principal
└── requirements.txt           # Dependências Python
````

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
https://ollama.com
https://www.python.org
https://pandas.pydata.org
https://matplotlib.org
https://platform.openai.com/tokenizer