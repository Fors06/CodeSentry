# Формат данных (JSON-контракт)

Так как в проекте нет схемы БД, эти структуры — единственный контракт
между Backend, Frontend, AI-модулями и Persistence. Источник истины —
Pydantic-модели в `core/schemas.py`; этот файл — их человекочитаемое описание.

## PullRequest (`data/prs/{id}.json`)

| Поле | Тип | Описание |
|---|---|---|
| id | string | Уникальный идентификатор PR |
| title | string | Заголовок PR |
| author | string | Логин автора |
| repo | string | `owner/name` |
| created_at | datetime (ISO 8601) | Дата создания |
| status | `pending \| analyzing \| analyzed \| error` | Статус обработки |
| files_changed | string[] | Список изменённых файлов |

## Finding (внутри `data/findings/{pr_id}.json` → `findings[]`)

| Поле | Тип | Описание |
|---|---|---|
| id | string (uuid) | Уникальный id находки |
| file | string | Путь к файлу |
| line | int | Номер строки |
| severity | `low \| medium \| high \| critical` | Уровень серьёзности |
| source | `static_analysis \| ai_review` | Откуда находка |
| message | string | Человекочитаемое описание проблемы |

## MetricPoint (элемент массива `data/metrics/metrics_history.json`)

| Поле | Тип | Описание |
|---|---|---|
| date | string (YYYY-MM-DD) | Дата снятия метрики |
| tech_debt_index | float | Индекс технического долга |
| avg_complexity | float | Средняя цикломатическая сложность |

## Правило изменения контракта

Любое изменение полей в `core/schemas.py` обсуждается со всей командой
на стендапе — это меняет то, что ожидают Frontend и все AI-модули.
