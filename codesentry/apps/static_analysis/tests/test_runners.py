from apps.static_analysis.ast_patterns import find_bare_except, find_mutable_default_args


def test_find_bare_except():
    source = "try:\n    pass\nexcept:\n    pass\n"
    findings = find_bare_except("test.py", source)
    assert len(findings) == 1
    assert findings[0].line == 3


def test_find_mutable_default_args():
    source = "def f(items=[]):\n    pass\n"
    findings = find_mutable_default_args("test.py", source)
    assert len(findings) == 1
