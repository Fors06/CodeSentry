from fastapi.testclient import TestClient

from apps.api.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_prs_empty(tmp_data_dir):
    response = client.get("/api/prs")
    assert response.status_code == 200
    assert response.json() == []


def test_metrics_empty(tmp_data_dir):
    response = client.get("/api/metrics")
    assert response.status_code == 200
