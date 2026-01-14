from fastapi import FastAPI # pyright: ignore[reportMissingImports]
from app.api.agent import router as agent_router

app = FastAPI(title="Agent Runtime")

app.include_router(agent_router)
