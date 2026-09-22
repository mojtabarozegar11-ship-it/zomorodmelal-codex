# Zomorod Melal — Master Agent + Website

Unified Django website and Master Agent operational architecture.

## Release policy
- No production claim without runtime evidence.
- Secrets must be supplied through environment variables.
- Sensitive actions remain approval-gated and audited.
- Public content is published on the website/social surfaces; the control plane remains private.

## Deployment
The cPanel/Passenger deployment package is maintained separately from source release artifacts.

## Quality gates
Syntax, unit/integration tests, Django checks, database migrations, static collection, Passenger runtime, browser E2E, security and production smoke tests are required before a production release is certified.
