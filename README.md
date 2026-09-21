# Zomorod Melal — Android Master Agent

## Product
Zomorod Melal is an **Android application installed on a mobile device**.

The production runtime is local to Android. The project is **not deployed to cPanel, Passenger, or a web host**.

## Canonical architecture

`Android App → Canonical Master Agent → autonomous_core.MasterCore → task/worker orchestration → device-local state`

The canonical application/runtime boundary is:

- Android project: `worker_mojtaba/android`
- Master Agent entry point: `master_agent.CanonicalMasterAgent`
- Python orchestration kernel: `autonomous_core.MasterCore`

Network/API integrations are optional capabilities of the application; they are not the location where the Master Agent runs.

## Build outputs

- **APK**: install directly on an Android device for testing/installation.
- **AAB**: release bundle for app distribution.

The GitHub Actions Android pipeline validates the Gradle project, runs Android unit tests, and builds both debug APK and release AAB.

## Production rules

- No cPanel deployment.
- No Passenger/Django host runtime.
- No server deployment as a production gate.
- No credentials embedded in the APK or source tree.
- Critical external actions remain behind explicit owner approval.

## Legacy code
Server/Django directories may still exist while migration cleanup is completed. They are not production runtime dependencies for the Android application.
