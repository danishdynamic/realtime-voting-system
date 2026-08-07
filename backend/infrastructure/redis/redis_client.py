# infrastructure/redis/redis_client.py
import redis
import os

# Use an Environment Variable for the host, defaulting to localhost
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client : redis.Redis = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
    socket_connect_timeout=5 
)

try:
    redis_client.ping()
    print(f"✅ Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
except redis.ConnectionError:
    print(f"❌ Could not connect to Redis at {REDIS_HOST}:{REDIS_PORT}. Is it running?")