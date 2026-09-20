"""REST-эндпоинт для трендов технического долга."""

from fastapi import APIRouter

from apps.metrics.trends import get_trend
from core.schemas import MetricPoint

router = APIRouter(prefix="/api/metrics", tags=["metrics"])


@router.get("", response_model=list[MetricPoint])
def metrics_trend(last_n: int = 30) -> list[MetricPoint]:
    return get_trend(last_n)
