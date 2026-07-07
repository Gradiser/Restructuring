# Milestone 2: Advanced Parsing

## Overview

Milestone 2 focuses on implementing comprehensive document parsing capabilities to extract structured audit data from DART documents. This milestone includes XML parsing, audit opinion parsing, and emphasis/key matter detection.

## Objectives

### 1. XML Parser
- Parse DART XML audit reports
- Extract structured financial and audit data
- Handle various report formats and versions
- Validate XML structure and content

### 2. Opinion Parser
- Extract audit opinion (적정의견, 한정의견, 부정의견, 의견거절)
- Parse key audit matters (감사상 핵심사항)
- Extract auditor information
- Track audit quality indicators

### 3. Emphasis Parser
- Identify emphasis of matter paragraphs
- Extract emphasis context and significance
- Detect going concern warnings
- Extract other significant audit findings

## Technical Specifications

### XML Parser

#### Objectives
- Parse DART XML documents (감사보고서)
- Extract structured sections:
  - Company information
  - Audit period and dates
  - Financial statements summary
  - Audit opinion
  - Key audit matters
  - Audit risk disclosures

#### Data Structures

```python
@dataclass
class AuditReport:
    """Parsed audit report data"""
    corp_code: str
    corp_name: str
    filing_date: str
    period_start: str
    period_end: str
    audit_firm: str
    audit_opinion: str  # 적정, 한정, 부정, 의견거절
    key_audit_matters: List[str]
    report_content: str
    parsed_at: datetime

@dataclass
class FinancialStatement:
    """Extracted financial statement data"""
    report_id: str
    statement_type: str  # 재무상태표, 손익계산서, etc.
    period_end: str
    data: Dict[str, Any]

@dataclass
class AuditFinding:
    """Audit findings and disclosures"""
    report_id: str
    category: str
    description: str
    severity: str  # major, moderate, minor
    confidence: float
```

#### DART XML Structure (Expected)

```xml
<?xml version="1.0" encoding="utf-8"?>
<AUDIT_REPORT>
  <COMPANY>
    <CORP_CODE>...</CORP_CODE>
    <CORP_NAME>...</CORP_NAME>
  </COMPANY>
  <AUDIT_PERIOD>
    <START_DATE>...</START_DATE>
    <END_DATE>...</END_DATE>
  </AUDIT_PERIOD>
  <AUDITOR>
    <FIRM_NAME>...</FIRM_NAME>
    <REPRESENTATIVE>...</REPRESENTATIVE>
  </AUDITOR>
  <OPINION>
    <TYPE>적정의견|한정의견|부정의견|의견거절</TYPE>
    <DESCRIPTION>...</DESCRIPTION>
  </OPINION>
  <KEY_MATTERS>
    <MATTER>...</MATTER>
    ...
  </KEY_MATTERS>
  <STATEMENTS>
    <STATEMENT type="...">...</STATEMENT>
    ...
  </STATEMENTS>
</AUDIT_REPORT>
```

#### Implementation Plan

- [ ] Create `src/parser/xml_parser.py`
  - [ ] XMLParser class with LXML
  - [ ] Validate XML schema
  - [ ] Extract company information
  - [ ] Extract audit period
  - [ ] Extract auditor details
  - [ ] Extract financial statements
  - [ ] Error handling for malformed XML
  - [ ] Support multiple DART XML versions

- [ ] Testing
  - [ ] Unit tests with sample DART XML files
  - [ ] Edge case handling
  - [ ] Performance tests on large documents
  - [ ] Error recovery tests

### Opinion Parser

#### Objectives
- Extract audit opinion and classification
- Parse key audit matters (KAM) / 감사상 핵심사항
- Identify opinion modifiers and disclaimers
- Extract auditor details

#### Audit Opinion Types
- **적정의견 (Unqualified)** - Clean opinion
- **한정의견 (Qualified)** - Qualified opinion with exceptions
- **부정의견 (Adverse)** - Adverse opinion
- **의견거절 (Disclaimer)** - Disclaimer of opinion

#### Data Structures

```python
@dataclass
class AuditOpinion:
    """Structured audit opinion"""
    opinion_type: str  # 적정, 한정, 부정, 의견거절
    opinion_text: str
    qualified_items: List[str]  # If qualified opinion
    qualification_reason: Optional[str]
    key_audit_matters: List[KeyAuditMatter]
    confidence: float

@dataclass
class KeyAuditMatter:
    """Key audit matter (감사상 핵심사항)"""
    title: str
    description: str
    scope: str
    procedures: str
    audit_response: str
```

