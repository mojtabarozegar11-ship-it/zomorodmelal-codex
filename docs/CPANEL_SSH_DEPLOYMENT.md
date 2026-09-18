# SSH cPanel deployment

The production deployment workflow connects to the cPanel account over SSH and updates the existing checkout in `DEPLOY_PATH`.

## Required GitHub Actions secrets

Create these secrets under **Settings → Secrets and variables → Actions**:

- `SSH_HOST` — SSH hostname, for example the server hostname (not the cPanel URL with port 2082).
- `SSH_PORT` — SSH port, usually `22`.
- `SSH_USER` — cPanel account username, for example `zomorodm`.
- `SSH_PRIVATE_KEY` — private key whose public key is authorized for the cPanel account.
- `SSH_KNOWN_HOSTS` — the verified host-key line(s) for the SSH server.
- `DEPLOY_PATH` — existing repository checkout, for example `/home/zomorodm/zomorodmelal-test`.

Do not commit any of these values to the repository.

## What the workflow does

1. Connects with strict host-key checking.
2. Fetches the repository.
3. Checks out `main` and resets it to `origin/main`.
4. Removes untracked files.
5. Uses `.venv`, `venv`, or the system Python available on the host.
6. Installs Django dependencies.
7. Runs migrations and collectstatic.
8. Runs `manage.py check`.

The workflow does not run until the required secrets exist.
