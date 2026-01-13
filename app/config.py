import os
from dotenv import load_dotenv

load_dotenv()

# Model Router
MODEL_ROUTER_URL = os.getenv("MODEL_ROUTER_URL")

# Redis
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

# Postgres
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
