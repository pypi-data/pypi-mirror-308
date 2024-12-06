from typing import Dict, Any, TypedDict, Optional
import aiohttp
import logging
import json

logger = logging.getLogger(__name__)


class ConfigDict(TypedDict):
    api_key: str
    env: str
    bypass: Optional[bool]


class Base:
    def __init__(self, config: ConfigDict):
        """
        Initialize the base class with configuration

        Args:
            config: Dictionary containing:
                - 'api_key': API key
                - 'env': Environment ('test' or 'prod')
                - 'bypass': Optional boolean to bypass PromptStudio server
        """
        self.api_key = config["api_key"]
        self.env = config["env"]
        self.bypass = config.get("bypass", False)

        self.base_url = (
            "https://api.promptstudio.dev/api/v1"
            if self.env == "prod"
            else "https://api.playground.promptstudio.dev/api/v1"
        )

    async def _request(
        self, endpoint: str, method: str = "GET", **kwargs
    ) -> Dict[str, Any]:
        """
        Make async HTTP requests to the API with proper request body handling
        """
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": "nDBabew4CGIKD8uKnOqOajG8AZgczzgW",
        }

        # Log request details
        logger.info(f"Making {method} request to: {url}")
        if "data" in kwargs:
            logger.info(f"Request body: {kwargs['data']}")

        async with aiohttp.ClientSession() as session:
            # For POST requests with data
            if method.upper() == "POST" and "data" in kwargs:
                # Ensure data is properly JSON encoded
                if isinstance(kwargs["data"], str):
                    # If data is already a JSON string, use it as is
                    json_data = kwargs["data"]
                else:
                    # If data is a dict or other object, convert to JSON string
                    json_data = json.dumps(kwargs["data"])

                # Make the request with JSON data
                async with session.post(
                    url, headers=headers, data=json_data
                ) as response:
                    response.raise_for_status()
                    return await response.json()
            else:
                # For other requests
                async with session.request(
                    method=method, url=url, headers=headers, **kwargs
                ) as response:
                    response.raise_for_status()
                    return await response.json()
