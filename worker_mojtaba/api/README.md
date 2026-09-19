# Worker Mojtaba API

HTTP transport for the Android client.

## Run

Set PYTHONPATH to the repository root, then run:

    uvicorn worker_mojtaba.api.server:app --host 0.0.0.0 --port 8787

Endpoints:

- GET /health
- POST /v1/tasks with JSON {"request":"..."}

Use HTTPS and real authentication before exposing this service beyond a trusted development network. Do not put API keys, passwords, wallet secrets, or private keys in source code.
