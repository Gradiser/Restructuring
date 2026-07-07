"""XML parser for DART audit reports.

Parses DART XML documents to extract structured audit data.
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from lxml import etree

logger = logging.getLogger(__name__)


@dataclass
class ParsedAuditReport:
    """Parsed audit report data."""

    corp_code: str
    corp_name: str
    filing_date: str
    period_start: str
    period_end: str
    audit_firm: str
    audit_opinion: str
    report_content: str
    raw_xml: Optional[bytes] = None
    parsed_at: datetime = None

    def __post_init__(self) -> None:
        """Initialize parsed_at timestamp."""
        if self.parsed_at is None:
            self.parsed_at = datetime.now()


@dataclass
class FinancialStatement:
    """Extracted financial statement data."""

    report_id: str
    statement_type: str
    period_end: str
    data: dict[str, Any]


class XMLParser:
    """Parser for DART XML audit reports."""

    def __init__(self) -> None:
        """Initialize XML parser."""
        self.parser = etree.XMLParser(remove_blank_text=True)

    def parse(self, xml_content: bytes) -> Optional[ParsedAuditReport]:
        """Parse DART XML audit report.

        Args:
            xml_content: Raw XML bytes from DART

        Returns:
            ParsedAuditReport if parsing successful, None otherwise
        """
        try:
            # Parse XML with namespace handling
            root = etree.fromstring(xml_content, parser=self.parser)
            logger.info("Successfully parsed XML document")

            # Extract company information
            corp_code = self._extract_text(root, ".//CORP_CODE")
            corp_name = self._extract_text(root, ".//CORP_NAME")

            # Extract audit period
            period_start = self._extract_text(root, ".//AUDIT_PERIOD_START")
            period_end = self._extract_text(root, ".//AUDIT_PERIOD_END")
            filing_date = self._extract_text(root, ".//FILING_DATE")

            # Extract auditor information
            audit_firm = self._extract_text(root, ".//AUDIT_FIRM_NAME")

            # Extract audit opinion
            audit_opinion = self._extract_text(root, ".//OPINION_TYPE")

            # Get full report content
            report_content = etree.tostring(root, pretty_print=True, encoding="unicode")

            return ParsedAuditReport(
                corp_code=corp_code,
                corp_name=corp_name,
                filing_date=filing_date or "",
                period_start=period_start or "",
                period_end=period_end or "",
                audit_firm=audit_firm or "",
                audit_opinion=audit_opinion or "",
                report_content=report_content,
                raw_xml=xml_content,
            )

        except etree.XMLSyntaxError as e:
            logger.error(f"XML parsing error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error parsing XML: {e}")
            return None

    def _extract_text(self, element: Any, xpath: str) -> Optional[str]:
        """Extract text from XML element using XPath.

        Args:
            element: XML element to search
            xpath: XPath expression

        Returns:
            Extracted text or None if not found
        """
        try:
            result = element.xpath(xpath)
            if result:
                if isinstance(result[0], str):
                    return result[0].strip() if result[0] else None
                else:
                    text = result[0].text
                    return text.strip() if text else None
        except Exception as e:
            logger.debug(f"Error extracting text with XPath {xpath}: {e}")
        return None

    def extract_financial_statements(
        self, parsed_report: ParsedAuditReport
    ) -> list[FinancialStatement]:
        """Extract financial statements from parsed report.

        Args:
            parsed_report: Parsed audit report

        Returns:
            List of extracted financial statements
        """
        statements = []
        try:
            if not parsed_report.raw_xml:
                logger.warning("No raw XML available for statement extraction")
                return statements

            root = etree.fromstring(parsed_report.raw_xml, parser=self.parser)
            statement_elements = root.xpath(".//FINANCIAL_STATEMENT")

            for stmt_elem in statement_elements:
                stmt_type = self._extract_text(stmt_elem, ".//TYPE")
                period_end = self._extract_text(stmt_elem, ".//PERIOD_END")

                if stmt_type and period_end:
                    # Extract statement data (simplified)
                    stmt_data = {"raw_content": etree.tostring(stmt_elem, encoding="unicode")}

                    statement = FinancialStatement(
                        report_id=parsed_report.corp_code,
                        statement_type=stmt_type,
                        period_end=period_end,
                        data=stmt_data,
                    )
                    statements.append(statement)

            logger.info(f"Extracted {len(statements)} financial statements")
        except Exception as e:
            logger.error(f"Error extracting financial statements: {e}")

        return statements
