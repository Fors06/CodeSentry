"""Поиск дополнительных антипаттернов через встроенный модуль ast."""

import ast
from dataclasses import dataclass


@dataclass
class AstFinding:
    file: str
    line: int
    message: str


def find_bare_except(file_path: str, source: str) -> list[AstFinding]:
    """Находит `except:` без указания типа исключения — частый антипаттерн."""
    findings: list[AstFinding] = []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return findings

    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            findings.append(
                AstFinding(
                    file=file_path,
                    line=node.lineno,
                    message="Пустой `except:` перехватывает все исключения — укажите конкретный тип.",
                )
            )
    return findings


def find_mutable_default_args(file_path: str, source: str) -> list[AstFinding]:
    """Находит изменяемые значения по умолчанию в аргументах функций (list/dict)."""
    findings: list[AstFinding] = []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return findings

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for default in node.args.defaults:
                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    findings.append(
                        AstFinding(
                            file=file_path,
                            line=node.lineno,
                            message=(
                                f"Функция `{node.name}` использует изменяемый объект "
                                "по умолчанию — используйте None и инициализацию внутри."
                            ),
                        )
                    )
    return findings
