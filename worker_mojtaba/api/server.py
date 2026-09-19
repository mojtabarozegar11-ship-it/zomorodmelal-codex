"""HTTP transport for Worker Mojtaba."""
from typing import Any

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

from worker_mojtaba.api.service import WorkerService

app = FastAPI(title="Worker Mojtaba API", version="0.4.0")
service = WorkerService()


class TaskRequest(BaseModel):
    request: str = Field(min_length=1)
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


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "worker-mojtaba", "version": "0.4.0"}


@app.post("/v1/tasks", response_model=TaskResponse)
def create_task(payload: TaskRequest) -> dict[str, Any]:
    result = service.handle(payload.request, payload.context)
    return result


@app.post("/v1/voice")
async def upload_voice(
    audio: UploadFile = File(...),
    request: str = Form(default=""),
) -> dict[str, Any]:
    if not audio.filename:
        raise HTTPException(status_code=400, detail="audio_filename_required")
    content_type = audio.content_type or ""
    if not content_type.startswith("audio/") and not audio.filename.lower().endswith((".m4a", ".mp3", ".wav", ".ogg", ".webm")):
        raise HTTPException(status_code=415, detail="unsupported_audio_type")
    data = await audio.read()
    if not data:
        raise HTTPException(status_code=400, detail="empty_audio")
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
