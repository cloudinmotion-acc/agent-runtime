import json
from redis.cluster import RedisCluster
import logging
import os
import time
from ssl import create_default_context, CERT_REQUIRED
import certifi

logger = logging.getLogger(__name__)

# Session expiration: 24 hours (86400 seconds)
SESSION_TTL = int(os.getenv("SESSION_TTL", "86400"))

class RedisMemory:
    def __init__(self, host: str, port: int, password: str, max_retries: int = 5, retry_delay: int = 10):
        if not host:
            raise ValueError("REDIS_HOST environment variable is not set")
        
        self.host = host
        self.port = port
        self.password = password
        self.client = None
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        self._connect_with_retry()
    
    def _connect_with_retry(self):
        """Connect to Redis Cluster with retry logic"""
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Attempting to connect to Redis Cluster at {self.host}:{self.port}... (Attempt {attempt + 1}/{self.max_retries})")
                
                # Create SSL context for AWS ElastiCache using certifi CA bundle
                ssl_context = create_default_context(cafile=certifi.where())
                ssl_context.check_hostname = True
                ssl_context.verify_mode = CERT_REQUIRED
                
                # RedisCluster with TLS support
                self.client = RedisCluster(
                    host=self.host,
                    port=self.port,
                    password=self.password,
                    decode_responses=True,
                    socket_timeout=10,
                    socket_connect_timeout=10,
                    skip_full_coverage_check=True,
                    ssl=True,
                    ssl_context=ssl_context,
                )

                self.client.ping()
                logger.info(f"✓ Redis Cluster connected successfully: {self.host}:{self.port}")
                return

            except Exception as e:
                logger.warning(f"Redis connection attempt {attempt + 1}/{self.max_retries} failed: {e}")
                
                if attempt < self.max_retries - 1:
                    logger.info(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"Failed to connect to Redis Cluster after {self.max_retries} attempts")
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
        
