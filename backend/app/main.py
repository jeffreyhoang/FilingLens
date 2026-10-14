import psycopg
from fastapi import FastAPI

from app.config import get_settings

app = FastAPI(title="FilingLens")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/db")
def health_db() -> dict[str, str | None]:
    with psycopg.connect(get_settings().database_url, connect_timeout=10) as conn:
        row = conn.execute(
            "SELECT extversion FROM pg_extension WHERE extname = 'vector'"
        ).fetchone()
    return {"status": "ok", "pgvector": row[0] if row else None}
