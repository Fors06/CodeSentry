"""
Агентский цикл: задача на естественном языке -> модель сама решает,
какие файловые инструменты вызвать -> инструменты выполняются локально
-> результат возвращается модели -> финальный ответ пользователю.

Работает полностью офлайн через локальную Ollama.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import json

from apps.ai_review.ollama_client import OllamaClient
from core.logging_config import get_logger

from . import file_tools
from .analysis import FileAnalyzer
from .tool_schemas import TOOLS

logger = get_logger(__name__)

MAX_STEPS = 8

_FILE_TOOLS_DISPATCH = {
    "list_files": file_tools.list_files,
    "read_file": file_tools.read_file,
    "write_file": file_tools.write_file,
    "append_file": file_tools.append_file,
    "delete_file": file_tools.delete_file,
    "create_directory": file_tools.create_directory,
    "list_files_recursive": file_tools.list_files_recursive,
    "search_files_by_name": file_tools.search_by_name,
    "search_file_content": file_tools.search_by_content,
}

# Эти инструменты сами обращаются к LLM (объяснение файла/папки), поэтому
# вызываются отдельно от простых файловых операций — им нужен self.analyzer.
_ANALYSIS_TOOLS = {"explain_file", "explain_folder"}

_SYSTEM_PROMPT = """Ты — ассистент, который помогает пользователю управлять файлами
в его рабочей папке на компьютере. У тебя есть инструменты для чтения, создания,
редактирования и удаления файлов. Используй их по одному за шаг, дожидаясь результата.
Перед удалением файла обязательно сначала прочитай/выведи список, чтобы убедиться,
что действуешь правильно. Когда задача выполнена, дай короткий финальный ответ
без вызова инструментов."""


@dataclass
class AgentStep:
    tool_name: str
    arguments: dict[str, Any]
    result: str


@dataclass
class AgentResult:
    answer: str
    steps: list[AgentStep] = field(default_factory=list)


class FileAgent:
    def __init__(self, workspace_root: Path, client: OllamaClient | None = None) -> None:
        self.workspace_root = Path(workspace_root)
        self.workspace_root.mkdir(parents=True, exist_ok=True)
        self.client = client or OllamaClient()
        self.analyzer = FileAnalyzer(self.workspace_root, client=self.client)

    def _execute_tool(self, name: str, arguments: dict[str, Any]) -> str:
        if name in _ANALYSIS_TOOLS:
            if name == "explain_file":
                return self.analyzer.explain_file(**arguments)
            if name == "explain_folder":
                return self.analyzer.explain_folder(**arguments)

        func = _FILE_TOOLS_DISPATCH.get(name)
        if not func:
            return f"Ошибка: неизвестный инструмент '{name}'."
        try:
            result = func(self.workspace_root, **arguments)
            if not isinstance(result, str):
                result = json.dumps(result, ensure_ascii=False, indent=2)
            return result
        except file_tools.UnsafePathError as exc:
            logger.warning("Заблокирована небезопасная попытка доступа к файлу: %s", exc)
            return f"Отклонено из соображений безопасности: {exc}"
        except Exception as exc:  # noqa: BLE001
            logger.exception("Ошибка выполнения инструмента %s", name)
            return f"Ошибка при выполнении '{name}': {exc}"

    def run(self, task: str, max_steps: int = MAX_STEPS) -> AgentResult:
        messages = [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": task},
        ]
        steps: list[AgentStep] = []

        for _ in range(max_steps):
            response = self.client.chat_with_tools(messages, tools=TOOLS)
            message = response.get("message", {})
            tool_calls = message.get("tool_calls") or []

            if not tool_calls:
                final_answer = message.get("content", "").strip()
                return AgentResult(answer=final_answer or "Задача выполнена.", steps=steps)

            messages.append(message)
            for call in tool_calls:
                fn = call.get("function", {})
                name = fn.get("name", "")
                arguments = fn.get("arguments", {}) or {}
                result = self._execute_tool(name, arguments)
                steps.append(AgentStep(tool_name=name, arguments=arguments, result=result))
                messages.append({"role": "tool", "content": result})

        return AgentResult(
            answer="Достигнут лимит шагов агента — задача может быть выполнена не полностью.",
            steps=steps,
        )
