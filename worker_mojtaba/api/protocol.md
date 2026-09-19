# Android ↔ Core protocol

1. Android creates a request ID.
2. Request contains text, optional attachments and context.
3. Core plans the task and selects a capability.
4. Execution status is returned to Android.
5. Results/artifacts are returned when execution is complete.

The production transport can be REST, WebSocket or another authenticated channel; this module intentionally does not embed credentials.
