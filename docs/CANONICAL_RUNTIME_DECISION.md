# Canonical Android Runtime Decision

## Product target
Zomorod Melal is an installable Android application. Production execution occurs on the Android device.

## Canonical runtime
The production orchestration boundary is `master_agent.CanonicalMasterAgent`, backed by `autonomous_core.MasterCore`.

The Android application source/build boundary is `worker_mojtaba/android`.

## Removed from production path
- cPanel / Passenger deployment
- Hosted Django runtime as the production application
- Server deployment workflows
- Host deployment as a release criterion

Django and other server-side code may remain in the repository only as legacy/reference tooling until separately removed; they are not part of the Android production runtime.

## Release contract
A production-ready change must validate the canonical Master Agent checks and the Android Gradle test/build pipeline. The distributable outputs are APK for installation/testing and AAB for release distribution.

## Security
The Master Agent remains sandbox/control-plane oriented. External actions require explicit owner approval and are not enabled merely by building the Android application.
