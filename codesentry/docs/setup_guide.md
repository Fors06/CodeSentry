# Инструкция по установке

## Требования
- Git
- pyenv (Linux/macOS) или pyenv-win (Windows)
- Poetry (ставится автоматически скриптом, если его нет)
- Ollama: https://ollama.com/download

## Шаги

1. Клонировать репозиторий:
   ```
   git clone <url-репозитория>
   cd codesentry
   ```

2. Запустить установку:
   - Linux/macOS: `bash scripts/setup.sh`
   - Windows (PowerShell): `powershell -ExecutionPolicy Bypass -File scripts/setup.ps1`

   Скрипт установит нужную версию Python, зависимости из `poetry.lock`,
   pre-commit хуки и скачает модели Ollama.

3. (Опционально) Сгенерировать демо-данные:
   ```
   poetry run python scripts/seed_demo_data.py
   ```

4. Запустить сайт:
   - Linux/macOS: `bash scripts/run_dev.sh`
   - Windows: `poetry run uvicorn apps.api.main:app --reload`

5. Открыть в браузере: **http://localhost:8000**

## Проверка офлайн-режима

Отключите Wi-Fi/интернет и убедитесь, что:
- Сайт открывается и работает как обычно.
- Вопросы через "Спросить у ИИ" получают ответ от локальной модели.
- Анализ PR (через `seed_demo_data.py` или локальный webhook) проходит успешно.

## Частые проблемы

- **"Ollama не отвечает"** — убедитесь, что в отдельном терминале запущено `ollama serve`.
- **Разные версии зависимостей у разных людей** — убедитесь, что все выполняют
  `poetry install` (без флагов) после `git pull`, а не `poetry update`.
