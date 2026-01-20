import logging
from fastapi import FastAPI # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv
from app.api.agent import router as agent_router

load_dotenv()

# Configure logging to show INFO and above
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(title="Agent Runtime")

app.include_router(agent_router)
