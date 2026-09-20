# Host Bridge — Complete integration layer

This directory is the host-side integration boundary between the live cPanel Django deployment and an authenticated external Connector/Action.

## Live endpoint
`https://zomorodmelal.ir/host_bridge/files.php`

## Authentication
Every file API request uses:
`Authorization: Bearer <HOST_BRIDGE_TOKEN>`

The production token is never stored in this repository. On cPanel, configure either:
- `HOST_BRIDGE_TOKEN`
- `HOST_BRIDGE_TOKEN_FILE=/home/zomorodm/.host_bridge_token`

## File permissions
The API is confined to:
`/home/zomorodm/zomorodmelal-app/django_project`
unless `HOST_BRIDGE_ROOT` is explicitly configured.

Supported actions are defined in `openapi.yaml`.

## Deployment
The cPanel package workflow includes `host_bridge/`. The live host must expose the endpoint over HTTPS and make the token available to PHP.

## Security
The bridge rejects traversal outside the project root and does not expose arbitrary OS command execution. Audit records are written outside the web root when configured.

## Operational sequence
1. Install `host_bridge/` under the public web root on the host.
2. Configure the production token outside the repository.
3. Confirm HTTPS.
4. Test `status`.
5. Test `list_directory`.
6. Test a harmless `read_file`.
7. Enable client write operations.
8. Keep deployment/restart/migration actions behind a separate allowlisted deployment mechanism; they are intentionally not implemented as arbitrary shell execution here.
