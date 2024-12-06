from typing import Optional, Dict, Any
import httpx
from fastapi import HTTPException


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

    async def request(
        self, endpoint: str, method: str = "GET", data: Optional[Dict] = None
    ) -> Any:
        headers = {"Content-Type": "application/json", "x-api-key": self.api_key}

        url = f"{self.base_url}{endpoint}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method=method, url=url, headers=headers, json=data
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                raise HTTPException(status_code=response.status_code, detail=str(e))