#### Implementation Plan

- [ ] Create `src/parser/opinion_parser.py`
  - [ ] OpinionParser class
  - [ ] Opinion type classification (regex + ML if needed)
  - [ ] Extract qualification reasons
  - [ ] Parse KAM sections
  - [ ] Extract auditor information
  - [ ] Handle multiple language variations

- [ ] NLP/Text Processing
  - [ ] Use BeautifulSoup4 for HTML if needed
  - [ ] Regex patterns for opinion keywords
  - [ ] Extract structured audit findings
  - [ ] Confidence scoring

- [ ] Testing
  - [ ] Opinion classification accuracy
  - [ ] KAM extraction tests
  - [ ] Variation handling tests
  - [ ] Mock audit opinion data

### Emphasis Parser

#### Objectives
- Detect emphasis of matter paragraphs (강조사항)
- Extract going concern warnings (계속기업의정성)
- Identify other significant disclosures
- Assess severity and importance

#### Data Structures

```python
@dataclass
class EmphasisMatter:
    """Emphasis of matter disclosure"""
    category: str  # going_concern, emphasis, subsequent_event, etc.
    title: str
    description: str
    severity: str  # critical, high, medium, low
    keywords: List[str]
    confidence: float

@dataclass
class GoingConcernWarning:
    """Going concern assessment"""
    warning_present: bool
    severity: str  # critical, high, medium, low
    reason: str
    management_response: Optional[str]
    auditor_assessment: Optional[str]
```

#### Key Audit Matters to Detect
- **Going Concern (계속기업)** - Company's ability to continue operations
- **Related Party Transactions** - 관련자거래
- **Significant Estimates** - 중요한회계추정
- **Revenue Recognition** - 수익인식
- **Impairment Issues** - 손상차손
- **Subsequent Events** - 보고기간후사건
- **Debt Restructuring** - 채무재조정
- **Litigation/Disputes** - 소송분쟁

#### Implementation Plan

- [ ] Create `src/parser/emphasis_parser.py`
  - [ ] EmphasisParser class
  - [ ] Keyword detection system
  - [ ] Going concern detection
  - [ ] Category classification
  - [ ] Severity assessment
  - [ ] Confidence scoring

- [ ] Keyword Database
  - [ ] Create `src/parser/keywords.json`
  - [ ] Going concern keywords (한국어)
  - [ ] Risk keywords
  - [ ] Emphasis keywords
  - [ ] Severity indicators

- [ ] ML/Statistical Approach (Optional v2)
  - [ ] Train classifier on historical audit reports
  - [ ] Detect emphasis patterns
  - [ ] Severity assessment model
  - [ ] Confidence scoring

- [ ] Testing
  - [ ] Keyword detection tests
  - [ ] Category classification tests
  - [ ] Severity assessment accuracy
  - [ ] False positive rate tests

## Dependencies

```
requests           # HTTP client
pandas            # Data processing
openpyxl          # Excel if needed
lxml              # XML parsing
beautifulsoup4    # HTML parsing
rapidfuzz         # Fuzzy matching for text similarity
```

## Data Flow

```
DART API
   ↓
[Download Report XML]
   ↓
[XML Parser]  → Parse structure, extract sections
   ↓
[Opinion Parser] → Extract opinion, KAM
   ↓
[Emphasis Parser] → Detect going concern, risks
   ↓
[Analyzer] → Risk calculation, scoring
   ↓
[Database/Storage] → Save results
   ↓
[Dashboard] → Visualize findings
```

## Testing Strategy

- Unit tests for each parser component
- Integration tests with sample DART XML files
- Mock data for testing without actual API calls
- Performance benchmarks
- Error handling and edge cases
- Korean language support testing

## Deliverables

- [x] Data models for parsed audit reports
- [ ] XML parser implementation
- [ ] Opinion parser implementation
- [ ] Emphasis parser implementation
- [ ] Unit tests (>80% coverage)
- [ ] Sample DART XML files for testing
- [ ] Parser integration tests
- [ ] Documentation and usage examples
- [ ] Error handling and validation

## Branch

`feature/parser`

## Schedule

Estimated completion: 2-3 weeks

## Notes

- Focus on accuracy over speed initially
- Build in flexibility for DART XML format changes
- Korean language handling is critical
- Emphasis on going concern detection (critical for risk assessment)
- Consider extensibility for future parser versions
