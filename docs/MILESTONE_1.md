# Milestone 1: MVP (Minimum Viable Product)

## Overview

Milestone 1 focuses on establishing the core infrastructure for the DDIP platform:
1. Project setup and configuration
2. DART API integration
3. CorpCode module
4. Audit report download functionality

## Objectives

### 1. 프로젝트 생성 (Project Setup) ✅
- [x] Initialize Poetry project
- [x] Configure pyproject.toml with all dependencies
- [x] Set up .env.example and configuration
- [x] Create project structure (src/, tests/, docs/)
- [x] Initialize Git repository with main branch
- [ ] Set up GitHub Actions CI/CD
- [ ] Create pre-commit hooks (Black, Ruff, MyPy)

### 2. DART API Integration
- [ ] Implement DARTClient class
  - [ ] Authentication with API key
  - [ ] Error handling and retry logic (using Tenacity)
  - [ ] Rate limiting
- [ ] Implement methods:
  - [ ] `get_corp_code()` - Fetch corporation information
  - [ ] `get_filings()` - Fetch audit report list
  - [ ] `download_report()` - Download audit report document

### 3. CorpCode Module
- [ ] Create Corporation data model
- [ ] Implement CorpCode service
  - [ ] Parse corporation code from DART
  - [ ] Cache corporation information
  - [ ] Search functionality

### 4. 감사보고서 다운로드 (Audit Report Download)
- [ ] Create AuditReport data model
- [ ] Implement download service
  - [ ] Fetch available reports from DART
  - [ ] Download documents (XML, PDF, HWP)
  - [ ] Store locally or in database
  - [ ] Handle errors gracefully

## Technical Specifications

### DART API Endpoints
```
Base URL: https://opendart.fss.or.kr/api

1. corpCode.json
   - List all corporations
   - Returns: Corporation codes and names

2. list.json
   - Fetch filings for a corporation
   - Params: corp_code, pblntf_ty (report type)
   - Returns: Filing list with dates and document numbers

3. document.xml
   - Download document
   - Params: dcm_no (document number), tp (type: xml/pdf/hwp)
   - Returns: Document content
```

### Data Models

#### Corporation
```python
- corp_code: str (Primary key)
- corp_name: str
- stock_code: Optional[str]
- ceo_name: Optional[str]
- established_date: Optional[str]
- industry: Optional[str]
- location: Optional[str]
```

#### AuditReport
```python
- report_id: str (Primary key)
- corp_code: str (Foreign key)
- corp_name: str
- filing_date: str
- report_period: str
- dcm_no: str (DART document number)
- document_type: str (xml/pdf/hwp)
- content: Optional[bytes]
```

## Testing

- Unit tests for DARTClient
- Mock DART API responses
- Integration tests with test DART API
- Error handling tests

## Deliverables

- [x] Project structure and configuration
- [x] DART API client implementation
- [x] Data models (Corporation, AuditReport)
- [ ] Functional DART API integration
- [ ] Unit tests
- [ ] Documentation and API specs

## Dependencies

- requests: HTTP client
- tenacity: Retry logic
- python-dotenv: Environment variables

## Notes

- DART API requires registration and API key
- Rate limiting: Check DART API limits
- Document types: XML (structured), PDF (visual), HWP (Korean format)
