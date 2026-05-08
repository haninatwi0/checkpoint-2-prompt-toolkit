"""
techniques.py — 4 Técnicas de Prompt Engineering
Referência: Aula 06 (Zero-Shot, Few-Shot, CoT) + Aula 07 (Role Prompting)

Cada função recebe uma tarefa e retorna o prompt montado + system prompt (se aplicável).
"""

from src.prompt_builder import montar_prompt, adicionar_exemplos, adicionar_cot


def zero_shot(tarefa: dict, input_texto: str) -> tuple:
    """
    Técnica Zero-Shot — Prompt direto sem exemplos.
    Ref: Aula 06

    Returns:
        (prompt, system_prompt) — system_prompt é None
    """
    prompt = montar_prompt(
        instrucao=tarefa["instrucao"],
        contexto=f"Domínio: {tarefa.get('dominio', '')}",
        input_dados=input_texto,
        formato_output=tarefa["formato_output"],
    )
    return prompt, None


def few_shot(tarefa: dict, input_texto: str) -> tuple:
    """
    Técnica Few-Shot — Prompt com 2-3 exemplos.
    Ref: Aula 06

    Returns:
        (prompt, system_prompt) — system_prompt é None
    """
    prompt = montar_prompt(
        instrucao=tarefa["instrucao"],
        contexto=f"Domínio: {tarefa.get('dominio', '')}",
        input_dados=input_texto,
        formato_output=tarefa["formato_output"],
    )

    exemplos = tarefa.get("exemplos_fewshot", [])
    if exemplos:
        prompt = adicionar_exemplos(prompt, exemplos)

    return prompt, None


def chain_of_thought(tarefa: dict, input_texto: str) -> tuple:
    """
    Técnica Chain-of-Thought — Raciocínio passo a passo.
    Ref: Aula 06

    Returns:
        (prompt, system_prompt) — system_prompt é None
    """
    prompt = montar_prompt(
        instrucao=tarefa["instrucao"],
        contexto=f"Domínio: {tarefa.get('dominio', '')}",
        input_dados=input_texto,
        formato_output=tarefa["formato_output"],
    )

    passos = tarefa.get("passos_cot", [])
    if passos:
        prompt = adicionar_cot(prompt, passos)

    return prompt, None


def role_prompting(tarefa: dict, input_texto: str, personas: dict) -> tuple:
    """
    Técnica Role Prompting — Persona especialista via system prompt.
    Ref: Aula 07

    Returns:
        (prompt, system_prompt)
    """
    prompt = montar_prompt(
        instrucao=tarefa["instrucao"],
        contexto=f"Domínio: {tarefa.get('dominio', '')}",
        input_dados=input_texto,
        formato_output=tarefa["formato_output"],
    )

    # Buscar persona definida para esta tarefa
    persona_key = tarefa.get("persona", "default")
    system_prompt = personas.get(persona_key, {}).get("system_prompt", "")

    return prompt, system_prompt


# Mapeamento de técnicas para facilitar iteração
TECNICAS = {
    "zero_shot": {
        "nome": "Zero-Shot",
        "funcao": zero_shot,
        "usa_persona": False,
        "descricao": "Prompt direto, sem exemplos (Aula 06)",
    },
    "few_shot": {
        "nome": "Few-Shot",
        "funcao": few_shot,
        "usa_persona": False,
        "descricao": "Prompt com 2-3 exemplos incluídos (Aula 06)",
    },
    "cot": {
        "nome": "Chain-of-Thought",
        "funcao": chain_of_thought,
        "usa_persona": False,
        "descricao": "Raciocínio passo a passo explícito (Aula 06)",
    },
    "role": {
        "nome": "Role Prompting",
        "funcao": role_prompting,
        "usa_persona": True,
        "descricao": "Persona especialista via system prompt (Aula 07)",
    },
}
