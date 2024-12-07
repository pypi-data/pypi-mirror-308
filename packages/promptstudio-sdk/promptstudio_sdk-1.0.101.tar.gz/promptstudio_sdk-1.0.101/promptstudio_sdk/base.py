from typing import Optional, Dict, Any
import httpx
from fastapi import HTTPException
from promptstudio_sdk.utils.logger import setup_logger

# Set up logging
logger = setup_logger()


class Base:
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Base class with configuration

        Args:
            config: Dictionary containing:
                - api_key: API key for authentication
                - env: Environment ('test' or 'prod')
                - bypass: Optional boolean to bypass server
        """
        self.api_key = config.get("api_key")
        self.env = config.get("env", "prod")
        self.bypass = config.get("bypass", False)
        self.base_url = (
            "https://api.promptstudio.dev/api/v1"
            if self.env == "prod"
            else "https://api.playground.promptstudio.dev/api/v1"
        )
        logger.info(f"Initialized Base with environment: {self.env}")

    async def request(
        self,
        endpoint: str,
        method: str = "GET",
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> Any:
        """
        Make HTTP request to the API

        Args:
            endpoint: API endpoint path
            method: HTTP method (GET, POST, etc.)
            data: Request body data for POST/PUT requests
            params: Query parameters for GET requests

        Returns:
            API response data
        """
        headers = {"Content-Type": "application/json", "x-api-key": self.api_key}
        url = f"{self.base_url}{endpoint}"

        logger.info(f"Making {method} request to: {url}")
        if data:
            logger.info(f"Request payload: {data}")
        if params:
            logger.info(f"Request params: {params}")

        async with httpx.AsyncClient() as client:
            try:
                if method.upper() == "GET":
                    logger.info(f"Sending GET request to {url}")
                    response = await client.get(url, headers=headers, params=params)
                elif method.upper() == "POST":
                    logger.info(f"Sending POST request to {url}")
                    logger.info(f"POST data: {data}")
                    response = await client.post(url, headers=headers, json=data)
                else:
                    response = await client.request(
                        method=method,
                        url=url,
                        headers=headers,
                        params=params if method.upper() == "GET" else None,
                        json=data if method.upper() != "GET" else None,
                    )

                response.raise_for_status()
                logger.info(f"Response status code: {response.status_code}")
                response_data = response.json()
                logger.info(f"Response data: {response_data}")
                return response_data

            except httpx.HTTPError as e:
                error_detail = str(e)
                try:
                    error_json = response.json()
                    if "detail" in error_json:
                        error_detail = error_json["detail"]
                except:
                    pass

                logger.error(f"HTTP Error: {error_detail}")
                raise HTTPException(
                    status_code=getattr(e, "response", httpx.Response(500)).status_code,
                    detail=error_detail,
                )
            except Exception as e:
                logger.error(f"Request failed: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")
