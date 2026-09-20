#!/usr/bin/env bash
# Единая настройка окружения для всех участников проекта (Linux/macOS)
set -e

echo "=== CodeSentry: настройка окружения ==="

# 1. Проверка / установка pyenv
if ! command -v pyenv &> /dev/null; then
    echo "pyenv не найден. Установите его: https://github.com/pyenv/pyenv#installation"
    exit 1
fi

PYVER=$(cat .python-version)
echo "Устанавливаю Python $PYVER через pyenv..."
pyenv install -s "$PYVER"
pyenv local "$PYVER"

# 2. Проверка / установка Poetry
if ! command -v poetry &> /dev/null; then
    echo "Poetry не найден. Устанавливаю..."
    curl -sSL https://install.python-poetry.org | python3 -
fi

# 3. Установка зависимостей строго по lock-файлу
echo "Устанавливаю зависимости (poetry install)..."
poetry install --no-interaction

# 4. Pre-commit хуки
echo "Устанавливаю pre-commit хуки..."
poetry run pre-commit install

# 5. Проверка Ollama
if ! command -v ollama &> /dev/null; then
    echo "ВНИМАНИЕ: Ollama не найдена. Установите с https://ollama.com/download"
    echo "После установки выполните: bash scripts/pull_model.sh"
else
    echo "Ollama найдена. Скачиваю модель..."
    bash scripts/pull_model.sh
fi

# 6. Копирование .env
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Создан .env из .env.example — при необходимости отредактируйте."
fi

echo "=== Готово! Запуск: bash scripts/run_dev.sh ==="
