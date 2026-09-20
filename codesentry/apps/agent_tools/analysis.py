"""
Анализ содержимого файлов и папок через локальную LLM: объяснение
человеческим языком, что делает файл, и общий обзор структуры папки.
"""

from pathlib import Path

from apps.ai_review.ollama_client import OllamaClient
from core.logging_config import get_logger

from . import file_tools

logger = get_logger(__name__)

_MAX_CHARS_FOR_EXPLANATION = 8000  # обрезаем очень большие файлы перед отправкой в модель

_EXPLAIN_FILE_PROMPT = """Объясни простым, понятным языком, что делает следующий файл.
Не пересказывай код построчно — опиши его назначение, основную логику и,
если это уместно, с чем он связан (например, "это конфигурация FastAPI",
"это скрипт для очистки данных", "это список зависимостей проекта").
Уложись в 4-6 предложений.

Имя файла: {filename}

Содержимое:
---
{content}
---
"""

_EXPLAIN_FOLDER_PROMPT = """Вот список файлов в папке (и подпапках). Опиши простым языком,
судя по именам и структуре, что это за проект или набор данных, и как файлы,
похоже, связаны между собой. Если непонятно — так и скажи, не выдумывай.
Уложись в 5-8 предложений.

Список файлов:
{file_list}
"""


class FileAnalyzer:
    def __init__(self, workspace_root: Path, client: OllamaClient | None = None) -> None:
        self.workspace_root = Path(workspace_root)
        self.client = client or OllamaClient()

    def explain_file(self, relative_path: str) -> str:
        try:
            content = file_tools.read_file(self.workspace_root, relative_path)
        except (FileNotFoundError, file_tools.UnsafePathError) as exc:
            return str(exc)

        truncated = content[:_MAX_CHARS_FOR_EXPLANATION]
        prompt = _EXPLAIN_FILE_PROMPT.format(filename=relative_path, content=truncated)
        return self.client.generate(prompt)

    def explain_folder(self, relative_dir: str = ".") -> str:
        files = file_tools.list_files_recursive(self.workspace_root, relative_dir)
        if not files:
            return "В этой папке не найдено файлов."

        file_list = "\n".join(files[:300])  # ограничение, чтобы не раздувать промпт
        prompt = _EXPLAIN_FOLDER_PROMPT.format(file_list=file_list)
        return self.client.generate(prompt)
