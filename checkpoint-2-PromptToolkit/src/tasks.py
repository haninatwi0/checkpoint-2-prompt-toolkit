"""
tasks.py — Tarefas do Domínio: E-commerce (TechStore Brasil)
Referência: Aula 08 — Prompts para Tarefas Específicas

Cada tarefa define: instrução, formato de output, exemplos few-shot,
passos CoT e persona associada.

Domínio escolhido: E-commerce (loja de eletrônicos)
"""

DOMINIO = "E-commerce — TechStore Brasil"
EMPRESA = "TechStore Brasil"
DESCRICAO = (
    "A TechStore Brasil é uma loja online de eletrônicos que recebe "
    "centenas de reviews e reclamações diariamente. O Prompt Toolkit "
    "ajuda a equipe a encontrar a melhor técnica de prompting para "
    "cada tipo de tarefa de processamento de texto."
)

TAREFAS = [
    # ─── TAREFA 1: Classificação de Sentimento ───
    {
        "nome": "classificacao_sentimento",
        "tipo": "classificacao",
        "dominio": DOMINIO,
        "instrucao": (
            "Classifique a seguinte review de produto como "
            "POSITIVO, NEGATIVO, NEUTRO ou MISTO."
        ),
        "formato_output": "Responda APENAS com a classificação (uma palavra).",
        "exemplos_fewshot": [
            {"input": "Adorei o produto, chegou rápido e funciona perfeitamente!", "output": "POSITIVO"},
            {"input": "Péssimo, veio com defeito e o suporte não resolveu.", "output": "NEGATIVO"},
            {"input": "Bom preço, mas a embalagem veio amassada.", "output": "MISTO"},
        ],
        "passos_cot": [
            "Identifique todos os aspectos POSITIVOS mencionados na review",
            "Identifique todos os aspectos NEGATIVOS mencionados",
            "Compare o peso dos aspectos positivos vs negativos",
            "Classifique como POSITIVO, NEGATIVO, NEUTRO ou MISTO",
        ],
        "persona": "analista_cx",
    },
    # ─── TAREFA 2: Extração de Dados de Reclamações ───
    {
        "nome": "extracao_reclamacao",
        "tipo": "extracao",
        "dominio": DOMINIO,
        "instrucao": (
            "Extraia as seguintes informações da reclamação de um cliente: "
            "produto, preço (se mencionado), defeito reportado e urgência "
            "(alta/média/baixa)."
        ),
        "formato_output": (
            'Responda APENAS em JSON: '
            '{"produto": "", "preco": "", "defeito": "", "urgencia": ""}'
        ),
        "exemplos_fewshot": [
            {
                "input": "O Monitor LG 27 polegadas de R$1.300 veio com mancha no canto. Preciso de troca urgente!",
                "output": '{"produto": "Monitor LG 27pol", "preco": "R$1.300", "defeito": "mancha no canto", "urgencia": "alta"}',
            },
            {
                "input": "Teclado Logitech de R$250, tecla Enter trava às vezes. Não é urgente.",
                "output": '{"produto": "Teclado Logitech", "preco": "R$250", "defeito": "tecla Enter trava", "urgencia": "baixa"}',
            },
        ],
        "passos_cot": [
            "Identifique o PRODUTO mencionado (marca + modelo se disponível)",
            "Encontre o PREÇO em reais (se mencionado, senão 'não informado')",
            "Descreva o DEFEITO ou problema reportado",
            "Avalie a URGÊNCIA com base no tom e impacto (alta/média/baixa)",
            "Monte o JSON com os 4 campos",
        ],
        "persona": "analista_cx",
    },
    # ─── TAREFA 3: Geração de Descrição de Produto ───
    {
        "nome": "geracao_descricao",
        "tipo": "geracao",
        "dominio": DOMINIO,
        "instrucao": (
            "Crie uma descrição atrativa de produto para a página de venda "
            "da TechStore Brasil com base nas especificações técnicas fornecidas."
        ),
        "formato_output": (
            "Escreva no máximo 5 frases. Tom: profissional e persuasivo. "
            "Destaque os 2 principais diferenciais do produto."
        ),
        "exemplos_fewshot": [
            {
                "input": "Fone Bluetooth, 40h bateria, cancelamento de ruído, 250g, R$399",
                "output": (
                    "Mergulhe no som perfeito com o Fone BT Pro! Com impressionantes "
                    "40 horas de bateria e cancelamento de ruído ativo, sua música "
                    "favorita ganha vida. Leve e confortável (250g), é o companheiro "
                    "ideal para o dia a dia. Tecnologia premium por apenas R$399."
                ),
            },
        ],
        "passos_cot": [
            "Identifique os 3 principais diferenciais competitivos do produto",
            "Defina o público-alvo ideal (gamer, profissional, estudante?)",
            "Escolha um tom de voz adequado (premium, jovem, técnico?)",
            "Escreva a descrição em 4-5 frases destacando os diferenciais",
        ],
        "persona": "copywriter",
    },
]
