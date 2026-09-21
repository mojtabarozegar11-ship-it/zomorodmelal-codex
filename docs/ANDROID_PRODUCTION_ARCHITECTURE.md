# Android Production Structure

The production product is the Android application.

## Canonical paths
- Android project: `worker_mojtaba/android`
- Android application module: `worker_mojtaba/android/app`
- Master Agent: `master_agent.CanonicalMasterAgent`
- Kernel: `autonomous_core.MasterCore`

## Removed from production
- cPanel
- Passenger/LiteSpeed deployment
- Hosted Django runtime
- Server deployment workflows as release gates

## CI contract
Android CI must run unit tests and produce:
- debug APK for device installation/testing
- release AAB for distribution

The Android app may call remote APIs when configured, but the Master Agent runtime itself is local to the device.
