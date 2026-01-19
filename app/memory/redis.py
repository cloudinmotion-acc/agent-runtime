import json
import redis
import logging
import os

logger = logging.getLogger(__name__)

class RedisMemory:
    def __init__(self, host: str, port: int, password: str):
        try:
            # Normalize host
            host = host.replace("redis://", "").replace("rediss://", "")

            self.client = redis.Redis(
                host=host,
                port=port,
                password=password,
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5,
                ssl=True,
                ssl_ca_certs="/etc/pki/tls/certs/ca-bundle.crt",
            )

            self.client.ping()
            logger.info(f"Redis connected: {host}:{port}")

        except Exception as e:
            logger.error(f"Redis connection failed: {e}")
            raise

    def get_state(self, session_id: str) -> dict:
        try:
            data = self.client.get(session_id)
            return json.loads(data) if data else {}
        except Exception as e:
            logger.error(f"Failed to get state for {session_id}: {e}")
            return {}

    def save_state(self, session_id: str, state: dict):
        try:
            self.client.set(session_id, json.dumps(state))
        except Exception as e:
            logger.error(f"Failed to save state for {session_id}: {e}")
            raise
        
