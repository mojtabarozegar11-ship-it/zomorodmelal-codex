# Host Bridge connector contract

## Purpose
This repository contains the host-side bridge needed for an authenticated external client to inspect and modify files under the Django application root.

### Endpoint
- Base: `https://zomorodmelal.ir/host_bridge`
- File API: `POST /files.php`
- Authentication: `Authorization: Bearer <HOST_BRIDGE_TOKEN>`
- Contract: `host_bridge/openapi.yaml`

### Supported operations
- `status`
- `list_directory`
- `read_file`
- `file_info`
- `create_file`
- `write_file`
- `create_directory`
- `delete_file`

### Security boundary
The bridge is confined to `HOST_BRIDGE_ROOT` (default: `/home/zomorodm/zomorodmelal-app`). Path traversal is rejected. The API does not expose arbitrary shell execution, cPanel account credentials, database administration, or OS command execution.

### Required host setup
1. Deploy the `host_bridge/` directory to the live host.
2. Create a long random token at `/home/zomorodm/.host_bridge_token` or configure `HOST_BRIDGE_TOKEN` in the host environment.
3. Keep the token outside GitHub and outside the public web root.
4. Serve the endpoint only over HTTPS.
5. Prefer an IP/WAF restriction and rate limiting if the host supports them.
6. Confirm the PHP process can read the token and write the configured audit file.
7. Test `status`, then `list_directory`, then a harmless `read_file` before enabling writes.

### Important
Adding these files to GitHub does not itself grant ChatGPT runtime access to the host. A compatible authenticated Connector/Action/API must call this endpoint. Do not put the production token in GitHub, source code, issues, pull requests, or chat messages.
