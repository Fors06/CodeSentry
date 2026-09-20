"""
Сквозной сценарий: сохранение PR -> сохранение находок -> проверка через API.
Полная интеграция с реальным Ollama/git не тестируется здесь (см. test_offline_mode.py) —
для CI используются моки, чтобы не требовать поднятого Ollama.
"""

from datetime import datetime, timezone

from fastapi.testclient import TestClient

from apps.api.main import app
from apps.persistence.repository import FindingRepository, PRRepository
from core.schemas import Finding, FindingSource, PullRequest, Severity

client = TestClient(app)


def test_full_pr_flow(tmp_data_dir):
    pr = PullRequest(
        id="e2e-1",
        title="E2E test PR",
        author="tester",
        repo="org/repo",
        created_at=datetime.now(timezone.utc),
        status="analyzed",
    )
    PRRepository().save(pr)

    findings = [
        Finding(
            id="f1", file="x.py", line=5, severity=Severity.MEDIUM,
            source=FindingSource.STATIC_ANALYSIS, message="test finding",
        )
    ]
    FindingRepository().save("e2e-1", findings)

    response = client.get("/api/prs/e2e-1")
    assert response.status_code == 200
    assert response.json()["title"] == "E2E test PR"

    response = client.get("/api/findings/e2e-1")
    assert response.status_code == 200
    assert len(response.json()["findings"]) == 1
