"""Risk calculator for comprehensive risk assessment and scoring.

Aggregates multi-source risk indicators (financial, audit opinion, emphasis matters,
going concern) to calculate overall risk scores and generate risk alerts.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class RiskAssessment:
    """Comprehensive risk assessment."""

    corp_code: str
    corp_name: str
    assessment_date: str

    # Component scores (0.0-1.0)
    financial_risk: float
    audit_opinion_risk: float
    emphasis_matter_risk: float
    going_concern_risk: float

    # Overall score
    overall_risk: float
    risk_level: str  # Low, Medium, High, Critical

    # Details
    primary_risks: list[str] = field(default_factory=list)
    key_metrics: dict[str, float] = field(default_factory=dict)
    trend_alerts: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)

    calculated_at: datetime = None

    def __post_init__(self) -> None:
        """Initialize calculated_at timestamp."""
        if self.calculated_at is None:
            self.calculated_at = datetime.now()


@dataclass
class RiskAlert:
    """Risk alert for critical findings."""

    corp_code: str
    alert_type: str  # going_concern, liquidity, solvency, etc.
    severity: str  # critical, high, medium, low
    message: str
    metric_value: Optional[float] = None
    threshold: Optional[float] = None
    created_at: datetime = None

    def __post_init__(self) -> None:
        """Initialize created_at timestamp."""
        if self.created_at is None:
            self.created_at = datetime.now()


class RiskCalculator:
    """Calculator for comprehensive risk assessment."""

    # Risk weighting scheme
    WEIGHTS = {
        "financial_risk": 0.40,
        "audit_opinion_risk": 0.25,
        "emphasis_matter_risk": 0.20,
        "going_concern_risk": 0.15,
    }

    # Risk level thresholds
    RISK_THRESHOLDS = {
        "low": (0.0, 0.3),
        "medium": (0.3, 0.6),
        "high": (0.6, 0.8),
        "critical": (0.8, 1.0),
    }

    def __init__(self) -> None:
        """Initialize risk calculator."""
        pass

    def calculate_overall_risk(
        self,
        corp_code: str,
        corp_name: str,
        assessment_date: str,
        financial_risk: float,
        audit_opinion_risk: float,
        emphasis_matter_risk: float,
        going_concern_risk: float,
    ) -> RiskAssessment:
        """Calculate overall risk assessment.

        Args:
            corp_code: Corporation code
            corp_name: Company name
            assessment_date: Assessment date
            financial_risk: Financial risk score (0.0-1.0)
            audit_opinion_risk: Audit opinion risk score (0.0-1.0)
            emphasis_matter_risk: Emphasis matter risk score (0.0-1.0)
            going_concern_risk: Going concern risk score (0.0-1.0)

        Returns:
            RiskAssessment object
        """
        # Validate inputs
        for risk_score in [
            financial_risk,
            audit_opinion_risk,
            emphasis_matter_risk,
            going_concern_risk,
        ]:
            if not 0.0 <= risk_score <= 1.0:
                logger.warning(f"Risk score out of range: {risk_score}")

        # Calculate weighted overall risk
        overall_risk = (
            financial_risk * self.WEIGHTS["financial_risk"]
            + audit_opinion_risk * self.WEIGHTS["audit_opinion_risk"]
            + emphasis_matter_risk * self.WEIGHTS["emphasis_matter_risk"]
            + going_concern_risk * self.WEIGHTS["going_concern_risk"]
        )

        # Ensure within bounds
        overall_risk = min(1.0, max(0.0, overall_risk))

        # Classify risk level
        risk_level = self._classify_risk_level(overall_risk)

        # Identify primary risks
        primary_risks = self._identify_primary_risks(
            financial_risk,
            audit_opinion_risk,
            emphasis_matter_risk,
            going_concern_risk,
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(
            risk_level, primary_risks
        )

        assessment = RiskAssessment(
            corp_code=corp_code,
            corp_name=corp_name,
            assessment_date=assessment_date,
            financial_risk=round(financial_risk, 3),
            audit_opinion_risk=round(audit_opinion_risk, 3),
            emphasis_matter_risk=round(emphasis_matter_risk, 3),
            going_concern_risk=round(going_concern_risk, 3),
            overall_risk=round(overall_risk, 3),
            risk_level=risk_level,
            primary_risks=primary_risks,
            recommendations=recommendations,
        )

        logger.info(
            f"Calculated overall risk for {corp_code}: {overall_risk:.3f} ({risk_level})"
        )
        return assessment

    def _classify_risk_level(self, overall_risk: float) -> str:
        """Classify risk level from score.

        Args:
            overall_risk: Overall risk score (0.0-1.0)

        Returns:
            Risk level string
        """
        for level, (lower, upper) in self.RISK_THRESHOLDS.items():
            if lower <= overall_risk < upper:
                return level.capitalize()
        return "Critical"

    def _identify_primary_risks(
        self,
        financial_risk: float,
        audit_opinion_risk: float,
        emphasis_matter_risk: float,
        going_concern_risk: float,
    ) -> list[str]:
        """Identify primary risk factors.

        Args:
            financial_risk: Financial risk score
            audit_opinion_risk: Audit opinion risk score
            emphasis_matter_risk: Emphasis matter risk score
            going_concern_risk: Going concern risk score

        Returns:
            List of primary risks (max 3)
        """
        risks = []

        # Create risk items with scores
        risk_items = [
            ("Financial Distress", financial_risk),
            ("Audit Qualification", audit_opinion_risk),
            ("Emphasis Matters", emphasis_matter_risk),
            ("Going Concern Warning", going_concern_risk),
        ]

        # Sort by score (descending)
        risk_items.sort(key=lambda x: x[1], reverse=True)

        # Select top 3 risks with score > 0.3
        for risk_name, score in risk_items[:3]:
            if score > 0.3:
                risks.append(f"{risk_name} ({score:.1%})")

        return risks if risks else ["Low Risk"]

    def _generate_recommendations(
        self, risk_level: str, primary_risks: list[str]
    ) -> list[str]:
        """Generate recommendations based on risk assessment.

        Args:
            risk_level: Risk level classification
            primary_risks: List of primary risks

        Returns:
            List of recommendations
        """
        recommendations = []

        if risk_level == "Critical":
            recommendations.extend(
                [
                    "Immediate review of financial statements required",
                    "Contact company for clarification on critical issues",
                    "Monitor for bankruptcy or restructuring filings",
                ]
            )

        elif risk_level == "High":
            recommendations.extend(
                [
                    "Schedule management discussion",
                    "Review detailed audit findings",
                    "Monitor quarterly reports closely",
                ]
            )

        elif risk_level == "Medium":
            recommendations.extend(
                [
                    "Review audit opinion and key audit matters",
                    "Monitor trends in key financial ratios",
                ]
            )

        else:  # Low
            recommendations.extend(
                [
                    "Standard monitoring procedures",
                    "Annual review recommended",
                ]
            )

        # Add specific recommendations based on primary risks
        if any("Going Concern" in risk for risk in primary_risks):
            recommendations.insert(
                0, "Priority: Assess going concern implications"
            )

        if any("Financial" in risk for risk in primary_risks):
            recommendations.insert(0, "Priority: Review liquidity and solvency")

        return recommendations

    def calculate_financial_risk(
        self,
        current_ratio: Optional[float] = None,
        debt_to_equity: Optional[float] = None,
        roa: Optional[float] = None,
        revenue_growth: Optional[float] = None,
    ) -> float:
        """Calculate financial risk score from key metrics.

        Args:
            current_ratio: Current ratio (liquidity)
            debt_to_equity: Debt-to-equity ratio (solvency)
            roa: Return on assets (profitability)
            revenue_growth: Revenue growth rate (growth)

        Returns:
            Financial risk score (0.0-1.0)
        """
        risk_scores = []

        # Liquidity risk
        if current_ratio is not None:
            if current_ratio < 1.0:
                risk_scores.append(0.9)
            elif current_ratio < 1.5:
                risk_scores.append(0.7)
            elif current_ratio < 2.0:
                risk_scores.append(0.4)
            else:
                risk_scores.append(0.1)

        # Solvency risk
        if debt_to_equity is not None:
            if debt_to_equity > 2.0:
                risk_scores.append(0.9)
            elif debt_to_equity > 1.5:
                risk_scores.append(0.7)
            elif debt_to_equity > 1.0:
                risk_scores.append(0.4)
            else:
                risk_scores.append(0.1)

        # Profitability risk
        if roa is not None:
            if roa < 0:
                risk_scores.append(0.9)
            elif roa < 0.02:
                risk_scores.append(0.7)
            elif roa < 0.05:
                risk_scores.append(0.4)
            else:
                risk_scores.append(0.1)

        # Growth risk
        if revenue_growth is not None:
            if revenue_growth < -20:
                risk_scores.append(0.9)
            elif revenue_growth < -10:
                risk_scores.append(0.7)
            elif revenue_growth < 0:
                risk_scores.append(0.4)
            else:
                risk_scores.append(0.1)

        # Average risk scores
        if risk_scores:
            return round(sum(risk_scores) / len(risk_scores), 3)
        else:
            return 0.5  # Default if no data

    def calculate_opinion_risk(self, opinion_type: str) -> float:
        """Calculate audit opinion risk.

        Args:
            opinion_type: Audit opinion type

        Returns:
            Opinion risk score (0.0-1.0)
        """
        opinion_risks = {
            "적정의견": 0.05,  # Clean opinion - very low risk
            "clean opinion": 0.05,
            "unqualified": 0.05,
            "한정의견": 0.50,  # Qualified - medium risk
            "qualified opinion": 0.50,
            "except for": 0.50,
            "부정의견": 0.80,  # Adverse - high risk
            "adverse opinion": 0.80,
            "does not present": 0.80,
            "의견거절": 0.95,  # Disclaimer - critical risk
            "disclaimer": 0.95,
            "unable to obtain": 0.95,
        }

        risk = opinion_risks.get(opinion_type.lower(), 0.5)
        logger.info(f"Opinion risk for '{opinion_type}': {risk}")
        return risk

    def generate_alert(
        self,
        corp_code: str,
        alert_type: str,
        severity: str,
        message: str,
        metric_value: Optional[float] = None,
        threshold: Optional[float] = None,
    ) -> RiskAlert:
        """Generate a risk alert.

        Args:
            corp_code: Corporation code
            alert_type: Type of alert
            severity: Alert severity
            message: Alert message
            metric_value: Actual metric value
            threshold: Threshold value

        Returns:
            RiskAlert object
        """
        alert = RiskAlert(
            corp_code=corp_code,
            alert_type=alert_type,
            severity=severity,
            message=message,
            metric_value=metric_value,
            threshold=threshold,
        )

        logger.warning(f"Generated {severity} alert for {corp_code}: {message}")
        return alert
