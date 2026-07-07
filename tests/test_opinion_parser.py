"""Tests for opinion parser."""

import pytest

from src.parser.opinion_parser import AuditOpinion, OpinionParser


class TestOpinionParser:
    """Test suite for OpinionParser."""

    @pytest.fixture
    def parser(self) -> OpinionParser:
        """Create opinion parser instance."""
        return OpinionParser()

    def test_classify_unqualified_opinion(self, parser: OpinionParser) -> None:
        """Test classifying unqualified opinion."""
        text = "재무제표는 적정의견으로 표현합니다."
        opinion = parser.parse_opinion(text)
        assert opinion.opinion_type == "적정의견"
        assert opinion.confidence > 0.8

    def test_classify_qualified_opinion(self, parser: OpinionParser) -> None:
        """Test classifying qualified opinion."""
        text = "다음을 제외하고는 한정의견을 표현합니다."
        opinion = parser.parse_opinion(text)
        assert opinion.opinion_type == "한정의견"

    def test_classify_adverse_opinion(self, parser: OpinionParser) -> None:
        """Test classifying adverse opinion."""
        text = "부정의견을 표현합니다. 재무제표는 적절하지 않습니다."
        opinion = parser.parse_opinion(text)
        assert opinion.opinion_type == "부정의견"

    def test_classify_disclaimer(self, parser: OpinionParser) -> None:
        """Test classifying disclaimer of opinion."""
        text = "충분한 감사증거를 얻지 못했으므로 의견거절합니다."
        opinion = parser.parse_opinion(text)
        assert opinion.opinion_type == "의견거절"

    def test_detect_going_concern(self, parser: OpinionParser) -> None:
        """Test going concern detection."""
        text = "계속기업의정성에 대하여 중대한 의문이 있습니다."
        result = parser.detect_going_concern(text)
        assert result is True

    def test_no_going_concern(self, parser: OpinionParser) -> None:
        """Test when no going concern warning."""
        text = "재무제표는 적정의견입니다."
        result = parser.detect_going_concern(text)
        assert result is False

    def test_empty_opinion_text(self, parser: OpinionParser) -> None:
        """Test parsing empty opinion text."""
        opinion = parser.parse_opinion("")
        assert opinion.opinion_type == "미정의"
        assert opinion.confidence == 0.0

    def test_extract_qualified_items(self, parser: OpinionParser) -> None:
        """Test extracting qualified items."""
        text = "재고자산에 대하여 제외하고는 한정의견을 표현합니다."
        qualified_items = parser._extract_qualified_items(text)
        assert len(qualified_items) > 0
