"""Расчёт цикломатической сложности через radon."""

from apps.static_analysis.runners import run_radon_complexity
from pathlib import Path


def average_complexity(target: Path) -> float:
    data = run_radon_complexity(target)
    complexities = []
    for _file, blocks in data.items():
        for block in blocks:
            complexities.append(block.get("complexity", 0))
    if not complexities:
        return 0.0
    return round(sum(complexities) / len(complexities), 2)
