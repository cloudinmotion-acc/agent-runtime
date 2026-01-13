import redis
from app.config import REDIS_HOST, REDIS_PORT

client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

def get_context(user_id: str) -> str:
    return client.get(user_id) or ""

def set_context(user_id: str, context: str):
    client.set(user_id, context)
