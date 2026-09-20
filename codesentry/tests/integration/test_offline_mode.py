"""
Проверка, что при недоступности Ollama система не падает, а деградирует
предсказуемо (возвращает понятное сообщение вместо необработанного исключения).
"""

from apps.ai_review.ollama_client import OllamaClient


def test_ollama_client_handles_connection_error(monkeypatch):
    client = OllamaClient()
    client.host = "http://localhost:1"  # заведомо недоступный порт

    result = client.generate("тестовый промпт")
    assert "недоступна" in result.lower() or "ошибка" in result.lower()
