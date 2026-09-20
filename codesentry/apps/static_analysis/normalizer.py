"""Приведение вывода разных линтеров/анализаторов к единому формату Finding."""

import uuid

from core.schemas import Finding, FindingSource, Severity

_BANDIT_SEVERITY_MAP = {
    "LOW": Severity.LOW,
    "MEDIUM": Severity.MEDIUM,
    "HIGH": Severity.HIGH,
}


def from_ruff(raw: list[dict]) -> list[Finding]:
    findings = []
    for item in raw:
        findings.append(
            Finding(
                id=str(uuid.uuid4()),
                file=item.get("filename", "unknown"),
                line=item.get("location", {}).get("row", 0),
                severity=Severity.LOW,
                source=FindingSource.STATIC_ANALYSIS,
                message=f"[{item.get('code')}] {item.get('message')}",
            )
        )
    return findings


def from_bandit(raw: list[dict]) -> list[Finding]:
    findings = []
    for item in raw:
        findings.append(
            Finding(
                id=str(uuid.uuid4()),
                file=item.get("filename", "unknown"),
                line=item.get("line_number", 0),
                severity=_BANDIT_SEVERITY_MAP.get(item.get("issue_severity", "LOW"), Severity.LOW),
                source=FindingSource.STATIC_ANALYSIS,
                message=item.get("issue_text", ""),
            )
        )
    return findings
