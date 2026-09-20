"""Генерация тестовых данных (PR + находки) для демо и разработки без реального GitHub."""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.config import get_settings  # noqa: E402


def seed() -> None:
    settings = get_settings()
    prs_dir = settings.data_dir / "prs"
    findings_dir = settings.data_dir / "findings"
    metrics_dir = settings.data_dir / "metrics"
    for d in (prs_dir, findings_dir, metrics_dir):
        d.mkdir(parents=True, exist_ok=True)

    demo_pr = {
        "id": "demo-1",
        "title": "Добавить обработку ошибок в payment_service",
        "author": "demo-user",
        "repo": "demo-org/demo-repo",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "analyzed",
        "files_changed": ["payment_service.py"],
    }
    (prs_dir / "demo-1.json").write_text(
        json.dumps(demo_pr, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    demo_findings = {
        "pr_id": "demo-1",
        "findings": [
            {
                "id": "f1",
                "file": "payment_service.py",
                "line": 42,
                "severity": "high",
                "source": "ai_review",
                "message": "Отсутствует обработка исключения при вызове внешнего API оплаты.",
            },
            {
                "id": "f2",
                "file": "payment_service.py",
                "line": 10,
                "severity": "medium",
                "source": "static_analysis",
                "message": "Функция process_payment имеет слишком высокую цикломатическую сложность (12).",
            },
        ],
    }
    (findings_dir / "demo-1.json").write_text(
        json.dumps(demo_findings, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    history_path = metrics_dir / "metrics_history.json"
    history = []
    for i in range(10):
        history.append(
            {
                "date": (datetime.now(timezone.utc) - timedelta(days=10 - i)).date().isoformat(),
                "tech_debt_index": round(50 - i * 1.5, 1),
                "avg_complexity": round(8.0 - i * 0.2, 2),
            }
        )
    history_path.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")

    print("Демо-данные созданы в data/")


if __name__ == "__main__":
    seed()
