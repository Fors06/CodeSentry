from apps.git_integration.diff_parser import parse_diff

SAMPLE_DIFF = """diff --git a/app.py b/app.py
index abc123..def456 100644
--- a/app.py
+++ b/app.py
@@ -1,3 +1,4 @@
 def foo():
-    return 1
+    return 2
+    # comment
"""


def test_parse_diff_extracts_filename():
    files = parse_diff(SAMPLE_DIFF)
    assert len(files) == 1
    assert files[0].filename == "app.py"


def test_parse_diff_extracts_added_lines():
    files = parse_diff(SAMPLE_DIFF)
    added_texts = [text for _, text in files[0].added_lines]
    assert "    return 2" in added_texts
