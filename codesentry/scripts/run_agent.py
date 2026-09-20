"""
Запуск файлового агента напрямую из терминала, без веб-интерфейса.
Пример:
    poetry run python scripts/run_agent.py "создай файл README.md с заголовком проекта"
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from apps.agent_tools.agent import FileAgent  # noqa: E402
from core.config import get_settings  # noqa: E402


def main() -> None:
    if len(sys.argv) < 2:
        print('Использование: python scripts/run_agent.py "текст задачи"')
        sys.exit(1)

    task = " ".join(sys.argv[1:])
    settings = get_settings()
    print(f"Рабочая папка агента: {settings.agent_workspace_dir.resolve()}")
    print(f"Задача: {task}\n")

    agent = FileAgent(workspace_root=settings.agent_workspace_dir)
    result = agent.run(task)

    for i, step in enumerate(result.steps, 1):
        print(f"[Шаг {i}] {step.tool_name}({step.arguments}) -> {step.result}")

    print(f"\nИтог: {result.answer}")


if __name__ == "__main__":
    main()
