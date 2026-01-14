import json
import redis

class RedisMemory:
    def __init__(self, url: str):
        self.client = redis.Redis.from_url(url, decode_responses=True)

    def get_state(self, session_id: str) -> dict:
        data = self.client.get(session_id)
        return json.loads(data) if data else {}

    def save_state(self, session_id: str, state: dict):
        self.client.set(session_id, json.dumps(state))
