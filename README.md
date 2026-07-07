# DDIP (DART Data Intelligence Platform)

## Overview

DDIP is a comprehensive financial audit analysis and risk detection platform that integrates with Korea's DART (Data Analysis, Retrieval and Transfer System) to automatically download, parse, and analyze corporate audit reports.

## Project Goals

- Automated audit report collection from DART
- Intelligent parsing of financial documents (XML, PDF)
- Risk detection (Going Concern, Liquidation Risk)
- Excel report generation
- Interactive web dashboard for analysis
- AI-powered audit opinion summarization

## Tech Stack

- **Language**: Python 3.12
- **Package Manager**: Poetry
- **Code Quality**: Ruff, Black, MyPy
- **Testing**: Pytest
- **Data Processing**: Pandas, OpenPyXL, LXML, BeautifulSoup4
- **Matching**: RapidFuzz
- **Reliability**: Tenacity
- **Frontend**: Streamlit
- **Database**: SQLAlchemy, SQLite (MVP), PostgreSQL (v2)

## Project Structure

```
ddip/
├── pyproject.toml
├── README.md
├── .env.example
├── .gitignore
├── LICENSE
├── docs/
├── tests/
└── src/
    ├── api/              # DART API integration
    ├── parser/           # Document parsing
    ├── detector/         # Risk detection
    ├── analyzer/         # Analysis logic
    ├── database/         # Database ORM
    ├── dashboard/        # Streamlit UI
    ├── models/           # Data models
    ├── excel/            # Excel export
    ├── utils/            # Utilities
    └── main.py           # Entry point
```

## Roadmap

### Milestone 1 (MVP)
- [ ] 프로젝트 생성 (Project Setup)
- [ ] DART API Integration
- [ ] CorpCode Module
- [ ] 감사보고서 다운로드 (Audit Report Download)

### Milestone 2
- [ ] XML Parser
- [ ] Opinion Parser
- [ ] Emphasis Parser

### Milestone 3
- [ ] Going Concern Detection
- [ ] Liquidation Detector
- [ ] Risk Engine

### Milestone 4
- [ ] Excel Export
- [ ] SQLite Database

### Milestone 5
- [ ] Dashboard (Streamlit)
- [ ] AI Summary

## Installation

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

## Configuration

```bash
# Create .env from template
cp .env.example .env

# Add your DART API credentials
```

## Usage

```bash
# Run main application
python -m src.main

# Run tests
pytest

# Run code quality checks
ruff check .
black --check .
mypy src/

# Format code
black .

# Run dashboard
streamlit run src/dashboard/app.py
```

## License

MIT
