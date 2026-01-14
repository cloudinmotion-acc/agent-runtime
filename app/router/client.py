import httpx
import logging

logger = logging.getLogger(__name__)

class ModelRouterClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        logger.info(f"ModelRouterClient initialized with URL: {base_url}")

    async def generate(self, prompt: str, model: str, state: dict):
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                resp = await client.post(
                    f"{self.base_url}/generate",
                    json={
                        "prompt": prompt,
                        "model": model,
                        "state": state
                    }
                )
                resp.raise_for_status()
                return resp.json()
        except httpx.ConnectError as e:
            logger.error(f"Failed to connect to ModelRouter at {self.base_url}: {e}")
            raise ValueError(f"ModelRouter service unavailable at {self.base_url}")
        except httpx.HTTPStatusError as e:
            logger.error(f"ModelRouter returned error {e.response.status_code}: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error calling ModelRouter: {e}")
            raise
