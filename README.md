# Zomorod Melal Master Agent Core

## Overview
Core execution framework and Django management layer for the Zomorod Melal Master Agent.

## Android Admin Panel
The repository now includes an Android-installable Progressive Web App (PWA) for the management panel:

- URL: `/mobile-admin/`
- Android Chrome can install it from the browser's install/add-to-home-screen flow.
- The app opens the Django Admin and AI configuration screens in a mobile-friendly management shell.
- DeepSeek API keys are entered through Django Admin and are never rendered back into the form.
- The DeepSeek provider reads the enabled configuration at runtime.
- External AI remains disabled unless `AI_PROVIDER_ENABLED=True` is explicitly configured.
- No API key is stored in GitHub, source code, APK, or frontend assets.

## Security Rule

OWNER APPROVAL REQUIRED BEFORE CRITICAL ACTION

Production deployment and external host actions remain gated by owner approval.

## Runtime
- Django admin: `/admin/`
- Android PWA admin: `/mobile-admin/`
- Agent API status: `/api/status/`
- Agent API execution: `/api/execute/`

## CI
MVP tests run on Python 3.8 through GitHub Actions.

## Remaining external setup
1. Run Django migrations on the target host.
2. Create/enable the admin account on the target host.
3. Open `/mobile-admin/` on Android and install the PWA.
4. Enter the DeepSeek API key through the secured admin form when ready.
5. Enable the provider only after the owner explicitly approves external AI use.
6. Configure production deployment credentials only after owner approval.

## Architecture

The repository follows a staged convergence model: `django_project/` is the primary Django application source of truth, `ai_engine/` is the canonical AI integration layer for new work, and `website/` plus `ai_providers/` are compatibility paths to be migrated only after import/test verification.

See `ARCHITECTURE.md`, `DESIGN_SYSTEM.md`, and `ARCHITECTURE_REFACTOR_PLAN.md` for the execution contract, approval boundary, UI system, and migration sequence.
