"""
llm_client.py — Conexão com Ollama API
Referência: Aula 05 — Ambiente Python para IA

Classe LLMClient que encapsula chamadas ao Ollama via REST API.
Modelo padrão: gpt-oss:120b
"""

import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    """Cliente para o Ollama REST API."""

    def __init__(self):
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "gpt-oss:120b")
        self.endpoint = f"{self.host}/api/chat"

    def chat(
        self,
        prompt: str,
        system_prompt: str = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> dict:
        """
        Envia prompt ao LLM via Ollama e retorna resposta + metadados.

        Args:
            prompt: Texto do usuário
            system_prompt: Instrução de sistema (persona, regras)
            temperature: Controla criatividade (0.0=determinístico, 1.5=criativo)
            max_tokens: Máximo de tokens na resposta

        Returns:
            dict com: resposta, tokens_prompt, tokens_resposta, tempo_ms
        """
        # Montar mensagens no formato Ollama
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }

        # Enviar requisição com retry
        inicio = time.time()
        for tentativa in range(3):
            try:
                resp = requests.post(self.endpoint, json=payload, timeout=120)
                resp.raise_for_status()
                data = resp.json()

                tempo_ms = round((time.time() - inicio) * 1000)

                return {
                    "resposta": data.get("message", {}).get("content", "").strip(),
                    "tokens_prompt": data.get("prompt_eval_count", 0),
                    "tokens_resposta": data.get("eval_count", 0),
                    "tempo_ms": tempo_ms,
                    "modelo": self.model,
                }

            except requests.exceptions.ConnectionError:
                print(f"  ⚠️  Tentativa {tentativa + 1}/3 — Ollama não respondeu. Verifique se está rodando.")
                time.sleep(2)
            except requests.exceptions.Timeout:
                print(f"  ⚠️  Tentativa {tentativa + 1}/3 — Timeout.")
                time.sleep(2)
            except Exception as e:
                print(f"  ❌ Erro: {e}")
                break

        return {
            "resposta": "[ERRO] Não foi possível obter resposta do Ollama.",
            "tokens_prompt": 0,
            "tokens_resposta": 0,
            "tempo_ms": 0,
            "modelo": self.model,
        }

    def health_check(self) -> bool:
        """Verifica se o Ollama está rodando."""
        try:
            r = requests.get(f"{self.host}/api/tags", timeout=5)
            return r.status_code == 200
        except:
            return False
