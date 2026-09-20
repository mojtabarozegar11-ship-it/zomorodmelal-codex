# Host Bridge

Read-only deployment diagnostics bridge for the Zomorod Melal cPanel/LiteSpeed host.

## Purpose

This bridge receives a small, sanitized deployment-status report from GitHub Actions and exposes the latest diagnostic status as JSON so it can be inspected remotely.

It does **not** execute shell commands, Git commands, cPanel commands, or arbitrary code.

## cPanel layout

Recommended deployment:

```
/home/zomorodm/
├── .zomorod_bridge/
│   └── git-status.json
└── public_html/
    └── git-bridge/
        ├── status.php
        ├── receive.php
        └── .htaccess
```

The PHP files can be copied into the public web root. The data directory should remain outside the web root.

## Configuration

Set these environment variables in the PHP/cPanel environment when available:

- `GIT_BRIDGE_WEBHOOK_SECRET` — high-entropy secret used by GitHub Actions when posting reports.
- `GIT_BRIDGE_READ_TOKEN` — optional read token. If set, status.php requires `Authorization: Bearer <token>`.

If the hosting panel cannot expose environment variables to PHP, configure them in a server-side file outside the public web root. Never commit secrets to Git.

## Endpoints

- `POST /git-bridge/receive.php` — receives a signed JSON report.
- `GET /git-bridge/status.php` — returns the latest sanitized report.
- `GET /git-bridge/status.php?health=1` — lightweight health response.

## GitHub setup

Create repository/environment secrets rather than putting credentials in workflow YAML. Suggested names:

- `HOST_BRIDGE_URL`
- `HOST_BRIDGE_TOKEN`

The workflow should POST only deployment metadata and the final error summary, not secrets or complete environment dumps.

GitHub recommends webhook secrets/secure secret storage and HTTPS for webhook-style integrations.
