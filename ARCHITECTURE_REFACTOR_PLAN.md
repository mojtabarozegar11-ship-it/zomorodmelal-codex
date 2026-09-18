# Architecture Refactor Plan

## Phase A — completed in this change
- Declare `django_project/` as the primary application source of truth.
- Declare `ai_engine/` as the canonical AI integration layer for new work.
- Document the Master Agent execution contract and approval boundary.
- Define the shared design-system direction.
- Keep legacy paths intact to avoid a destructive migration.

## Phase B — next implementation
- Introduce a single Master Agent orchestrator interface.
- Add policy objects for action classification and owner approval.
- Add a single provider manager/router facade over all supported providers.
- Add audit events for every execution transition.
- Add contract tests for denial, approval, execution, validation and rollback.

## Phase C — cleanup
- Migrate remaining `ai_providers/` consumers to `ai_engine/`.
- Migrate legacy `website/` consumers to `django_project/`.
- Remove duplicate modules only after CI proves there are no remaining imports.
- Reduce stale feature branches after confirming their changes are merged or obsolete.

## Non-goals
This refactor does not enable production deployment, external AI, financial execution or autonomous critical actions.
