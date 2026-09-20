# API-контракт CodeSentry

Базовый URL: `http://localhost:8000`

| Метод | Путь | Описание |
|---|---|---|
| POST | `/webhooks/github` | Приём события GitHub (проверяется подпись HMAC) |
| GET | `/api/prs` | Список всех PR |
| GET | `/api/prs/{pr_id}` | Детали одного PR |
| GET | `/api/findings` | Все находки по всем PR |
| GET | `/api/findings/{pr_id}` | Находки конкретного PR |
| GET | `/api/metrics?last_n=30` | Тренд технического долга |
| POST | `/api/ask` | Вопрос к RAG по кодовой базе (`{question, repo}`) |
| GET | `/health` | Проверка живости сервиса |

Полная интерактивная документация доступна автоматически на
`http://localhost:8000/docs` (Swagger UI от FastAPI) после запуска сервера.
