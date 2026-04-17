from datetime import datetime, timezone

from fastapi import HTTPException

from app.config import settings, redis_client


def _budget_key(api_key: str) -> str:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return f"budget:{api_key}:{today}"


def calculate_cost(input_tokens: int = 0, output_tokens: int = 0) -> float:
    return (input_tokens / 1000) * 0.00015 + (output_tokens / 1000) * 0.0006


def check_budget(api_key: str, input_tokens: int = 0, output_tokens: int = 0) -> float:
    cost = calculate_cost(input_tokens, output_tokens)
    budget_key = _budget_key(api_key)
    current_spent = float(redis_client.get(budget_key) or 0)

    if current_spent + cost > settings.daily_budget_usd:
        raise HTTPException(
            status_code=402,
            detail="Daily budget exceeded. Try again tomorrow.",
        )

    new_total = redis_client.incrbyfloat(budget_key, cost)
    redis_client.expire(budget_key, 48 * 3600)
    return float(new_total)


def get_daily_spend(api_key: str) -> float:
    return float(redis_client.get(_budget_key(api_key)) or 0)
