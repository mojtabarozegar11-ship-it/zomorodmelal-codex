# Android/Core Contract

Request fields:
- request_id
- text
- attachments
- context

Response fields:
- request_id
- status
- message
- artifacts

Rules:
- No API keys or private keys in source code.
- Device capabilities are exposed through adapters.
- Authentication belongs to the deployment environment.
