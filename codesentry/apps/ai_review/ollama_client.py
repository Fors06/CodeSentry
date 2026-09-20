"""
Тонкая обёртка над локальным Ollama API (http://localhost:11434).
Никакого интернета — модель работает полностью офлайн после `ollama pull`.
"""

import requests

from core.config import get_settings
from core.logging_config import get_logger

logger = get_logger(__name__)


class OllamaClient:
    def __init__(self) -> None:
        settings = get_settings()
        self.host = settings.ollama_host
        self.model = settings.ollama_model
        self.embed_model = settings.ollama_embed_model

    def generate(self, prompt: str, system: str | None = None, timeout: int = 120) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        if system:
            payload["system"] = system

        try:
            response = requests.post(f"{self.host}/api/generate", json=payload, timeout=timeout)
            response.raise_for_status()
            return response.json().get("response", "")
        except requests.RequestException as exc:
            logger.error("Ошибка обращения к Ollama: %s", exc)
            return "[Ошибка: локальная модель недоступна. Проверьте, что `ollama serve` запущена.]"

    def chat_with_tools(
        self, messages: list[dict], tools: list[dict], timeout: int = 120
    ) -> dict:
        """
        Вызов /api/chat с поддержкой function calling (tools).
        Требует модель, поддерживающую tools (например, qwen2.5-coder, llama3.1+).
        Возвращает сырой ответ Ollama: {"message": {"content": ..., "tool_calls": [...]}}
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "tools": tools,
            "stream": False,
        }
        try:
            response = requests.post(f"{self.host}/api/chat", json=payload, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            logger.error("Ошибка обращения к Ollama (chat_with_tools): %s", exc)
            return {"message": {"content": "[Ошибка: локальная модель недоступна.]", "tool_calls": []}}

    def embed(self, text: str, timeout: int = 60) -> list[float]:
        payload = {"model": self.embed_model, "prompt": text}
        try:
            response = requests.post(f"{self.host}/api/embeddings", json=payload, timeout=timeout)
            response.raise_for_status()
            return response.json().get("embedding", [])
        except requests.RequestException as exc:
            logger.error("Ошибка получения эмбеддинга: %s", exc)
            return []
