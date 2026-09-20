"""Агрегация истории метрик (metrics_history.json) для отображения трендов."""

from apps.persistence.repository import MetricRepository
from core.schemas import MetricPoint


def get_trend(last_n: int = 30) -> list[MetricPoint]:
    repo = MetricRepository()
    history = repo.list()
    return history[-last_n:]
