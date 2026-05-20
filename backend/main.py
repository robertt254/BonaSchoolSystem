import os
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

import auth
import models
import students
import fees
import staff
import academics
import attendance
from database import engine
from limiter import limiter

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Bona School Management API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# ── Security headers ──────────────────────────────────────────────────────────
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';"
    )
    return response


# ── CORS (origins come from environment, comma-separated) ────────────────────
_raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:5174")
origins = [o.strip() for o in _raw_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Global exception handler — prevents stack traces leaking to clients ───────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled error on %s %s: %s", request.method, request.url, exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal error occurred. Please try again."},
    )


# ── Startup: validate required env vars, then sync DB schema ─────────────────
@app.on_event("startup")
async def startup():
    required_vars = ["SECRET_KEY", "DATABASE_URL"]
    missing = [k for k in required_vars if not os.getenv(k)]
    if missing:
        raise RuntimeError(f"Cannot start — missing environment variables: {missing}")
    models.Base.metadata.create_all(bind=engine)
    logger.info("Database schema synced.")


# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(students.router)
app.include_router(fees.router)
app.include_router(staff.router)
app.include_router(academics.router)
app.include_router(attendance.router)


@app.get("/")
def read_root():
    return {"status": "online", "system": "Bona School Backend API"}
