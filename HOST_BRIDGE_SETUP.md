# Host Bridge setup

The authenticated file API is `host_bridge/files.php`.

It supports controlled read/list/create/update/delete operations inside `/home/zomorodm/zomorodmelal-app` and rejects path traversal. It does not execute arbitrary shell commands.

Configure `HOST_BRIDGE_TOKEN_FILE=/home/zomorodm/.host_bridge_token` or `HOST_BRIDGE_TOKEN` outside GitHub. The token file must contain only the random token.

Optional: `HOST_BRIDGE_ROOT`, `HOST_BRIDGE_AUDIT_FILE`, `HOST_BRIDGE_MAX_READ_BYTES`, `HOST_BRIDGE_MAX_WRITE_BYTES`.

Every file API request requires `Authorization: Bearer <token>`.

Example body: `{"action":"read_file","path":"config/settings.py"}`

The bridge itself does not grant the ChatGPT product automatic access. A compatible authenticated Connector/Action/API must be configured separately.

Never commit or send the production token in chat.
