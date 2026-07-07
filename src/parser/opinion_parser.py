"""Opinion parser for extracting audit opinions and key audit matters.

Parses audit opinion sections and key audit matters (감사상 핵심사항) from audit reports.
"""

import logging
import re
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class KeyAuditMatter:
    """Key audit matter (감사상 핵심사항)."""

    title: str
    description: str
    scope: Optional[str] = None
    procedures: Optional[str] = None
    audit_response: Optional[str] = None


@dataclass
class AuditOpinion:
    """Structured audit opinion."""

    opinion_type: str  # 적정, 한정, 부정, 의견거절
    opinion_text: str
    qualified_items: list[str] = field(default_factory=list)
    qualification_reason: Optional[str] = None
    key_audit_matters: list[KeyAuditMatter] = field(default_factory=list)
    confidence: float = 1.0


class OpinionParser:
    """Parser for audit opinions and key audit matters."""

    # Korean audit opinion keywords
    OPINION_KEYWORDS = {
        "적정의견": ["적정의견", "unqualified", "clean opinion"],
        "한정의견": ["한정의견", "qualified opinion", "except for"],
        "부정의견": ["부정의견", "adverse opinion", "does not present"],
        "의견거절": ["의견거절", "disclaimer", "unable to obtain"],
    }

    # Korean going concern keywords
    GOING_CONCERN_KEYWORDS = [
        "계속기업",
        "going concern",
        "계속성",
        "중대한의문",
        "substantial doubt",
    ]

    # Qualification keywords
    QUALIFICATION_KEYWORDS = [
        "제한적",
        "제외하고는",
        "제외",
        "except for",
        "excluding",
    ]

    def __init__(self) -> None:
        """Initialize opinion parser."""
        self._opinion_patterns = self._compile_patterns()

    def _compile_patterns(self) -> dict[str, re.Pattern]:
        """Compile regex patterns for opinion detection.

        Returns:
            Dictionary of compiled patterns
        """
        patterns = {}
        for opinion_type, keywords in self.OPINION_KEYWORDS.items():
            pattern = "|".join(re.escape(kw) for kw in keywords)
            patterns[opinion_type] = re.compile(pattern, re.IGNORECASE)
        return patterns

    def parse_opinion(self, opinion_text: str) -> AuditOpinion:
        """Parse audit opinion from text.

        Args:
            opinion_text: Opinion section text

        Returns:
            Parsed AuditOpinion object
        """
        if not opinion_text:
            logger.warning("Empty opinion text provided")
            return AuditOpinion(
                opinion_type="미정의",
                opinion_text="",
                confidence=0.0,
            )

        # Determine opinion type
        opinion_type = self._classify_opinion_type(opinion_text)

        # Extract qualification details if qualified opinion
        qualified_items = []
        qualification_reason = None
        if opinion_type == "한정의견":
            qualified_items = self._extract_qualified_items(opinion_text)
            qualification_reason = self._extract_qualification_reason(opinion_text)

        # Extract key audit matters
        key_audit_matters = self._extract_key_audit_matters(opinion_text)

        # Calculate confidence score
        confidence = self._calculate_confidence(opinion_type, opinion_text)

        logger.info(f"Parsed audit opinion: {opinion_type} (confidence: {confidence:.2f})")

        return AuditOpinion(
            opinion_type=opinion_type,
            opinion_text=opinion_text,
            qualified_items=qualified_items,
            qualification_reason=qualification_reason,
            key_audit_matters=key_audit_matters,
            confidence=confidence,
        )

    def _classify_opinion_type(self, text: str) -> str:
        """Classify opinion type from text.

        Args:
            text: Opinion text

        Returns:
            Opinion type (적정, 한정, 부정, 의견거절)
        """
        # Check in order of specificity (부정의견 before 한정의견)
        for opinion_type in ["부정의견", "의견거절", "한정의견", "적정의견"]:
            if opinion_type in self.OPINION_KEYWORDS:
                if self._opinion_patterns[opinion_type].search(text):
                    return opinion_type

        return "미분류"

    def _extract_qualified_items(self, text: str) -> list[str]:
        """Extract items subject to qualification.

        Args:
            text: Opinion text

        Returns:
            List of qualified items
        """
        qualified_items = []

        # Common patterns for qualifications (Korean)
        qualification_patterns = [
            r"재고자산[^,.]*에 대하여[^,.]*제외",
            r"수익[^,.]*에 대하여[^,.]*제외",
            r"[^\s]+\s*[^,.*]*제외하고는",
        ]

        for pattern in qualification_patterns:
            matches = re.findall(pattern, text)
            qualified_items.extend(matches)

        return list(set(qualified_items))

    def _extract_qualification_reason(self, text: str) -> Optional[str]:
        """Extract reason for qualification.

        Args:
            text: Opinion text

        Returns:
            Qualification reason or None
        """
        # Look for "왜냐하면" (because), "이유는" (reason)
        reason_patterns = [
            r"(?:왜냐하면|이유는|이는)\s*([^.]+\.)$",
            r"(?:적절히 확인할 수 없었기|감사|검증할 수 없었기|직접|다음의)\s*([^.]+\.)",
        ]

        for pattern in reason_patterns:
            match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return None

    def _extract_key_audit_matters(self, text: str) -> list[KeyAuditMatter]:
        """Extract key audit matters from opinion text.

        Args:
            text: Opinion text

        Returns:
            List of KeyAuditMatter objects
        """
        matters = []

        # Split by common KAM section headers
        kam_patterns = [
            r"감사상\s*핵심사항[^:]*:\s*(.+?)(?=감사상\s*핵심사항|$)",
            r"핵심감사사항\s*(?::|:)\s*(.+?)(?=핵심감사사항|$)",
        ]

        for pattern in kam_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                kam = KeyAuditMatter(
                    title="핵심감사사항",
                    description=match.strip()[:200],  # First 200 chars
                )
                matters.append(kam)

        logger.debug(f"Extracted {len(matters)} key audit matters")
        return matters

    def _calculate_confidence(self, opinion_type: str, text: str) -> float:
        """Calculate confidence score for opinion classification.

        Args:
            opinion_type: Classified opinion type
            text: Opinion text

        Returns:
            Confidence score (0.0 to 1.0)
        """
        confidence = 0.5  # Base confidence

        # Increase if opinion type explicitly mentioned
        if opinion_type in ["적정의견", "부정의견"]:
            if opinion_type in text:
                confidence = 0.95
        elif opinion_type in ["한정의견", "의견거절"]:
            if opinion_type in text:
                confidence = 0.9

        # Adjust based on text length and structure
        if len(text) > 100:
            confidence = min(1.0, confidence + 0.05)

        # Check for going concern warning (affects confidence)
        if any(kw in text for kw in self.GOING_CONCERN_KEYWORDS):
            confidence = min(1.0, confidence + 0.05)

        return round(confidence, 2)

    def detect_going_concern(self, text: str) -> bool:
        """Detect going concern warning in opinion text.

        Args:
            text: Opinion text

        Returns:
            True if going concern warning detected
        """
        for keyword in self.GOING_CONCERN_KEYWORDS:
            if keyword.lower() in text.lower():
                logger.info("Going concern warning detected")
                return True
        return False
