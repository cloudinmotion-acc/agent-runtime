from fastapi import FastAPI # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv
from app.api.agent import router as agent_router

load_dotenv()

app = FastAPI(title="Agent Runtime")

app.include_router(agent_router)
