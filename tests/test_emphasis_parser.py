"""Tests for emphasis parser."""

import pytest

from src.parser.emphasis_parser import EmphasisParser


class TestEmphasisParser:
    """Test suite for EmphasisParser."""

    @pytest.fixture
    def parser(self) -> EmphasisParser:
        """Create emphasis parser instance."""
        return EmphasisParser()

    def test_detect_going_concern_warning(self, parser: EmphasisParser) -> None:
        """Test detecting going concern warning."""
        text = "회사의 계속기업의정성에 대하여 중대한 의문이 있습니다."
        warning = parser._detect_going_concern(text)
        assert warning.warning_present is True
        assert warning.severity == "critical"

    def test_no_going_concern_warning(self, parser: EmphasisParser) -> None:
        """Test when no going concern warning."""
        text = "회사의 재무상태는 건전합니다."
        warning = parser._detect_going_concern(text)
        assert warning.warning_present is False

    def test_parse_emphasis_matters(self, parser: EmphasisParser) -> None:
        """Test parsing emphasis matters."""
        text = "수익인식정책은 중요한 감사상 핵심사항입니다. 회사의 관련자거래가 중요합니다."
        matters = parser.parse_emphasis_matters(text)
        assert len(matters) > 0
        assert any(m.category == "revenue_recognition" for m in matters)
        assert any(m.category == "related_party" for m in matters)

    def test_calculate_risk_score_empty(self, parser: EmphasisParser) -> None:
        """Test risk score calculation with empty matters."""
        risk_score = parser.calculate_risk_score([])
        assert risk_score == 0.0

    def test_calculate_risk_score_critical(self, parser: EmphasisParser) -> None:
        """Test risk score with critical matters."""
        text = "계속기업의정성에 대하여 중대한 의문이 있습니다."
        matters = parser.parse_emphasis_matters(text)
        risk_score = parser.calculate_risk_score(matters)
        assert risk_score > 0.5

    def test_detect_litigation(self, parser: EmphasisParser) -> None:
        """Test detecting litigation emphasis."""
        text = "회사는 현재 진행 중인 소송이 있습니다."
        matters = parser.parse_emphasis_matters(text)
        assert any(m.category == "litigation" for m in matters)

    def test_detect_impairment(self, parser: EmphasisParser) -> None:
        """Test detecting impairment emphasis."""
        text = "회사는 재산손상차손을 인식했습니다."
        matters = parser.parse_emphasis_matters(text)
        assert any(m.category == "impairment" for m in matters)
