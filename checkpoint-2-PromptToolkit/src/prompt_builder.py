"""
prompt_builder.py — Construtor de Prompts por Anatomia
Referência: Aula 05 — Anatomia de um Prompt

Funções para montar prompts seguindo a estrutura:
Instrução + Contexto + Input + Formato de Output
"""


def montar_prompt(
    instrucao: str,
    contexto: str = "",
    input_dados: str = "",
    formato_output: str = "",
) -> str:
    """
    Monta um prompt seguindo a anatomia da Aula 05.

    Args:
        instrucao: O que o modelo deve fazer (obrigatório)
        contexto: Informação de domínio/background
        input_dados: Os dados a serem processados
        formato_output: Como a resposta deve ser formatada

    Returns:
        String do prompt montado
    """
    if not instrucao.strip():
        raise ValueError("Instrução não pode estar vazia!")

    partes = [instrucao.strip()]

    if contexto.strip():
        partes.append(f"\nContexto: {contexto.strip()}")

    if input_dados.strip():
        partes.append(f"\nInput: {input_dados.strip()}")

    if formato_output.strip():
        partes.append(f"\nFormato de resposta: {formato_output.strip()}")

    return "\n".join(partes)


def adicionar_exemplos(prompt: str, exemplos: list[dict]) -> str:
    """
    Adiciona exemplos few-shot ao prompt.

    Args:
        prompt: Prompt base
        exemplos: Lista de dicts com 'input' e 'output'

    Returns:
        Prompt com exemplos adicionados
    """
    bloco_exemplos = "\n\nExemplos:"
    for ex in exemplos:
        bloco_exemplos += f'\nInput: "{ex["input"]}" → Output: "{ex["output"]}"'

    # Inserir exemplos antes do input real (se houver "Input:" no prompt)
    if "\nInput:" in prompt:
        pos = prompt.rfind("\nInput:")
        return prompt[:pos] + bloco_exemplos + prompt[pos:]
    else:
        return prompt + bloco_exemplos


def adicionar_cot(prompt: str, passos: list[str]) -> str:
    """
    Adiciona instrução de Chain-of-Thought ao prompt.

    Args:
        prompt: Prompt base
        passos: Lista de passos de raciocínio

    Returns:
        Prompt com CoT adicionado
    """
    bloco_cot = "\n\nAnalise passo a passo:"
    for i, passo in enumerate(passos, 1):
        bloco_cot += f"\n{i}. {passo}"
    bloco_cot += "\n\nApós a análise, forneça sua resposta final."

    # Inserir antes do formato de output (se houver)
    if "\nFormato de resposta:" in prompt:
        pos = prompt.rfind("\nFormato de resposta:")
        return prompt[:pos] + bloco_cot + prompt[pos:]
    else:
        return prompt + bloco_cot
