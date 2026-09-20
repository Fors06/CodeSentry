"""Разбор unified diff на файлы и изменённые строки."""

from dataclasses import dataclass, field


@dataclass
class FileDiff:
    filename: str
    added_lines: list[tuple[int, str]] = field(default_factory=list)  # (номер строки, текст)
    removed_lines: list[str] = field(default_factory=list)


def parse_diff(diff_text: str) -> list[FileDiff]:
    """Простой парсер unified diff (без внешних зависимостей)."""
    files: list[FileDiff] = []
    current: FileDiff | None = None
    current_line_no = 0

    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            current = FileDiff(filename=line[6:])
            files.append(current)
        elif line.startswith("@@"):
            # формат: @@ -a,b +c,d @@
            try:
                plus_part = line.split("+")[1].split()[0]
                current_line_no = int(plus_part.split(",")[0])
            except (IndexError, ValueError):
                current_line_no = 0
        elif current is not None:
            if line.startswith("+") and not line.startswith("+++"):
                current.added_lines.append((current_line_no, line[1:]))
                current_line_no += 1
            elif line.startswith("-") and not line.startswith("---"):
                current.removed_lines.append(line[1:])
            elif not line.startswith("\\"):
                current_line_no += 1

    return files
