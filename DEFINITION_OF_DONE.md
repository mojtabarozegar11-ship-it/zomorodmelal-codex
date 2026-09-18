# 100% Definition of Done

This repository uses explicit, testable completion criteria. A component is considered complete only when its code path exists, is documented, and has automated verification where practical.

## Project
- Canonical Django application identified.
- Canonical Master Agent entry point identified.
- Canonical AI integration layer identified.
- CI and migration checks present.
- Production operations remain approval-gated.

## Website
- Django apps provide the domain modules.
- RTL/Persian direction is defined.
- Shared design-system direction is documented.
- Legacy website is compatibility-only pending verified migration.

## Agent
- Orchestrator supports plan, approval gate, execution, validation and audit reporting.
- Critical actions are denied without explicit approval.
- Runtime tests cover approval denial and successful/failed validation.

## Environment-dependent items
External host credentials, DNS/SSL, production database, provider API keys and real third-party services cannot be truthfully marked as operational solely from repository state. They are deployment prerequisites and must remain disabled until configured by the owner.
