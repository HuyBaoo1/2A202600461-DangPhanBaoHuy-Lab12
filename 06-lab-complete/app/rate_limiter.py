import time
import uuid

from fastapi import HTTPException

from app.config import settings, redis_client

RATE_BUCKET_TTL_SECONDS = 90


def _bucket_key(api_key: str) -> str:
    return f"rate:{api_key}"


def check_rate_limit(api_key: str) -> None:
    now_ms = int(time.time() * 1000)
    bucket = _bucket_key(api_key)
    member = f"{now_ms}-{uuid.uuid4().hex}"

    pipe = redis_client.pipeline()
    pipe.zadd(bucket, {member: now_ms})
    pipe.zremrangebyscore(bucket, 0, now_ms - 60_000)
    pipe.zcard(bucket)
    pipe.expire(bucket, RATE_BUCKET_TTL_SECONDS)
    _, _, count, _ = pipe.execute()

    if int(count) > settings.rate_limit_per_minute:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded: {settings.rate_limit_per_minute} req/min",
            headers={"Retry-After": "60"},
        )
