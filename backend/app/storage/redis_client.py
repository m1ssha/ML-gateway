import redis.asyncio as redis
from app.config import settings

redis_client: redis.Redis | None = None

async def init_redis():
    global redis_client
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

async def close_redis():
    if redis_client:
        await redis_client.close()

async def get_redis() -> redis.Redis:
    if redis_client is None:
        await init_redis()
    return redis_client
