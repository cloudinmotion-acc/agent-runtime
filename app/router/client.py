import httpx

class ModelRouterClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def generate(self, prompt: str, model: str, state: dict):
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/generate",
                json={
                    "prompt": prompt,
                    "model": model,
                    "state": state
                },
                timeout=60
            )
            resp.raise_for_status()
            return resp.json()
