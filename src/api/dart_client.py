"""DART API client for fetching corporate audit reports."""

import logging
from typing import Any, Optional

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


class DARTClient:
    """Client for DART (Data Analysis, Retrieval and Transfer System) API."""

    BASE_URL = "https://opendart.fss.or.kr/api"

    def __init__(self, api_key: str) -> None:
        """Initialize DART client.

        Args:
            api_key: DART API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.params = {"crtfc_key": api_key}  # type: ignore[assignment]

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def get_corp_code(self, corp_code: str) -> Optional[dict[str, Any]]:
        """Fetch corporation information by code.

        Args:
            corp_code: Corporation code

        Returns:
            Corporation information or None if not found
        """
        try:
            url = f"{self.BASE_URL}/corpCode.json"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            logger.info(f"Successfully fetched CorpCode: {corp_code}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch CorpCode {corp_code}: {e}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def get_filings(
        self, corp_code: str, report_type: str = "11014"
    ) -> Optional[dict[str, Any]]:
        """Fetch audit report filings for a corporation.

        Args:
            corp_code: Corporation code
            report_type: Type of report (default: 11014 = Audit Report)

        Returns:
            Filing information or None if not found
        """
        try:
            url = f"{self.BASE_URL}/list.json"
            params = {"corp_code": corp_code, "pblntf_ty": report_type}
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            logger.info(f"Successfully fetched filings for {corp_code}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch filings for {corp_code}: {e}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def download_report(
        self, dcm_no: str, report_type: str = "xml"
    ) -> Optional[bytes]:
        """Download audit report document.

        Args:
            dcm_no: Document number
            report_type: Document type (xml, pdf, hwp)

        Returns:
            Document content or None if download failed
        """
        try:
            url = f"{self.BASE_URL}/document.xml"
            params = {"dcm_no": dcm_no, "tp": report_type}
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            logger.info(f"Successfully downloaded report: {dcm_no}")
            return response.content
        except requests.RequestException as e:
            logger.error(f"Failed to download report {dcm_no}: {e}")
            raise

    def close(self) -> None:
        """Close the session."""
        self.session.close()
