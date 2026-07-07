# Milestone 3: Risk Detection Engine

## Overview

Milestone 3 focuses on implementing an advanced risk detection engine that analyzes parsed audit reports and generates comprehensive risk assessments. This milestone includes financial ratio analysis, trend detection, and machine learning-based anomaly detection.

## Objectives

### 1. Financial Analysis Engine
- Calculate key financial ratios from audit reports
- Analyze financial trends and patterns
- Identify financial distress signals
- Compare against industry benchmarks

### 2. Risk Detection & Scoring
- Aggregate multi-source risk indicators
- Calculate comprehensive risk scores
- Prioritize high-risk companies
- Generate risk alerts and warnings

### 3. Machine Learning Detection (Optional v2)
- Train models on historical audit data
- Detect anomalies in financial patterns
- Predict company failure risk
- Classify companies by risk profile

## Technical Specifications

### Financial Analysis Module

#### Key Financial Ratios

**Liquidity Ratios**
- Current Ratio = Current Assets / Current Liabilities
- Quick Ratio = (Current Assets - Inventory) / Current Liabilities
- Cash Ratio = Cash / Current Liabilities

**Solvency Ratios**
- Debt-to-Equity = Total Debt / Total Equity
- Debt-to-Assets = Total Debt / Total Assets
- Interest Coverage = EBIT / Interest Expense

**Profitability Ratios**
- ROA (Return on Assets) = Net Income / Total Assets
- ROE (Return on Equity) = Net Income / Total Equity
- Net Margin = Net Income / Revenue
- Operating Margin = Operating Income / Revenue

**Efficiency Ratios**
- Asset Turnover = Revenue / Total Assets
- Inventory Turnover = Cost of Goods Sold / Inventory
- Receivables Turnover = Revenue / Accounts Receivable

**Growth Ratios**
- Revenue Growth Rate (YoY %)
- Net Income Growth Rate (YoY %)
- Asset Growth Rate (YoY %)

#### Data Models

```python
@dataclass
class FinancialRatios:
    """Calculated financial ratios"""
    report_id: str
    period_end: str
    
    # Liquidity
    current_ratio: Optional[float]
    quick_ratio: Optional[float]
    cash_ratio: Optional[float]
    
    # Solvency
    debt_to_equity: Optional[float]
    debt_to_assets: Optional[float]
    interest_coverage: Optional[float]
    
    # Profitability
    roa: Optional[float]
    roe: Optional[float]
    net_margin: Optional[float]
    operating_margin: Optional[float]
    
    # Efficiency
    asset_turnover: Optional[float]
    inventory_turnover: Optional[float]
    receivables_turnover: Optional[float]
    
    # Growth
    revenue_growth: Optional[float]
    income_growth: Optional[float]
    asset_growth: Optional[float]
    
    calculated_at: datetime

@dataclass
class FinancialTrend:
    """Financial trend over multiple periods"""
    corp_code: str
    metric: str  # e.g., "debt_to_equity"
    periods: List[str]  # dates
    values: List[float]
    trend_direction: str  # up, down, stable
    trend_strength: float  # 0.0-1.0
    alert: bool
```

### Risk Detection Module

#### Risk Scoring Framework

**Multi-Factor Risk Score**

```
Overall Risk = weighted_sum(
    financial_risk * 0.40,
    audit_opinion_risk * 0.25,
    emphasis_matter_risk * 0.20,
    going_concern_risk * 0.15
)

Range: 0.0 (low risk) to 1.0 (high risk)
```

#### Risk Categories

**1. Financial Risk (0.0-1.0)**
- Liquidity Risk: Based on current/quick ratios
- Solvency Risk: Based on debt ratios
- Profitability Risk: Based on margins and ROA/ROE
- Growth Risk: Declining revenues or income

**2. Audit Opinion Risk (0.0-1.0)**
- 적정의견 (Clean): 0.0-0.1 (low)
- 한정의견 (Qualified): 0.4-0.6 (medium)
- 부정의견 (Adverse): 0.7-0.9 (high)
- 의견거절 (Disclaimer): 0.9-1.0 (critical)

**3. Emphasis Matter Risk (0.0-1.0)**
- No matters: 0.0
- Low-risk matters: 0.2-0.4
- Medium-risk matters: 0.4-0.6
- High-risk matters: 0.6-0.8
- Critical matters (going concern): 0.8-1.0

**4. Going Concern Risk (0.0-1.0)**
- No warning: 0.0
- Management discussion: 0.3
- Auditor concern: 0.6
- Critical warning: 0.9-1.0

#### Data Models

