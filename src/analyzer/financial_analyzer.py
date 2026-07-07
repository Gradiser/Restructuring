"""Financial analyzer for calculating key financial ratios and metrics.

Calculates liquidity, solvency, profitability, efficiency, and growth ratios
from parsed audit report financial statements.
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class FinancialRatios:
    """Calculated financial ratios."""

    report_id: str
    period_end: str

    # Liquidity Ratios
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None
    cash_ratio: Optional[float] = None

    # Solvency Ratios
    debt_to_equity: Optional[float] = None
    debt_to_assets: Optional[float] = None
    interest_coverage: Optional[float] = None

    # Profitability Ratios
    roa: Optional[float] = None
    roe: Optional[float] = None
    net_margin: Optional[float] = None
    operating_margin: Optional[float] = None

    # Efficiency Ratios
    asset_turnover: Optional[float] = None
    inventory_turnover: Optional[float] = None
    receivables_turnover: Optional[float] = None

    # Growth Ratios
    revenue_growth: Optional[float] = None
    income_growth: Optional[float] = None
    asset_growth: Optional[float] = None

    calculated_at: datetime = None

    def __post_init__(self) -> None:
        """Initialize calculated_at timestamp."""
        if self.calculated_at is None:
            self.calculated_at = datetime.now()


class FinancialAnalyzer:
    """Analyzer for financial ratios and metrics."""

    # Safe division threshold
    EPSILON = 1e-10

    def __init__(self) -> None:
        """Initialize financial analyzer."""
        pass

    def calculate_ratios(
        self,
        report_id: str,
        period_end: str,
        financial_data: dict,
    ) -> FinancialRatios:
        """Calculate all financial ratios from statement data.

        Args:
            report_id: Report identifier
            period_end: Period end date
            financial_data: Dictionary with financial statement values

        Returns:
            FinancialRatios object with calculated metrics
        """
        ratios = FinancialRatios(report_id=report_id, period_end=period_end)

        # Extract key values from data
        current_assets = financial_data.get("current_assets", 0)
        current_liabilities = financial_data.get("current_liabilities", 0)
        inventory = financial_data.get("inventory", 0)
        cash = financial_data.get("cash", 0)

        total_debt = financial_data.get("total_debt", 0)
        total_equity = financial_data.get("total_equity", 0)
        total_assets = financial_data.get("total_assets", 0)
        interest_expense = financial_data.get("interest_expense", 0)

        revenue = financial_data.get("revenue", 0)
        operating_income = financial_data.get("operating_income", 0)
        net_income = financial_data.get("net_income", 0)
        ebit = financial_data.get("ebit", 0)

        cost_of_goods_sold = financial_data.get("cogs", 0)
        accounts_receivable = financial_data.get("accounts_receivable", 0)

        # Calculate Liquidity Ratios
        ratios.current_ratio = self._safe_divide(current_assets, current_liabilities)
        ratios.quick_ratio = self._safe_divide(
            current_assets - inventory, current_liabilities
        )
        ratios.cash_ratio = self._safe_divide(cash, current_liabilities)

        # Calculate Solvency Ratios
        ratios.debt_to_equity = self._safe_divide(total_debt, total_equity)
        ratios.debt_to_assets = self._safe_divide(total_debt, total_assets)
        ratios.interest_coverage = self._safe_divide(ebit, interest_expense)

        # Calculate Profitability Ratios
        ratios.roa = self._safe_divide(net_income, total_assets)
        ratios.roe = self._safe_divide(net_income, total_equity)
        ratios.net_margin = self._safe_divide(net_income, revenue)
        ratios.operating_margin = self._safe_divide(operating_income, revenue)

        # Calculate Efficiency Ratios
        ratios.asset_turnover = self._safe_divide(revenue, total_assets)
        ratios.inventory_turnover = self._safe_divide(cost_of_goods_sold, inventory)
        ratios.receivables_turnover = self._safe_divide(revenue, accounts_receivable)

        logger.info(f"Calculated ratios for report {report_id}")
        return ratios

    def _safe_divide(self, numerator: float, denominator: float) -> Optional[float]:
        """Safely divide two numbers, handling division by zero.

        Args:
            numerator: Numerator value
            denominator: Denominator value

        Returns:
            Result of division or None if denominator is zero/invalid
        """
        if abs(denominator) < self.EPSILON:
            return None
        try:
            result = numerator / denominator
            return round(result, 4)
        except (ValueError, TypeError):
            return None

    def assess_liquidity(self, ratios: FinancialRatios) -> tuple[str, float]:
        """Assess liquidity based on ratios.

        Args:
            ratios: FinancialRatios object

        Returns:
            Tuple of (assessment_level, risk_score)
        """
        if ratios.current_ratio is None:
            return "unknown", 0.5

        # Thresholds
        if ratios.current_ratio < 1.0:
            return "critical", 0.9
        elif ratios.current_ratio < 1.5:
            return "high", 0.7
        elif ratios.current_ratio < 2.0:
            return "medium", 0.4
        else:
            return "low", 0.1

    def assess_solvency(self, ratios: FinancialRatios) -> tuple[str, float]:
        """Assess solvency based on debt ratios.

        Args:
            ratios: FinancialRatios object

        Returns:
            Tuple of (assessment_level, risk_score)
        """
        if ratios.debt_to_equity is None:
            return "unknown", 0.5

        # Thresholds
        if ratios.debt_to_equity > 2.0:
            return "critical", 0.9
        elif ratios.debt_to_equity > 1.5:
            return "high", 0.7
        elif ratios.debt_to_equity > 1.0:
            return "medium", 0.4
        else:
            return "low", 0.1

    def assess_profitability(self, ratios: FinancialRatios) -> tuple[str, float]:
        """Assess profitability based on margins.

        Args:
            ratios: FinancialRatios object

        Returns:
            Tuple of (assessment_level, risk_score)
        """
        if ratios.roa is None:
            return "unknown", 0.5

        # Thresholds
        if ratios.roa < 0:
            return "critical", 0.9
        elif ratios.roa < 0.02:
            return "high", 0.7
        elif ratios.roa < 0.05:
            return "medium", 0.4
        else:
            return "low", 0.1

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
        if prior_value == 0:
            return None
        try:
            growth = ((current_value - prior_value) / abs(prior_value)) * 100
            return round(growth, 2)
        except (ValueError, TypeError):
            return None
