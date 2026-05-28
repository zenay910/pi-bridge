import os

HOST = os.environ.get("PI_BRIDGE_HOST", "0.0.0.0")
PORT = int(os.environ.get("PI_BRIDGE_PORT", "8080"))

STATUS_SCRIPT = os.environ.get("PI_BRIDGE_STATUS_SCRIPT", "./scripts/status.sh")
WAKE_SCRIPT = os.environ.get("PI_BRIDGE_WAKE_SCRIPT", "./scripts/wake.sh")
SUSPEND_SCRIPT = os.environ.get("PI_BRIDGE_SUSPEND_SCRIPT", "./scripts/suspend.sh")

# Seconds before subprocess.run raises TimeoutExpired
SCRIPT_TIMEOUT = int(os.environ.get("PI_BRIDGE_SCRIPT_TIMEOUT", "30"))
