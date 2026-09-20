# Host Bridge — ChatGPT handoff

This repository now contains an explicit connector manifest at
`host_bridge/connector-manifest.json`.

## Live prerequisites

The host must serve:

`https://zomorodmelal.ir/host_bridge/files.php`

and expose the authenticated JSON API described by
`host_bridge/openapi.yaml`.

Required host-side secret:

`/home/zomorodm/.host_bridge_token`

The production token must never be committed to GitHub or pasted into chat.

## Verification sequence

1. GET `/host_bridge/health.php` with `Authorization: Bearer <token>`.
2. GET `/host_bridge/status.php?health=1` with the same token.
3. POST `{"action":"status"}` to `/host_bridge/files.php`.
4. POST `{"action":"read_file","path":"passenger_wsgi.py"}`.
5. Only after successful read verification enable write operations.

## Important

GitHub changes alone cannot create a runtime connector inside ChatGPT. A compatible external Connector/Action must be registered against this HTTPS endpoint and supplied the token through its secret store.

Once the Connector is active, the first live diagnostic should inspect:
- cPanel application root `/home/zomorodm/zomorodmelal-app` existence
- Passenger entrypoint
- Python runtime/dependencies
- Django settings
- restart marker
- recent application logs available to the connector

Do not expose cPanel credentials or arbitrary shell execution through this bridge.
