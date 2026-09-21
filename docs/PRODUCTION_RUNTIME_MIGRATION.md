# Production Runtime Migration

## Canonical

Use only:

    python -m master_agent

This delegates to autonomous_core.MasterCore.

## Retired from production

### auto_agent/runtime

This tree contains an earlier scheduler/worker experiment. It has inconsistent
interfaces across modules, so it must not be used as a production launcher.

### orchestrator

The legacy orchestrator imports an older module layout that is not the
canonical package boundary.

## Migration rule

Do not add new production integrations to the retired runtimes. New
integrations must target master_agent.CanonicalMasterAgent and/or the
autonomous_core services.

## Safety

The migration does not grant credentials or enable external side effects.
Owner approval remains mandatory for any future external capability activation.
