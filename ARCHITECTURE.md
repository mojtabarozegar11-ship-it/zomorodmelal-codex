# Zomorod Melal Platform Architecture

## Source of truth
The production Django application lives under `django_project/`. Legacy `website/` remains compatibility-only until verified safe to remove.

## Runtime layers
- Django apps: business/domain functionality and HTTP/admin interfaces.
- Master Agent: orchestration, planning, execution policy, validation and reporting.
- AI layer: provider abstraction and task routing. New code should use `ai_engine/` as the canonical AI integration layer.
- Infrastructure: deployment, persistence and external adapters.

## Agent execution contract
```
Goal -> Plan -> Policy/Approval -> Agent/Tool -> Execute -> Validate -> Audit -> Report
                                    |-> deny / pause
```

Critical actions must pass the owner-approval boundary before execution. External AI is disabled by default.

## Migration rule
Do not add new provider implementations to both `ai_engine/` and `ai_providers/`. New integrations belong in `ai_engine/`. Existing `ai_providers/` code is compatibility code and should be migrated incrementally behind tests.

## Web/template rule
The Django project should converge on a shared base template and reusable components. Avoid adding new standalone HTML documents outside the canonical template system.

## Data/runtime evolution
SQLite is retained for MVP/offline operation. Production scale should move to PostgreSQL and a durable task queue/cache before high-volume workloads are enabled.
