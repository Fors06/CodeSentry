"""
Расчёт условного индекса технического долга на основе находок и сложности.
Формула упрощённая — можно дорабатывать по мере развития проекта.
"""

from core.schemas import Finding, Severity

_SEVERITY_WEIGHTS = {
    Severity.LOW: 1,
    Severity.MEDIUM: 3,
    Severity.HIGH: 7,
    Severity.CRITICAL: 15,
}


def calculate_tech_debt_index(findings: list[Finding], avg_complexity: float) -> float:
    findings_score = sum(_SEVERITY_WEIGHTS[f.severity] for f in findings)
    return round(findings_score + avg_complexity * 2, 1)
