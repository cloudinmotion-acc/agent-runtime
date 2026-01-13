import requests
from app.config import MODEL_ROUTER_URL

def call_llm(prompt: str, model: str = "gpt-4o-mini") -> str:
    response = requests.post(
        f"{MODEL_ROUTER_URL}/generate",
        json={
            "prompt": prompt,
            "model": model
        },
        timeout=30
    )
    response.raise_for_status()
    return response.json()["output"]
