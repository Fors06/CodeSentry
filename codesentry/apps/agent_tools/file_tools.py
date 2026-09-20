"""
Файловые инструменты, которые локальная LLM может вызывать (function calling)
для создания, чтения, редактирования и удаления файлов.

КРИТИЧЕСКИ ВАЖНО: все операции жёстко ограничены каталогом workspace_root
(например, D:\\AI), заданным в .env как AGENT_WORKSPACE_DIR. Любая попытка
выйти за его пределы (через "..", абсолютные пути другого диска и т.д.)
отклоняется. Это единственное место в проекте, где ИИ получает право
изменять файлы на диске пользователя — весь код здесь должен проходить
особенно внимательное ревью.
"""

from pathlib import Path


class UnsafePathError(Exception):
    """Попытка обратиться к пути за пределами разрешённой рабочей папки."""


def _resolve_safe_path(workspace_root: Path, relative_path: str) -> Path:
    """
    Превращает относительный путь в абсолютный внутри workspace_root
    и проверяет, что результат не выходит за его границы.
    """
    root = workspace_root.resolve()
    candidate = (root / relative_path).resolve()
    if not str(candidate).startswith(str(root)):
        raise UnsafePathError(
            f"Путь '{relative_path}' выходит за пределы рабочей папки '{root}'"
        )
    return candidate


def list_files(workspace_root: Path, relative_dir: str = ".") -> list[str]:
    """Возвращает список файлов и папок внутри relative_dir (нерекурсивно)."""
    target = _resolve_safe_path(workspace_root, relative_dir)
    if not target.exists():
        return []
    return sorted(p.name + ("/" if p.is_dir() else "") for p in target.iterdir())


def read_file(workspace_root: Path, relative_path: str) -> str:
    """Читает содержимое файла как текст."""
    target = _resolve_safe_path(workspace_root, relative_path)
    if not target.exists() or not target.is_file():
        raise FileNotFoundError(f"Файл не найден: {relative_path}")
    return target.read_text(encoding="utf-8", errors="ignore")


def write_file(workspace_root: Path, relative_path: str, content: str) -> str:
    """Создаёт файл или полностью перезаписывает его содержимое."""
    target = _resolve_safe_path(workspace_root, relative_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return f"Файл '{relative_path}' сохранён ({len(content)} символов)."


def append_file(workspace_root: Path, relative_path: str, content: str) -> str:
    """Дописывает содержимое в конец существующего файла."""
    target = _resolve_safe_path(workspace_root, relative_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as f:
        f.write(content)
    return f"В файл '{relative_path}' дописано {len(content)} символов."


def delete_file(workspace_root: Path, relative_path: str) -> str:
    """Удаляет файл (не папку)."""
    target = _resolve_safe_path(workspace_root, relative_path)
    if not target.exists():
        return f"Файл '{relative_path}' уже не существует."
    if target.is_dir():
        raise IsADirectoryError(f"'{relative_path}' — это папка, а не файл. Удаление папок отключено.")
    target.unlink()
    return f"Файл '{relative_path}' удалён."


def create_directory(workspace_root: Path, relative_path: str) -> str:
    """Создаёт папку (и все промежуточные родительские папки)."""
    target = _resolve_safe_path(workspace_root, relative_path)
    target.mkdir(parents=True, exist_ok=True)
    return f"Папка '{relative_path}' создана."


# Расширения файлов, которые пытаемся читать как текст при поиске по содержимому.
# Бинарные файлы (изображения, архивы и т.д.) пропускаются автоматически.
_TEXT_EXTENSIONS = {
    ".py", ".txt", ".md", ".json", ".yaml", ".yml", ".toml", ".cfg", ".ini",
    ".html", ".css", ".js", ".ts", ".jsx", ".tsx", ".csv", ".xml", ".sh",
    ".ps1", ".env", ".gitignore", ".sql", ".log",
}

# Папки, которые всегда пропускаются при рекурсивном обходе (мусор/служебное).
_IGNORED_DIR_NAMES = {".git", "__pycache__", "node_modules", ".venv", ".pytest_cache", ".mypy_cache"}

_MAX_FILE_SIZE_FOR_CONTENT_SEARCH = 2 * 1024 * 1024  # 2 МБ — не читаем гигантские файлы целиком


def _iter_files_recursive(start: Path):
    for path in start.rglob("*"):
        if path.is_dir():
            continue
        if any(part in _IGNORED_DIR_NAMES for part in path.parts):
            continue
        yield path


def list_files_recursive(workspace_root: Path, relative_dir: str = ".") -> list[str]:
    """Возвращает полный список файлов (относительные пути) во всех вложенных папках."""
    start = _resolve_safe_path(workspace_root, relative_dir)
    if not start.exists():
        return []
    root = workspace_root.resolve()
    return sorted(str(p.relative_to(root)).replace("\\", "/") for p in _iter_files_recursive(start))


def search_by_name(workspace_root: Path, pattern: str, relative_dir: str = ".") -> list[str]:
    """
    Ищет файлы и папки, чьё имя содержит `pattern` (регистронезависимо),
    рекурсивно по всей рабочей папке (или её подпапке relative_dir).
    """
    start = _resolve_safe_path(workspace_root, relative_dir)
    if not start.exists():
        return []
    root = workspace_root.resolve()
    pattern_lower = pattern.lower()

    matches = []
    for path in start.rglob("*"):
        if any(part in _IGNORED_DIR_NAMES for part in path.parts):
            continue
        if pattern_lower in path.name.lower():
            rel = str(path.relative_to(root)).replace("\\", "/")
            matches.append(rel + ("/" if path.is_dir() else ""))
    return sorted(matches)


def search_by_content(
    workspace_root: Path,
    query: str,
    relative_dir: str = ".",
    max_results: int = 50,
) -> list[dict]:
    """
    Ищет строку `query` (регистронезависимо) внутри текстовых файлов,
    рекурсивно по всей рабочей папке (или её подпапке relative_dir).
    Возвращает список совпадений: {file, line, snippet}.
    """
    start = _resolve_safe_path(workspace_root, relative_dir)
    if not start.exists():
        return []
    root = workspace_root.resolve()
    query_lower = query.lower()

    results: list[dict] = []
    for path in _iter_files_recursive(start):
        if path.suffix.lower() not in _TEXT_EXTENSIONS:
            continue
        try:
            if path.stat().st_size > _MAX_FILE_SIZE_FOR_CONTENT_SEARCH:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        for line_no, line in enumerate(text.splitlines(), start=1):
            if query_lower in line.lower():
                rel = str(path.relative_to(root)).replace("\\", "/")
                results.append({"file": rel, "line": line_no, "snippet": line.strip()[:200]})
                if len(results) >= max_results:
                    return results
    return results
