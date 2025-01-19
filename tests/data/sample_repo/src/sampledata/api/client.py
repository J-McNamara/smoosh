"""API client for external services."""
import requests
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class APIClient:
    """Client for external API interactions."""

    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """Initialize client with configuration."""
        self.base_url = base_url
        self.api_key = api_key

    def get_data(self, endpoint: str, params: Dict[str, str]) -> Dict:
        """Fetch data from API endpoint."""
        headers = {'Authorization': f'Bearer {self.api_key}'} if self.api_key else {}

        try:
            response = requests.get(
                f"{self.base_url}/{endpoint}",
                params=params,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"API request failed: {str(e)}")
            raise
