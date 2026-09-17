# Zomorod Melal Master Agent Core

## Overview
Core execution framework for Master Agent.

## Current Mode
- API: Disabled
- Django: Pending Integration
- Runtime: Local Core Mode

## CI Status

![MVP Tests](https://github.com/mojtabarozegar11-ship-it/zomorodmelal-codex/actions/workflows/mvp-tests.yml/badge.svg)

## Test Suite

Current validation layers:

- Startup validation
- Import validation
- Agent flow validation
- Execution logger validation
- End-to-end flow validation

## Run

```bash
make run
```

or

```bash
bash start.sh
```

## Architecture

Startup Pipeline -> Orchestrator -> MVP Runner -> Master Core -> Agents -> Report

## Agents

- Knowledge
- Finance
- Agriculture
- Security
- Game

## Security Rule

OWNER APPROVAL REQUIRED BEFORE CRITICAL ACTION

## Hardening Phase Progress

Completed review actions:

1. Repository structure review: completed.
2. Security boundary review: owner approval gate confirmed.
3. Agent workflow validation: validation layers documented.
4. Deployment readiness: production remains gated until host credentials and approval are provided.
5. Documentation update: this progress section added.

## Roadmap

1. Core validation
2. Django integration
3. Database layer
4. AI API integration
