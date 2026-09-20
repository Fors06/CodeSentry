from apps.metrics.tech_debt import calculate_tech_debt_index
from core.schemas import Finding, FindingSource, Severity


def test_calculate_tech_debt_index():
    findings = [
        Finding(id="1", file="a.py", line=1, severity=Severity.HIGH, source=FindingSource.AI_REVIEW, message="x"),
        Finding(id="2", file="a.py", line=2, severity=Severity.LOW, source=FindingSource.STATIC_ANALYSIS, message="y"),
    ]
    index = calculate_tech_debt_index(findings, avg_complexity=5.0)
    assert index == 7 + 1 + 10  # high(7) + low(1) + complexity(5*2)
