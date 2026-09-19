"""HTTP transport for Worker Mojtaba."""
from fastapi import FastAPI
from pydantic import BaseModel

from worker_mojtaba.api.service import WorkerService

app = FastAPI(title="Worker Mojtaba API", version="0.2.0")
service = WorkerService()


class TaskRequest(BaseModel):
    request: str


class TaskResponse(BaseModel):
    status: str
    request: str
    intent: str | None = None
    route: str | None = None
    plan: list[str] = []
    ai: dict = {}
    tools: list[dict[str, str]] = []


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "worker-mojtaba"}


@app.post("/v1/tasks", response_model=TaskResponse)
def create_task(payload: TaskRequest) -> dict:
    return service.handle(payload.request)
