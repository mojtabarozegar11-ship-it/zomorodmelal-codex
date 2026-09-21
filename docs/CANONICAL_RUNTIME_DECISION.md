# Canonical Runtime Decision

## Decision

The production path is one runtime:

- Public entry point: python -m master_agent
- Runtime facade: master_agent.CanonicalMasterAgent
- Canonical kernel: autonomous_core.MasterCore

The existing auto_agent/runtime and legacy orchestrator implementations are not
production entry points. They remain temporarily for migration and historical
compatibility.

## Production boundary

The canonical runtime is a control-plane runtime. A cycle can discover, audit,
plan, delegate, test and verify in the sandbox, but it does not perform
real-world writes by default. External capabilities continue to pass through
the existing access manager, approval context and activation gate.

## Required commands

    python -m master_agent --check
    python -m master_agent --status
    python -m master_agent --once --goal "validate the production stack"

## Acceptance criteria

1. Canonical kernel imports successfully.
2. Python syntax audit completes.
3. The public runtime entry point starts deterministically.
4. No parallel runtime is used by production workflows.
5. External execution remains disabled until explicit owner approval.
6. CI installs real project dependencies before integration tests.
7. Django system checks and the Master Agent smoke test run in CI.
