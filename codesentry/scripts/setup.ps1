# Единая настройка окружения для всех участников проекта (Windows)
$ErrorActionPreference = "Stop"

Write-Host "=== CodeSentry: настройка окружения ===" -ForegroundColor Cyan

# 1. Проверка pyenv-win
if (-not (Get-Command pyenv -ErrorAction SilentlyContinue)) {
    Write-Host "pyenv-win не найден. Установите: https://github.com/pyenv-win/pyenv-win" -ForegroundColor Red
    exit 1
}

$pyver = Get-Content ".python-version"
Write-Host "Устанавливаю Python $pyver через pyenv-win..."
pyenv install -s $pyver
pyenv local $pyver

# 2. Проверка Poetry
if (-not (Get-Command poetry -ErrorAction SilentlyContinue)) {
    Write-Host "Poetry не найден. Устанавливаю..."
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
}

# 3. Установка зависимостей
Write-Host "Устанавливаю зависимости (poetry install)..."
poetry install --no-interaction

# 4. Pre-commit хуки
Write-Host "Устанавливаю pre-commit хуки..."
poetry run pre-commit install

# 5. Проверка Ollama
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Host "ВНИМАНИЕ: Ollama не найдена. Установите с https://ollama.com/download" -ForegroundColor Yellow
    Write-Host "После установки выполните: powershell scripts/pull_model.ps1"
} else {
    Write-Host "Ollama найдена. Скачиваю модель..."
    ollama pull qwen2.5-coder:7b-instruct-q4_K_M
    ollama pull nomic-embed-text
}

# 6. Копирование .env
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Создан .env из .env.example — при необходимости отредактируйте."
}

Write-Host "=== Готово! Запуск: powershell scripts/run_dev.ps1 ===" -ForegroundColor Green
