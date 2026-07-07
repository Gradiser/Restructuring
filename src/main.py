"""Main entry point for DDIP application."""

import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

logger = logging.getLogger(__name__)


def main() -> None:
    """Main application entry point."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger.info("Starting DDIP Application...")
    logger.info("Milestone 1: MVP Setup")


if __name__ == "__main__":
    main()
