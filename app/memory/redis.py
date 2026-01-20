import json
from redis.cluster import RedisCluster
import logging
import os

logger = logging.getLogger(__name__)

# Session expiration: 24 hours (86400 seconds)
SESSION_TTL = int(os.getenv("SESSION_TTL", "86400"))

class RedisMemory:
    def __init__(self, host: str, port: int, password: str):
        if not host:
            raise ValueError("REDIS_HOST environment variable is not set")
        
        try:
            logger.info(f"Attempting to connect to Redis at {host}:{port}...")
            self.client = RedisCluster(
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
            logger.info(f"✓ Redis connected successfully: {host}:{port}")

        except Exception as e:
            logger.error(f"Redis connection failed: {e}")
            raise

    def get_state(self, session_id: str) -> dict:
        try:
            data = self.client.get(session_id)
            if data:
                logger.info(f"📖 Retrieved state for {session_id}")
                return json.loads(data)
            else:
                logger.info(f"🆕 No state found for {session_id}, starting new conversation")
                return {}
        except Exception as e:
            logger.error(f"Failed to get state for {session_id}: {e}")
            raise

    def save_state(self, session_id: str, state: dict):
        try:
            json_data = json.dumps(state)
            self.client.set(session_id, json_data, ex=SESSION_TTL)
            logger.info(f"💾 State persisted to Redis for {session_id} - history length: {len(state.get('history', []))} - expires in {SESSION_TTL}s")
        except Exception as e:
            logger.error(f"Failed to save state for {session_id}: {e}")
            raise

    def get_session_ttl(self, session_id: str) -> int:
        """Get remaining TTL for a session in seconds (-1 if no expiry, -2 if not found)"""
        try:
            ttl = self.client.ttl(session_id)
            return ttl
        except Exception as e:
            logger.error(f"Failed to get TTL for {session_id}: {e}")
            return -2

    def delete_session(self, session_id: str) -> bool:
        """Delete a session from Redis"""
        try:
            result = self.client.delete(session_id)
            if result:
                logger.info(f"🗑️  Deleted session {session_id}")
                return True
            else:
                logger.info(f"Session {session_id} not found")
                return False
        except Exception as e:
            logger.error(f"Failed to delete session {session_id}: {e}")
            raise
        
