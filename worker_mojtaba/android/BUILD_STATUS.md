# Android Build Status

The GitHub Actions workflow is configured to build a debug APK. This file intentionally triggers the Worker Mojtaba Android workflow on the next push.


Build diagnostics updated: 2026-09-19.

SDK setup switched to runner-provided SDK.

Robust SDK discovery added.

AndroidX enabled for next build.

Java/Kotlin JVM targets aligned to 17.


## Current CI gate
Android CI now runs Gradle unit tests before assembling the debug APK. A successful APK must pass both the test task and assembleDebug before the artifact is considered valid.
