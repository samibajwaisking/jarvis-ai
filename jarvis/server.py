"""Web server: a small FastAPI app with a chat UI and a JSON API."""

from __future__ import annotations

import hmac
from pathlib import Path

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from . import __version__
from .about import CREATOR, TAGLINE
from .assistant import Jarvis
from .guide import GUIDE

WEB_DIR = Path(__file__).parent / "web"

app = FastAPI(title="Jarvis AI", version=__version__, description=TAGLINE)
_jarvis: Jarvis | None = None


def get_jarvis() -> Jarvis:
    global _jarvis
    if _jarvis is None:
        _jarvis = Jarvis()
    return _jarvis


def require_token(
    authorization: str = Header(default=""),
    x_jarvis_token: str = Header(default=""),
    jarvis: Jarvis = Depends(get_jarvis),
) -> None:
    """If JARVIS_API_TOKEN is set, every API call must send it."""
    expected = jarvis.settings.api_token
    if not expected:
        return
    supplied = x_jarvis_token or authorization.removeprefix("Bearer ").strip()
    if not hmac.compare_digest(supplied, expected):
        raise HTTPException(status_code=401, detail="Invalid or missing token.")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    session: str = Field(default="web", max_length=64)


class ChatResponse(BaseModel):
    reply: str


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(WEB_DIR / "index.html")


@app.get("/api/health")
def health(jarvis: Jarvis = Depends(get_jarvis)) -> dict:
    s = jarvis.settings
    return {
        "status": "ok",
        "version": __version__,
        "provider": s.provider,
        "model": s.model,
        "auth_required": bool(s.api_token),
    }


@app.post("/api/chat", response_model=ChatResponse, dependencies=[Depends(require_token)])
def chat(req: ChatRequest, jarvis: Jarvis = Depends(get_jarvis)) -> ChatResponse:
    return ChatResponse(reply=jarvis.ask(req.message, session=req.session))


@app.post("/api/clear", dependencies=[Depends(require_token)])
def clear(session: str = "web", jarvis: Jarvis = Depends(get_jarvis)) -> dict:
    jarvis.clear(session)
    return {"status": "cleared"}


@app.get("/api/guide")
def guide() -> dict:
    return {"guide": GUIDE}


@app.get("/api/about")
def about() -> dict:
    return CREATOR
