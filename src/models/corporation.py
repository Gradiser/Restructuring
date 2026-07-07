"""Corporation data model."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Corporation:
    """Corporation information model."""

    corp_code: str
    corp_name: str
    stock_code: Optional[str] = None
    ceo_name: Optional[str] = None
    established_date: Optional[str] = None
    industry: Optional[str] = None
    location: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class AuditReport:
    """Audit report information model."""

    report_id: str
    corp_code: str
    corp_name: str
    filing_date: str
    report_period: str
    dcm_no: str
    document_type: str
    content: Optional[bytes] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
