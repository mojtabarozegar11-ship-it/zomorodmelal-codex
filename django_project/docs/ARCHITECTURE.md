# Architecture Standard

## Canonical application
Production web application: `django_project/`.

Legacy/reference trees must not be deployed alongside the canonical application.

## Layers
- Presentation: Django templates, PWA, future native clients.
- API: versioned REST contract under `/api/v1/`.
- Domain: one Django app per bounded business domain.
- Platform: identity, RBAC, owner approval, audit, events, notifications.
- Integration: provider adapters with explicit capability/status.
- Data: PostgreSQL in production; Redis/queue/object storage as required.

## Cross-cutting invariants
1. Sensitive actions require owner approval.
2. Real financial execution is disabled by default.
3. Secrets live outside source control.
4. Provider calls are auditable and idempotent.
5. Published financial content has compliance metadata.
6. Every production mutation has an actor and audit event.

## Domain boundaries
- agriculture
- economy
- office
- marketplace
- encyclopedia
- research
- services
- studio
- ai

No domain should directly mutate another domain's tables without an explicit service boundary.
