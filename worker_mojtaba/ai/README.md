# AI Provider Integration

Worker Mojtaba supports provider adapters without storing credentials in source code.

## Configuration contract

- Provider endpoint: HTTPS URL.
- API credential: environment variable or platform secret.
- The worker must never print, persist, or return the credential.
- If authentication is missing, the provider returns `provider_auth_required`.
- Provider failures return a bounded status rather than exposing response secrets.

Use `HTTPJSONProvider` for services that accept a JSON POST request and bearer-style authentication. Provider-specific payload/response mapping can be implemented as a dedicated adapter when required.
