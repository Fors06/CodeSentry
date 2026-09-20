#!/usr/bin/env bash
# Скачивание фиксированных версий моделей — одинаковые у всей команды
set -e
ollama pull qwen2.5-coder:7b-instruct-q4_K_M
ollama pull nomic-embed-text
echo "Модели скачаны. Проверка офлайн-режима: отключите интернет и запустите run_dev.sh"
