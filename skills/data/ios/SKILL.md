---
name: ios
description: Deploy iOS app to physical iPhone over WiFi. Use when user asks about running on phone, running on iPhone, deploying to device, or testing on their physical phone. For simulator, use ios-simulator skill instead.
allowed-tools: Bash(cd:*), Bash(./scripts/*), Bash(xcrun:*), Bash(xcodebuild:*), Bash(curl:*)
---

# iOS Physical Device Deployment

**This is an action skill. Offer to run commands, don't just explain them.**

When user asks to run on their phone/device:

1. **Check prerequisites** before running:
   - Verify device is visible with `xcrun devicectl list devices`
   - Check daemon is running: `curl -s localhost:47100/health`
2. **Run the deployment** after confirming with user

## Commands

**Physical iPhone:**
```bash
cd apps/ios && ./scripts/run-device.sh
```

For simulator testing, use the `ios-simulator` skill instead.

## Typical Flow

User: "run this on my phone"

You: "I can deploy to your iPhone over WiFi. Let me check if your device is connected..."
[Run: `xcrun devicectl list devices`]

If device found:
"Found [device name]. Want me to build and deploy now?"
[If yes, run: `cd apps/ios && ./scripts/run-device.sh`]

If no device:
"No device found. Your iPhone needs to be:
- On the same WiFi as your Mac
- Paired in Xcode (Devices & Simulators → Connect via network)

Want me to try the simulator instead?"

## Troubleshooting

**"No device found":** Pair device via USB first, enable "Connect via network" in Xcode, then disconnect USB.

**App can't connect to daemon:** Check daemon is running, Mac firewall allows connections, same network.

**Need logs over WiFi:** Use `os_log` instead of `print()`. See `apps/ios/DEBUGGING_OVER_WIFI.md`.
