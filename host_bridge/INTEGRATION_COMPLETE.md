# Host Bridge — Final integration layer

This directory is the host-side integration boundary between the live cPanel Django deployment and an authenticated external Connector/Action.

## Contract

Live URL when deployed and mapped by cPanel/LiteSpeed:
`https://zomorodmelal.ir/host_bridge/files.php`

Authentication:
`Authorization: Bearer <HOST_BRIDGE_TOKEN>`

Supported file operations:
- `status`
- `list_directory`
- `read_file`
- `write_file`
- `create_file`
- `create_directory`
- `delete_file`
- `file_info`

The OpenAPI contract in `openapi.yaml` is the source of the client-facing operation contract.

## Security boundary

The bridge is confined to:
`/home/zomorodm/zomorodmelal-app/django_project`
unless `HOST_BRIDGE_ROOT` is explicitly configured.

The bridge:
- rejects path traversal;
- requires a bearer token;
- never exposes arbitrary OS shell execution;
- writes audit events outside the web root when configured;
- uses configurable read/write size limits;
- serves no directory indexes;
- blocks direct web access to installation scripts, documentation, logs, and JSON diagnostics.

Production token location:
`/home/zomorodm/.host_bridge_token`
or the `HOST_BRIDGE_TOKEN` environment variable.

Never commit or paste the production token into GitHub or chat.

## Health endpoint

`health.php` is protected by the same bearer token by default. Set `HOST_BRIDGE_HEALTH_PRIVATE=0` only when a public health probe is explicitly required.

The health response intentionally does not disclose whether a token is configured.

## Deployment prerequisites

1. Deploy `host_bridge/` into a web-accessible path that actually maps to `/host_bridge` on the live domain.
2. Configure the token outside the repository.
3. Confirm HTTPS and LiteSpeed/Passenger routing.
4. Test `status`.
5. Test `list_directory`.
6. Test a harmless `read_file`.
7. Only then enable write operations for the external client.

The repository can validate source/configuration and build a cPanel package. It cannot prove live cPanel, DNS, TLS, LiteSpeed/Passenger mapping, or a live ChatGPT-to-bridge session by itself.

Deployment/restart/migration commands remain a separate allowlisted mechanism; arbitrary shell execution is intentionally not added to the bridge.
