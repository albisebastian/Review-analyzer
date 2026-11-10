"""FastAPI app: JSON API under /api, web UI served from /frontend."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .analyzer import MAX_CHARS, ReviewAnalyzer, ReviewError

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

app = FastAPI(title="Customer Review Analyzer", docs_url="/api/docs", redoc_url=None, openapi_url="/api/openapi.json")
analyzer = ReviewAnalyzer()


class ReviewIn(BaseModel):
    text: str


@app.post("/api/analyze")
def analyze(body: ReviewIn):
    try:
        return analyzer.analyze(body.text)
    except ReviewError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Analysis failed: {exc}") from exc


@app.get("/api/status")
def status():
    return {**analyzer.status(), "max_chars": MAX_CHARS}


@app.post("/api/reload")
def reload_model():
    """Re-scan backend/models/ so a freshly copied .keras file is used without a restart."""
    return {**analyzer.reload(), "max_chars": MAX_CHARS}


@app.middleware("http")
async def no_store(request, call_next):
    response = await call_next(request)
    if request.url.path.startswith("/api/") or request.url.path in {"/", "/index.html"}:
        response.headers["Cache-Control"] = "no-store"
    return response


app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="ui")
