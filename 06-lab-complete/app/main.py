"""
Production AI Agent — Kết hợp tất cả Day 12 concepts

Checklist:
  ✅ Config từ environment (12-factor)
  ✅ Structured JSON logging
  ✅ API Key authentication
  ✅ Rate limiting
  ✅ Cost guard
  ✅ Input validation (Pydantic)
  ✅ Health check + Readiness probe
  ✅ Graceful shutdown
  ✅ Security headers
  ✅ CORS
  ✅ Error handling
"""
import contextlib
import json
import logging
import signal
import time
from datetime import datetime, timezone
from typing import List

from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

from app.auth import verify_api_key
from app.config import settings, redis_client
from app.cost_guard import check_budget, get_daily_spend
from app.rate_limiter import check_rate_limit
from utils.mock_llm import ask as llm_ask

# ─────────────────────────────────────────────────────────
# Logging — JSON structured
# ─────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format='%(message)s',
)
logger = logging.getLogger(__name__)

START_TIME = time.time()
_is_ready = False
_request_count = 0
_error_count = 0


def _log(event: str, **data) -> None:
    payload = {"event": event, "timestamp": datetime.now(timezone.utc).isoformat(), **data}
    logger.info(json.dumps(payload))


def _history_key(api_key: str) -> str:
    return f"history:{api_key}"


def load_history(api_key: str) -> List[dict]:
    items = redis_client.lrange(_history_key(api_key), 0, -1)
    return [json.loads(item) for item in items]


def append_history(api_key: str, question: str, answer: str) -> None:
    item = {
        "question": question,
        "answer": answer,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    history_key = _history_key(api_key)
    pipe = redis_client.pipeline()
    pipe.rpush(history_key, json.dumps(item))
    pipe.ltrim(history_key, -settings.history_size, -1)
    pipe.expire(history_key, 7 * 24 * 3600)
    pipe.execute()


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    global _is_ready
    _log("startup", app=settings.app_name, version=settings.app_version, environment=settings.environment)

    try:
        redis_client.ping()
    except Exception as exc:
        _log("startup_error", error=str(exc))
        raise

    _is_ready = True
    _log("ready")
    yield
    _is_ready = False
    _log("shutdown")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs" if settings.environment != "production" else None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type", "X-API-Key"],
)


@app.middleware("http")
async def request_middleware(request: Request, call_next):
    global _request_count, _error_count
    start = time.time()
    _request_count += 1

    try:
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        if "server" in response.headers:
            del response.headers["server"]

        duration_ms = round((time.time() - start) * 1000, 1)
        _log(
            "request",
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration_ms=duration_ms,
        )
        return response
    except Exception as exc:
        _error_count += 1
        _log("request_error", error=str(exc), path=request.url.path)
        raise


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)


class AskResponse(BaseModel):
    question: str
    answer: str
    model: str
    timestamp: str
    history_length: int
    daily_spend_usd: float


@app.get("/", tags=["Info"])
def root():
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "endpoints": {
            "ask": "POST /ask (requires X-API-Key)",
            "health": "GET /health",
            "ready": "GET /ready",
            "history": "GET /history (requires X-API-Key)",
        },
    }


@app.post("/ask", response_model=AskResponse, tags=["Agent"])
async def ask_agent(body: AskRequest, request: Request, api_key: str = Depends(verify_api_key)):
    check_rate_limit(api_key)

    input_tokens = len(body.question.split()) * 2
    check_budget(api_key, input_tokens=input_tokens)

    _log(
        "agent_request",
        client=request.client.host if request.client else "unknown",
        question_length=len(body.question),
    )

    answer = llm_ask(body.question)
    output_tokens = len(answer.split()) * 2
    check_budget(api_key, output_tokens=output_tokens)
    append_history(api_key, body.question, answer)

    return AskResponse(
        question=body.question,
        answer=answer,
        model=settings.llm_model,
        timestamp=datetime.now(timezone.utc).isoformat(),
        history_length=len(load_history(api_key)),
        daily_spend_usd=get_daily_spend(api_key),
    )


@app.get("/history", tags=["Agent"])
def get_history(api_key: str = Depends(verify_api_key)):
    history = load_history(api_key)
    return {
        "history": history,
        "history_size": len(history),
    }


@app.get("/health", tags=["Operations"])
def health():
    return {
        "status": "ok",
        "version": settings.app_version,
        "environment": settings.environment,
        "uptime_seconds": round(time.time() - START_TIME, 1),
        "total_requests": _request_count,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/ready", tags=["Operations"])
def ready():
    if not _is_ready:
        raise HTTPException(status_code=503, detail="Not ready")
    try:
        redis_client.ping()
    except Exception:
        raise HTTPException(status_code=503, detail="Redis unavailable")
    return {"ready": True}


@app.get("/metrics", tags=["Operations"])
def metrics(api_key: str = Depends(verify_api_key)):
    return {
        "uptime_seconds": round(time.time() - START_TIME, 1),
        "total_requests": _request_count,
        "error_count": _error_count,
        "daily_budget_usd": settings.daily_budget_usd,
        "daily_spend_usd": get_daily_spend(api_key),
    }


def _handle_signal(signum, _frame):
    _log("signal_received", signum=signum)


signal.signal(signal.SIGTERM, _handle_signal)


if __name__ == "__main__":
    _log("startup_command", host=settings.host, port=settings.port)
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        timeout_graceful_shutdown=30,
    )
