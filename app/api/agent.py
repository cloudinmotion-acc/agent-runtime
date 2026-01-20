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
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

try:
    agent = SimpleChatAgent(
        router=ModelRouterClient(MODEL_ROUTER_URL),
        memory=RedisMemory(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)
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
        logger.info(f"📨 Request received - session_id: {request.session_id}, input: {request.input[:50]}...")
        response = await agent.run(
            session_id=request.session_id,
            input_text=request.input,
            model=request.model
        )
        logger.info(f"✅ State saved to Redis for session: {request.session_id}")
        return {"response": response}
    except ValueError as e:
        logger.error(f"Agent error: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in agent: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/debug/session/{session_id}")
async def get_session_info(session_id: str):
    """Debug endpoint: Get session state and TTL"""
    if agent is None:
        raise HTTPException(status_code=500, detail="Agent not initialized")
    
    try:
        state = agent.memory.get_state(session_id)
        ttl = agent.memory.get_session_ttl(session_id)
        
        if ttl == -2:
            return {"session_id": session_id, "exists": False, "ttl": None}
        
        return {
            "session_id": session_id,
            "exists": True,
            "history_length": len(state.get("history", [])),
            "ttl_seconds": ttl,
            "state": state
        }
    except Exception as e:
        logger.error(f"Debug error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/debug/session/{session_id}")
async def delete_session(session_id: str):
    """Debug endpoint: Delete a session from Redis"""
    if agent is None:
        raise HTTPException(status_code=500, detail="Agent not initialized")
    
    try:
        deleted = agent.memory.delete_session(session_id)
        return {"session_id": session_id, "deleted": deleted}
    except Exception as e:
        logger.error(f"Delete error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
