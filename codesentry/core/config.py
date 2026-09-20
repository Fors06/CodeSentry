"""Единая конфигурация проекта. Импортируется всеми модулями apps/*."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Ollama
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5-coder:7b-instruct-q4_K_M"
    ollama_embed_model: str = "nomic-embed-text"

    # GitHub
    github_webhook_secret: str = "changeme"

    # Telegram
    telegram_bot_token: str = ""

    # Пути / данные
    data_dir: Path = Path("./data")

    # Рабочая папка, в которой агенту разрешено создавать/редактировать/
    # удалять файлы (песочница). ВАЖНО: указывайте существующую папку,
    # предназначенную именно для работы агента, не системные каталоги.
    agent_workspace_dir: Path = Path("./data/agent_workspace")

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    @property
    def prs_dir(self) -> Path:
        return self.data_dir / "prs"

    @property
    def findings_dir(self) -> Path:
        return self.data_dir / "findings"

    @property
    def metrics_dir(self) -> Path:
        return self.data_dir / "metrics"

    @property
    def repos_cache_dir(self) -> Path:
        return self.data_dir / "repos_cache"

    @property
    def embeddings_dir(self) -> Path:
        return self.data_dir / "embeddings"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    for d in (
        settings.prs_dir,
        settings.findings_dir,
        settings.metrics_dir,
        settings.repos_cache_dir,
        settings.embeddings_dir,
        settings.agent_workspace_dir,
    ):
        d.mkdir(parents=True, exist_ok=True)
    return settings
