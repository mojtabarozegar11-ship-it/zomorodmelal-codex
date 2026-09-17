# Phase 1 E2E Offline Test Plan

Goal: validate the full project flow without external AI API.

Flow:
Django -> API Layer -> Agent Service -> Master Agent Runtime -> Task Result

Checks:
- Django startup
- App loading
- Database readiness
- Agent runtime initialization
- Internal task execution
- Logging
- Permission boundary

AI Provider: Disabled
