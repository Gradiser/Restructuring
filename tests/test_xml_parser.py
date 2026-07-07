"""Tests for XML parser."""

import pytest

from src.parser.xml_parser import ParsedAuditReport, XMLParser


class TestXMLParser:
    """Test suite for XMLParser."""

    @pytest.fixture
    def parser(self) -> XMLParser:
        """Create XML parser instance."""
        return XMLParser()

    @pytest.fixture
    def sample_xml(self) -> bytes:
        """Sample DART XML for testing."""
        return b"""<?xml version="1.0" encoding="utf-8"?>
        <AUDIT_REPORT>
            <CORP_CODE>00123456</CORP_CODE>
            <CORP_NAME>Sample Company</CORP_NAME>
            <FILING_DATE>20251231</FILING_DATE>
            <AUDIT_PERIOD_START>20250101</AUDIT_PERIOD_START>
            <AUDIT_PERIOD_END>20251231</AUDIT_PERIOD_END>
            <AUDIT_FIRM_NAME>Sample Audit Firm</AUDIT_FIRM_NAME>
            <OPINION_TYPE>적정의견</OPINION_TYPE>
        </AUDIT_REPORT>
        """

    def test_parse_valid_xml(self, parser: XMLParser, sample_xml: bytes) -> None:
        """Test parsing valid XML."""
        result = parser.parse(sample_xml)
        assert result is not None
        assert result.corp_code == "00123456"
        assert result.corp_name == "Sample Company"
        assert result.audit_opinion == "적정의견"

    def test_parse_invalid_xml(self, parser: XMLParser) -> None:
        """Test parsing invalid XML."""
        invalid_xml = b"<invalid>unclosed"
        result = parser.parse(invalid_xml)
        assert result is None

    def test_parse_empty_xml(self, parser: XMLParser) -> None:
        """Test parsing empty XML."""
        result = parser.parse(b"")
        assert result is None

    def test_extract_financial_statements(
        self, parser: XMLParser, sample_xml: bytes
    ) -> None:
        """Test extracting financial statements."""
        parsed = parser.parse(sample_xml)
        assert parsed is not None

        statements = parser.extract_financial_statements(parsed)
        assert isinstance(statements, list)
