from unittest.mock import MagicMock

from apps.ai_review.review_pipeline import AIReviewPipeline


def test_parse_response_valid_json():
    mock_client = MagicMock()
    mock_client.generate.return_value = (
        '[{"file": "a.py", "line": 10, "severity": "high", "message": "Проблема"}]'
    )
    pipeline = AIReviewPipeline(client=mock_client)
    findings = pipeline.review_diff("some diff")
    assert len(findings) == 1
    assert findings[0].severity.value == "high"


def test_parse_response_invalid_json_returns_empty():
    mock_client = MagicMock()
    mock_client.generate.return_value = "не JSON вообще"
    pipeline = AIReviewPipeline(client=mock_client)
    findings = pipeline.review_diff("some diff")
    assert findings == []
