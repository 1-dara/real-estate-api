import redis
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

redis_client = redis.from_url(REDIS_URL, decode_responses=True)

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True
)


def get_cache(key: str):
    try:
        value = redis_client.get(key)
        return value
    except Exception:
        return None


def set_cache(key: str, value: str, expire: int = 300):
    try:
        redis_client.setex(key, expire, value)
    except Exception:
        pass


def delete_cache(key: str):
    try:
        redis_client.delete(key)
    except Exception:
        pass


def delete_pattern(pattern: str):
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
    except Exception:
        pass
