"""Получение эмбеддингов текста через локальную Ollama (без внешних API)."""

from apps.ai_review.ollama_client import OllamaClient


class Embedder:
    def __init__(self, client: OllamaClient | None = None) -> None:
        self.client = client or OllamaClient()

    def embed_text(self, text: str) -> list[float]:
        return self.client.embed(text)

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_text(t) for t in texts]
