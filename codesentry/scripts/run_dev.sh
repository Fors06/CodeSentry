#!/usr/bin/env bash
set -e
echo "Проверка, что Ollama запущена..."
if ! curl -s http://localhost:11434 > /dev/null; then
    echo "Ollama не отвечает. Запустите 'ollama serve' в отдельном терминале."
    exit 1
fi
echo "Ollama работает. Запускаю сайт на http://localhost:8000 ..."
poetry run uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000
