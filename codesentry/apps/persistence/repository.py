"""
Репозитории — единственная точка входа для остальных модулей.
Никто, кроме этого файла, не должен импортировать storage.py напрямую.
"""

from core.config import get_settings
from core.schemas import Finding, FindingsForPR, MetricPoint, PullRequest

from . import storage


class PRRepository:
    def __init__(self) -> None:
        self._settings = get_settings()

    def save(self, pr: PullRequest) -> None:
        path = self._settings.prs_dir / f"{pr.id}.json"
        storage.write_json(path, pr.model_dump())

    def get(self, pr_id: str) -> PullRequest | None:
        path = self._settings.prs_dir / f"{pr_id}.json"
        data = storage.read_json(path)
        return PullRequest.model_validate(data) if data else None

    def list(self) -> list[PullRequest]:
        result = []
        for path in storage.list_json_files(self._settings.prs_dir):
            data = storage.read_json(path)
            if data:
                result.append(PullRequest.model_validate(data))
        return sorted(result, key=lambda p: p.created_at, reverse=True)


class FindingRepository:
    def __init__(self) -> None:
        self._settings = get_settings()

    def save(self, pr_id: str, findings: list[Finding]) -> None:
        path = self._settings.findings_dir / f"{pr_id}.json"
        payload = FindingsForPR(pr_id=pr_id, findings=findings)
        storage.write_json(path, payload.model_dump())

    def get(self, pr_id: str) -> FindingsForPR:
        path = self._settings.findings_dir / f"{pr_id}.json"
        data = storage.read_json(path)
        return FindingsForPR.model_validate(data) if data else FindingsForPR(pr_id=pr_id)

    def list_all(self) -> list[FindingsForPR]:
        result = []
        for path in storage.list_json_files(self._settings.findings_dir):
            data = storage.read_json(path)
            if data:
                result.append(FindingsForPR.model_validate(data))
        return result


class MetricRepository:
    def __init__(self) -> None:
        self._settings = get_settings()
        self._history_path = self._settings.metrics_dir / "metrics_history.json"

    def append(self, point: MetricPoint) -> None:
        history = storage.read_json(self._history_path, default=[])
        history.append(point.model_dump())
        storage.write_json(self._history_path, history)

    def list(self) -> list[MetricPoint]:
        history = storage.read_json(self._history_path, default=[])
        return [MetricPoint.model_validate(item) for item in history]
