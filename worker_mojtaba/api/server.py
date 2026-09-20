"""HTTP transport for Worker Mojtaba."""
import os
from typing import Any

from fastapi import FastAPI, File, Form, Header, HTTPException, UploadFile
from pydantic import BaseModel, Field

from worker_mojtaba.api.service import WorkerService

app = FastAPI(title="Worker Mojtaba API", version="0.5.0")
service = WorkerService()

MAX_REQUEST_LENGTH = 8_000
MAX_AUDIO_BYTES = 10 * 1024 * 1024


class TaskRequest(BaseModel):
    request: str = Field(min_length=1, max_length=MAX_REQUEST_LENGTH)
    context: dict[str, Any] = Field(default_factory=dict)


class TaskResponse(BaseModel):
    status: str
    request: str
    intent: str | None = None
    route: str | None = None
    plan: list[str] = Field(default_factory=list)
    ai: dict[str, Any] = Field(default_factory=dict)
    execution: dict[str, Any] = Field(default_factory=dict)
    tools: list[str] = Field(default_factory=list)


def _require_token(authorization: str | None) -> None:
    expected = os.environ.get("WORKER_API_TOKEN", "").strip()
    if not expected:
        raise HTTPException(status_code=503, detail="api_auth_not_configured")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="authentication_required")
    provided = authorization[7:].strip()
    if not provided or provided != expected:
        raise HTTPException(status_code=401, detail="invalid_credentials")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "worker-mojtaba", "version": "0.5.0"}


@app.post("/v1/tasks", response_model=TaskResponse)
def create_task(
    payload: TaskRequest,
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    _require_token(authorization)
    result = service.handle(payload.request, payload.context)
    return result


@app.post("/v1/voice")
async def upload_voice(
    audio: UploadFile = File(...),
    request: str = Form(default="", max_length=MAX_REQUEST_LENGTH),
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    _require_token(authorization)
    if not audio.filename:
        raise HTTPException(status_code=400, detail="audio_filename_required")

    content_type = audio.content_type or ""
    allowed_extensions = (".m4a", ".mp3", ".wav", ".ogg", ".webm")
    if not content_type.startswith("audio/") and not audio.filename.lower().endswith(allowed_extensions):
        raise HTTPException(status_code=415, detail="unsupported_audio_type")

    data = await audio.read(MAX_AUDIO_BYTES + 1)
    if not data:
        raise HTTPException(status_code=400, detail="empty_audio")
    if len(data) > MAX_AUDIO_BYTES:
        raise HTTPException(status_code=413, detail="audio_too_large")

    return {
        "status": "received",
        "filename": audio.filename,
        "content_type": content_type,
        "size_bytes": len(data),
        "request": request,
        "transcription": None,
        "audio_response": None,
        "provider_required": "speech_provider_required",
    }
