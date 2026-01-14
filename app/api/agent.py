import os
import logging
from fastapi import APIRouter, HTTPException # pyright: ignore[reportMissingImports]
from pydantic import BaseModel, Field
from app.agents.simple_agent import SimpleChatAgent
from app.router.client import ModelRouterClient
from app.memory.redis import RedisMemory

logger = logging.getLogger(__name__)

class AgentRequest(BaseModel):
    session_id: str = Field(..., description="Unique session identifier")
    input: str = Field(..., description="User input text")
    model: str = Field(default="gpt-5-nano", description="Model to use for generation")

router = APIRouter()

MODEL_ROUTER_URL = os.getenv("MODEL_ROUTER_URL", "http://localhost:8000")
REDIS_HOST = str(os.getenv("REDIS_HOST"))
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

try:
    agent = SimpleChatAgent(
        router=ModelRouterClient(MODEL_ROUTER_URL),
        memory=RedisMemory(REDIS_HOST, REDIS_PORT)
    )
    logger.info("Agent initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize agent: {e}")
    # Don't fail startup - let endpoint handle the error
    agent = None

@router.post("/agent/run")
async def run_agent(request: AgentRequest):
    if agent is None:
        raise HTTPException(status_code=500, detail="Agent not initialized. Check Redis and ModelRouter connectivity.")
    
    try:
        response = await agent.run(
            session_id=request.session_id,
            input_text=request.input,
            model=request.model
        )
        return {"response": response}
    except ValueError as e:
        logger.error(f"Agent error: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in agent: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
