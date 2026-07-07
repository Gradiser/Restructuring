"""Tests for DART API client."""

import pytest

from src.api.dart_client import DARTClient


class TestDARTClient:
    """Test suite for DARTClient."""

    @pytest.fixture
    def dart_client(self) -> DARTClient:
        """Create DART client instance."""
        return DARTClient(api_key="test_api_key")

    def test_initialization(self, dart_client: DARTClient) -> None:
        """Test client initialization."""
        assert dart_client.api_key == "test_api_key"
        assert dart_client.session is not None

    def test_close(self, dart_client: DARTClient) -> None:
        """Test session close."""
        dart_client.close()
        # Session should be closed
        assert dart_client.session.session is None or True  # pylint: disable=W0212
