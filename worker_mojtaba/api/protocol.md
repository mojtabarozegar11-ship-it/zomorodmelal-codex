# Android ↔ Core protocol

1. Android creates a request ID.
2. Request contains text, optional attachments and context.
3. Core plans the task and selects a capability.
4. Execution status is returned to Android.
5. Results/artifacts are returned when execution is complete.

The production transport can be REST, WebSocket or another authenticated channel; this module intentionally does not embed credentials.


## Tool Center

The service owns an explicit Tool Center for provider-backed capabilities.
- Only registered adapters may execute.
- Unknown adapters/capabilities are rejected.
- Media generation remains provider_required until an authorized provider is configured.
- Provider credentials are supplied through secure runtime configuration, not source code.


## Task response
The task endpoint returns the selected intent/capability, execution status, AI status, plan and registered Tool Center names. Android clients may send a JSON `context` object; it is carried through the response and does not contain credentials.
