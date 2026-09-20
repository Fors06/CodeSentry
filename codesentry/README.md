# 🛡️ CodeSentry

Локальный, полностью офлайн ИИ-ассистент для код-ревью и анализа
технического долга. Локальная LLM (через Ollama) анализирует диффы
Pull Request'ов, ищет баги и уязвимости, отвечает на вопросы по
кодовой базе через RAG, а веб-дашборд показывает тренды качества кода.

**Особенности:**
- Никакого Docker — единообразие окружения через pyenv + Poetry.
- Никакой внешней БД — все данные в JSON-файлах на диске (`data/`).
- Никакого интернета в рантайме — ИИ работает через локальный Ollama.

## Быстрый старт

См. подробную инструкцию: [`docs/setup_guide.md`](docs/setup_guide.md)

```bash
git clone <url-репозитория>
cd codesentry
bash scripts/setup.sh          # или scripts/setup.ps1 на Windows
poetry run python scripts/seed_demo_data.py   # демо-данные (опционально)
bash scripts/run_dev.sh
```

Открыть: **http://localhost:8000**

## Документация

- [`docs/architecture.md`](docs/architecture.md) — архитектура и потоки данных
- [`docs/data_format.md`](docs/data_format.md) — формат JSON-контракта
- [`docs/api_contract.md`](docs/api_contract.md) — REST API
- [`docs/setup_guide.md`](docs/setup_guide.md) — установка и запуск
- [`docs/agent_capabilities.md`](docs/agent_capabilities.md) — файловый агент (create/edit/delete в песочнице)

## Структура проекта

```
apps/
├── static_analysis/  # ruff, bandit, radon, ast-паттерны
├── ai_review/         # промпты + вызовы Ollama для ревью диффов
├── rag/                # индексация кода и поиск контекста (без векторной БД)
├── git_integration/    # webhook, клонирование, парсинг диффов
├── agent_tools/         # create/edit/delete файлов в песочнице (AGENT_WORKSPACE_DIR)
├── api/                # FastAPI: роуты + фоновая обработка
├── persistence/        # JSON-хранилище вместо БД (repository-паттерн)
├── web/                # статический дашборд (HTML/CSS/JS)
├── bot/                # Telegram-уведомления
└── metrics/            # индекс техдолга, сложность, тренды
core/                   # общая конфигурация и Pydantic-схемы (контракт)
tests/                  # интеграционные тесты
docs/                   # документация
scripts/                # setup, запуск, демо-данные
```

## Команда и роли

| Модуль | Роль |
|---|---|
| Tech Lead | Архитектура, контракты, CI, ревью |
| `static_analysis` | Static Analysis Dev |
| `ai_review` | AI Engineer (промпты) |
| `rag` | AI Engineer (RAG) |
| `git_integration` | Git Integration Dev |
| `api` | Backend Dev |
| `persistence` | Storage/Persistence Dev |
| `web` | Frontend Dev |
| `bot` + `metrics` | Bot/Infra Dev |

## Разработка

```bash
poetry run pytest              # тесты
poetry run ruff check .        # линт
poetry run mypy apps core      # типы
```

Pre-commit хуки запускаются автоматически при коммите (см. `.pre-commit-config.yaml`).
