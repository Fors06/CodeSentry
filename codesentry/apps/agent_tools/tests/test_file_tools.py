import tempfile
from pathlib import Path

import pytest

from apps.agent_tools import file_tools


@pytest.fixture
def workspace():
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)


def test_write_and_read_file(workspace):
    file_tools.write_file(workspace, "notes.txt", "привет")
    assert file_tools.read_file(workspace, "notes.txt") == "привет"


def test_append_file(workspace):
    file_tools.write_file(workspace, "log.txt", "строка1\n")
    file_tools.append_file(workspace, "log.txt", "строка2\n")
    content = file_tools.read_file(workspace, "log.txt")
    assert content == "строка1\nстрока2\n"


def test_delete_file(workspace):
    file_tools.write_file(workspace, "temp.txt", "x")
    result = file_tools.delete_file(workspace, "temp.txt")
    assert "удалён" in result
    assert not (workspace / "temp.txt").exists()


def test_list_files(workspace):
    file_tools.write_file(workspace, "a.txt", "1")
    file_tools.create_directory(workspace, "sub")
    files = file_tools.list_files(workspace, ".")
    assert "a.txt" in files
    assert "sub/" in files


def test_path_traversal_blocked(workspace):
    """Критический тест: попытка выйти за пределы рабочей папки через '..' должна блокироваться."""
    with pytest.raises(file_tools.UnsafePathError):
        file_tools.read_file(workspace, "../../../../etc/passwd")


def test_absolute_path_outside_workspace_blocked(workspace):
    with pytest.raises(file_tools.UnsafePathError):
        file_tools.write_file(workspace, "/etc/evil.txt", "hacked")


def test_read_nonexistent_file_raises(workspace):
    with pytest.raises(FileNotFoundError):
        file_tools.read_file(workspace, "does_not_exist.txt")


def test_delete_directory_raises(workspace):
    file_tools.create_directory(workspace, "somedir")
    with pytest.raises(IsADirectoryError):
        file_tools.delete_file(workspace, "somedir")


def test_search_by_name_recursive(workspace):
    file_tools.create_directory(workspace, "sub")
    file_tools.write_file(workspace, "report.txt", "x")
    file_tools.write_file(workspace, "sub/report_2024.txt", "y")
    file_tools.write_file(workspace, "sub/other.md", "z")

    matches = file_tools.search_by_name(workspace, "report")
    assert "report.txt" in matches
    assert "sub/report_2024.txt" in matches
    assert "sub/other.md" not in matches


def test_search_by_content_finds_line_and_number(workspace):
    file_tools.write_file(workspace, "a.py", "def foo():\n    return 'hello world'\n")
    results = file_tools.search_by_content(workspace, "hello")
    assert len(results) == 1
    assert results[0]["file"] == "a.py"
    assert results[0]["line"] == 2


def test_search_by_content_is_case_insensitive(workspace):
    file_tools.write_file(workspace, "a.txt", "Секретное СЛОВО тут")
    results = file_tools.search_by_content(workspace, "слово")
    assert len(results) == 1


def test_list_files_recursive(workspace):
    file_tools.create_directory(workspace, "sub")
    file_tools.write_file(workspace, "top.txt", "1")
    file_tools.write_file(workspace, "sub/nested.txt", "2")

    files = file_tools.list_files_recursive(workspace)
    assert "top.txt" in files
    assert "sub/nested.txt" in files


def test_search_by_name_traversal_blocked(workspace):
    with pytest.raises(file_tools.UnsafePathError):
        file_tools.search_by_name(workspace, "x", relative_dir="../../")
