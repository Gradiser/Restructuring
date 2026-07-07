"""Trend analyzer for detecting financial trends and anomalies.

Analyzes financial metrics over time to identify trends, calculate growth rates,
and detect anomalies or concerning patterns.
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class FinancialTrend:
    """Financial trend over multiple periods."""

    corp_code: str
    metric: str  # e.g., "debt_to_equity", "current_ratio"
    periods: list[str]  # dates in chronological order
    values: list[float]  # corresponding values
    trend_direction: str  # "up", "down", "stable"
    trend_strength: float  # 0.0-1.0 (confidence)
    volatility: float  # Standard deviation
    anomalies: list[int] = None  # Indices of anomalous values
    alert: bool = False
    alert_message: Optional[str] = None


class TrendAnalyzer:
    """Analyzer for financial trends and time series data."""

    # Volatility thresholds
    HIGH_VOLATILITY_THRESHOLD = 0.5
    MODERATE_VOLATILITY_THRESHOLD = 0.2

    # Anomaly detection threshold (standard deviations)
    ANOMALY_THRESHOLD = 2.0

    def __init__(self) -> None:
        """Initialize trend analyzer."""
        pass

    def analyze_trend(
        self,
        corp_code: str,
        metric: str,
        periods: list[str],
        values: list[float],
    ) -> FinancialTrend:
        """Analyze trend in financial metric over time.

        Args:
            corp_code: Corporation code
            metric: Metric name
            periods: List of period dates (chronological order)
            values: List of corresponding values

        Returns:
            FinancialTrend object
        """
        if len(periods) != len(values):
            logger.error("Periods and values length mismatch")
            raise ValueError("Periods and values must have same length")

        if len(values) < 2:
            logger.warning(f"Insufficient data for trend analysis: {len(values)} values")
            return FinancialTrend(
                corp_code=corp_code,
                metric=metric,
                periods=periods,
                values=values,
                trend_direction="unknown",
                trend_strength=0.0,
                volatility=0.0,
            )

        # Calculate trend direction
        trend_direction, trend_strength = self._calculate_trend(values)

        # Calculate volatility
        volatility = self._calculate_volatility(values)

        # Detect anomalies
        anomalies = self._detect_anomalies(values)

        # Generate alert if needed
        alert, alert_message = self._generate_trend_alert(
            metric, trend_direction, trend_strength, volatility, anomalies
        )

        trend = FinancialTrend(
            corp_code=corp_code,
            metric=metric,
            periods=periods,
            values=values,
            trend_direction=trend_direction,
            trend_strength=trend_strength,
            volatility=volatility,
            anomalies=anomalies,
            alert=alert,
            alert_message=alert_message,
        )

        logger.info(
            f"Analyzed trend for {corp_code}.{metric}: {trend_direction} "
            f"(strength={trend_strength:.2f}, volatility={volatility:.2f})"
        )
        return trend

    def _calculate_trend(self, values: list[float]) -> tuple[str, float]:
        """Calculate trend direction and strength using linear regression.

        Args:
            values: List of values in chronological order

        Returns:
            Tuple of (trend_direction, trend_strength)
        """
        if len(values) < 2:
            return "unknown", 0.0

        try:
            values_array = np.array(values, dtype=float)
            x = np.arange(len(values))

            # Calculate linear regression
            coefficients = np.polyfit(x, values_array, 1)
            slope = coefficients[0]

            # Determine direction
            if slope > 0.001:
                direction = "up"
            elif slope < -0.001:
                direction = "down"
            else:
                direction = "stable"

            # Calculate trend strength (R-squared)
            poly = np.poly1d(coefficients)
            predicted = poly(x)
            ss_res = np.sum((values_array - predicted) ** 2)
            ss_tot = np.sum((values_array - np.mean(values_array)) ** 2)

            if ss_tot == 0:
                strength = 0.0
            else:
                strength = 1 - (ss_res / ss_tot)
                strength = max(0.0, min(1.0, strength))

            return direction, round(strength, 3)

        except Exception as e:
            logger.error(f"Error calculating trend: {e}")
            return "unknown", 0.0

    def _calculate_volatility(self, values: list[float]) -> float:
        """Calculate volatility (standard deviation) of values.

        Args:
            values: List of values

        Returns:
            Volatility score (normalized)
        """
        if len(values) < 2:
            return 0.0

        try:
            values_array = np.array(values, dtype=float)
            mean_value = np.mean(values_array)

            if mean_value == 0:
                return 0.0

            # Calculate coefficient of variation (CV)
            std_dev = np.std(values_array)
            cv = std_dev / abs(mean_value) if mean_value != 0 else 0.0

            # Normalize CV to 0-1 range
            volatility = min(1.0, cv / 2.0)  # Assume 200% CV = max volatility
            return round(volatility, 3)

        except Exception as e:
            logger.error(f"Error calculating volatility: {e}")
            return 0.0

    def _detect_anomalies(
        self, values: list[float], threshold: float = ANOMALY_THRESHOLD
    ) -> list[int]:
        """Detect anomalous values using z-score method.

        Args:
            values: List of values
            threshold: Z-score threshold for anomaly

        Returns:
            List of indices of anomalous values
        """
        if len(values) < 3:
            return []

        try:
            values_array = np.array(values, dtype=float)
            mean_value = np.mean(values_array)
            std_dev = np.std(values_array)

            if std_dev == 0:
                return []

            # Calculate z-scores
            z_scores = np.abs((values_array - mean_value) / std_dev)

            # Find anomalies
            anomalies = list(np.where(z_scores > threshold)[0])
            return anomalies

        except Exception as e:
            logger.error(f"Error detecting anomalies: {e}")
            return []

    def _generate_trend_alert(
        self,
        metric: str,
        trend_direction: str,
        trend_strength: float,
        volatility: float,
        anomalies: list[int],
    ) -> tuple[bool, Optional[str]]:
        """Generate alert based on trend analysis.

        Args:
            metric: Metric name
            trend_direction: Trend direction (up/down/stable)
            trend_strength: Trend strength (0.0-1.0)
            volatility: Volatility level (0.0-1.0)
            anomalies: List of anomaly indices

        Returns:
            Tuple of (alert_present, alert_message)
        """
        alerts = []

        # Check for strong negative trend
        if (
            trend_direction == "down"
            and trend_strength > 0.7
            and metric
            in ["current_ratio", "roa", "revenue_growth"]
        ):
            alerts.append(f"Strong declining trend in {metric}")

        # Check for high volatility
        if volatility > self.HIGH_VOLATILITY_THRESHOLD:
            alerts.append(f"High volatility in {metric}")

        # Check for anomalies
        if anomalies:
            alerts.append(f"Anomalous values detected in {metric}")

        if alerts:
            message = "; ".join(alerts)
            return True, message
        else:
            return False, None

    def calculate_growth_rate(
        self, current_value: float, prior_value: float
    ) -> Optional[float]:
        """Calculate year-over-year growth rate.

        Args:
            current_value: Current period value
            prior_value: Prior period value

        Returns:
            Growth rate as percentage or None
        """
        if prior_value == 0 or np.isnan(prior_value):
            return None

        try:
            growth = ((current_value - prior_value) / abs(prior_value)) * 100
            return round(growth, 2)
        except (ValueError, TypeError):
            return None

    def calculate_compound_growth_rate(
        self, values: list[float], periods: int
    ) -> Optional[float]:
        """Calculate compound annual growth rate (CAGR).

        Args:
            values: List of values (start and end)
            periods: Number of periods

        Returns:
            CAGR as percentage or None
        """
        if len(values) < 2 or periods <= 0:
            return None

        start_value = values[0]
        end_value = values[-1]

        if start_value <= 0:
            return None

        try:
            cagr = (((end_value / start_value) ** (1 / periods)) - 1) * 100
            return round(cagr, 2)
        except (ValueError, TypeError, ZeroDivisionError):
            return None
