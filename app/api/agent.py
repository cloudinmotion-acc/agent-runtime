import os
from fastapi import APIRouter # pyright: ignore[reportMissingImports]
from app.agents.simple_agent import SimpleChatAgent
from app.router.client import ModelRouterClient
from app.memory.redis import RedisMemory

router = APIRouter()

agent = SimpleChatAgent(
    router=ModelRouterClient("http://localhost:8000"),
    memory=RedisMemory(os.getenv("REDIS_URL", "redis://localhost:6379"))
)

@router.post("/agent/run")
async def run_agent(payload: dict):
    return {
        "response": await agent.run(
            session_id=payload["session_id"],
            input_text=payload["input"],
            model=payload["model"]
        )
    }
