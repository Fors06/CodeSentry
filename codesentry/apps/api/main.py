"""
Точка входа FastAPI. Раздаёт REST API и статический веб-дашборд.
Запуск: uvicorn apps.api.main:app --reload  (или scripts/run_dev.sh)
Открывается офлайн в браузере на http://localhost:8000
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from apps.api.routers import agent, chat, findings, metrics, prs, webhooks
from core.config import get_settings
from core.logging_config import configure_logging

configure_logging()
get_settings()  # создаёт папки data/* при старте

app = FastAPI(
    title="CodeSentry",
    description="Локальный офлайн ИИ-ассистент для код-ревью и анализа технического долга",
    version="0.1.0",
)

app.include_router(webhooks.router)
app.include_router(prs.router)
app.include_router(findings.router)
app.include_router(metrics.router)
app.include_router(chat.router)
app.include_router(agent.router)

_STATIC_DIR = Path(__file__).parent.parent / "web" / "static"
app.mount("/", StaticFiles(directory=_STATIC_DIR, html=True), name="web")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