```python
@dataclass
class RiskAssessment:
    """Comprehensive risk assessment"""
    corp_code: str
    corp_name: str
    assessment_date: str
    
    # Component scores
    financial_risk: float  # 0.0-1.0
    audit_opinion_risk: float  # 0.0-1.0
    emphasis_matter_risk: float  # 0.0-1.0
    going_concern_risk: float  # 0.0-1.0
    
    # Overall score
    overall_risk: float  # 0.0-1.0
    risk_level: str  # Low, Medium, High, Critical
    
    # Details
    primary_risks: List[str]  # Top 3 risks
    key_metrics: Dict[str, float]  # Important ratios
    trend_alerts: List[str]  # Concerning trends
    recommendations: List[str]  # Action items
    
    calculated_at: datetime

@dataclass
class RiskAlert:
    """Risk alert for critical findings"""
    corp_code: str
    alert_type: str  # going_concern, liquidity, solvency, etc.
    severity: str  # critical, high, medium, low
    message: str
    metric_value: Optional[float]
    threshold: Optional[float]
    created_at: datetime
```

#### Risk Level Thresholds

```
Low:       0.0 - 0.3
Medium:    0.3 - 0.6
High:      0.6 - 0.8
Critical:  0.8 - 1.0
```

### Trend Detection Module

#### Time Series Analysis

- **Trend Direction**: Up, Down, Stable
- **Trend Strength**: 0.0 (weak) to 1.0 (strong)
- **Volatility**: Measure of fluctuation
- **Anomalies**: Detect outliers in patterns

#### Trend Detection Methods

```python
# Simple Linear Regression
# Moving Average Analysis
# Year-over-Year Growth Rates
# Volatility Calculation (Std Dev)
```

#### Alert Triggers

**Liquidity Alerts**
- Current ratio < 1.0 (critical)
- Current ratio < 1.5 (high)
- Quick ratio < 0.8 (medium)

**Solvency Alerts**
- Debt-to-Equity > 2.0 (critical)
- Debt-to-Equity > 1.5 (high)
- Debt-to-Assets > 0.7 (medium)

**Profitability Alerts**
- ROA < 0% (loss) (critical)
- Net Margin < 0% (medium)
- Declining margins (trend) (medium)

**Growth Alerts**
- Revenue decline YoY > 20% (high)
- Revenue decline YoY > 10% (medium)
- Consistent negative growth (medium)

**Going Concern Alerts**
- Going concern warning (critical)
- Management restructuring plan (high)
- Liquidity pressure + losses (high)

## Implementation Plan

### Phase 1: Financial Analysis

- [ ] Create `src/analyzer/financial_analyzer.py`
  - [ ] Calculate all standard ratios
  - [ ] Handle missing data gracefully
  - [ ] Validate calculations
  - [ ] Support multiple fiscal year formats

- [ ] Create `src/analyzer/trend_analyzer.py`
  - [ ] Analyze trends over 3-5 years
  - [ ] Detect inflection points
  - [ ] Calculate trend metrics
  - [ ] Generate trend visualizations

### Phase 2: Risk Detection

- [ ] Create `src/analyzer/risk_calculator.py`
  - [ ] Aggregate multi-source risks
  - [ ] Calculate weighted scores
  - [ ] Classify risk levels
  - [ ] Generate risk alerts

- [ ] Create `src/analyzer/alert_engine.py`
  - [ ] Define alert thresholds
  - [ ] Trigger alerts on conditions
  - [ ] Track alert history
  - [ ] Prioritize alerts by severity

### Phase 3: Integration & Testing

- [ ] Create `src/analyzer/analyzer_pipeline.py`
  - [ ] Coordinate all analysis modules
  - [ ] Execute in proper sequence
  - [ ] Handle errors gracefully
  - [ ] Return comprehensive report

- [ ] Comprehensive testing
  - [ ] Unit tests for each module
  - [ ] Integration tests
  - [ ] Accuracy validation
  - [ ] Performance benchmarks

## Dependencies

```
numpy              # Numerical computations
pandas             # Time series analysis
scipy              # Statistical functions
scikit-learn       # ML for anomaly detection (optional)
```

## Data Flow

```
Parsed Audit Report
    ↓
[Financial Analyzer] → Financial Ratios
    ↓
[Trend Analyzer] → Historical Trends
    ↓
[Risk Calculator] → Risk Scores
    ↓
[Alert Engine] → Risk Alerts
    ↓
[Analyzer Pipeline] → RiskAssessment
    ↓
Database/Dashboard
```

## Testing Strategy

- Unit tests for ratio calculations (verify against known values)
- Integration tests with sample data
- Accuracy validation against industry benchmarks
- Performance testing (handle 1000+ companies efficiently)
- Edge cases (missing data, zero values, extreme values)

## Branch

`feature/risk-detection`

## Deliverables

- [x] Financial ratio calculator
- [x] Trend analyzer
- [x] Risk scoring engine
- [ ] Alert engine implementation
- [ ] Analyzer pipeline integration
- [ ] Unit tests (>80% coverage)
- [ ] Sample risk reports
- [ ] Documentation and usage guide

## Schedule

Estimated completion: 2-3 weeks

## Notes

- Focus on accuracy of financial calculations first
- Build in flexibility for custom ratio definitions
- Consider industry-specific benchmarks in v2
- Machine learning component is optional enhancement
- Type hints required throughout
- Comprehensive error handling for missing/invalid data
