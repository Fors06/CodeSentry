"""Пайплайн: diff -> промпт -> структурированные находки (Finding)."""

import json
import uuid
from pathlib import Path

from core.logging_config import get_logger
from core.schemas import Finding, FindingSource, Severity

from .ollama_client import OllamaClient

logger = get_logger(__name__)
_PROMPT_PATH = Path(__file__).parent / "prompts" / "review_diff.txt"


class AIReviewPipeline:
    def __init__(self, client: OllamaClient | None = None) -> None:
        self.client = client or OllamaClient()
        self._prompt_template = _PROMPT_PATH.read_text(encoding="utf-8")

    def review_diff(self, diff: str) -> list[Finding]:
        prompt = self._prompt_template.format(diff=diff)
        raw_response = self.client.generate(prompt)
        return self._parse_response(raw_response)

    @staticmethod
    def _parse_response(raw_response: str) -> list[Finding]:
        try:
            start = raw_response.index("[")
            end = raw_response.rindex("]") + 1
            items = json.loads(raw_response[start:end])
        except (ValueError, json.JSONDecodeError):
            logger.warning("Не удалось распарсить ответ модели как JSON: %s", raw_response[:200])
            return []

        findings = []
        for item in items:
            try:
                findings.append(
                    Finding(
                        id=str(uuid.uuid4()),
                        file=item["file"],
                        line=int(item.get("line", 0)),
                        severity=Severity(item.get("severity", "low")),
                        source=FindingSource.AI_REVIEW,
                        message=item["message"],
                    )
                )
            except (KeyError, ValueError) as exc:
                logger.warning("Пропуск некорректной находки от модели: %s", exc)
        return findings
