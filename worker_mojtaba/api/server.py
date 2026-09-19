"""HTTP transport for Worker Mojtaba."""
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from worker_mojtaba.api.service import WorkerService

app = FastAPI(title="Worker Mojtaba API", version="0.3.0")
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
    return {"status": "ok", "service": "worker-mojtaba", "version": "0.3.0"}


@app.post("/v1/tasks", response_model=TaskResponse)
def create_task(payload: TaskRequest) -> dict[str, Any]:
    result = service.handle(payload.request)
    result["context"] = payload.context
    return result
