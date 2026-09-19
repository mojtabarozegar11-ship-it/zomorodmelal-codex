# Zomorod 24/7

This repository uses GitHub Actions for continuous testing, cPanel simulation, nightly packaging, and automated failure reporting.

## Components

- `.github/workflows/ci.yml` — existing CI checks.
- `.github/workflows/cpanel-simulation.yml` — production/cPanel simulation.
- `.github/workflows/nightly.yml` — nightly tests and cPanel ZIP artifact.
- `.github/workflows/failure-report.yml` — creates an Issue when a monitored workflow fails.
- `scripts/run-tests.sh` — local Django test/check runner.
- `scripts/build-zip.sh` — creates `dist/zomorodmelal-cpanel.zip`.
- `scripts/collect-logs.sh` — creates a local failure report.
- `termux/watcher.sh` — lightweight Termux branch watcher.

## No OpenAI API required

This automation does not call the OpenAI API. GitHub Actions performs deterministic testing, packaging, and failure reporting. Semantic debugging and code changes can be handled interactively in ChatGPT using the connected GitHub repository.

## Termux

After cloning the repository:

```bash
chmod +x termux/watcher.sh
./termux/watcher.sh
```

Optional environment variables:

```bash
export REPO="$HOME/zomorodmelal-codex"
export BRANCH="fix/all-errors-2026-09-19"
export INTERVAL=300
```

## cPanel release gate

A ZIP artifact is produced only after the nightly test job reaches the build step. The cPanel simulation remains a separate production-style validation workflow.

For a real deployment, inspect the cPanel simulation and production logs before replacing the live package.
