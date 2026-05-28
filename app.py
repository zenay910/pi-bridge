import logging
import subprocess
from datetime import datetime, timezone

from flask import Flask, jsonify

import config

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)


def run_script(path: str) -> tuple[int, str, str]:
    """Run a shell script and return (exit_code, stdout, stderr).

    Raises subprocess.TimeoutExpired if the script exceeds config.SCRIPT_TIMEOUT.
    Never uses shell=True; the path is passed directly to the OS.
    """
    logger.info("running script: %s", path)
    result = subprocess.run(
        [path],
        timeout=config.SCRIPT_TIMEOUT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        logger.warning(
            "script %s exited %d — stderr: %s",
            path,
            result.returncode,
            result.stderr.strip(),
        )
    return result.returncode, result.stdout, result.stderr


@app.get("/api/status")
def api_status():
    # Exit codes per project.md: 0=awake, 1=asleep, anything else=unknown
    try:
        code, _, stderr = run_script(config.STATUS_SCRIPT)
    except subprocess.TimeoutExpired:
        logger.error("status script timed out after %ds", config.SCRIPT_TIMEOUT)
        return jsonify({"error": "status_script_failed", "detail": "timeout"}), 500
    except OSError as exc:
        logger.error("status script could not be run: %s", exc)
        return jsonify({"error": "status_script_failed", "detail": str(exc)}), 500

    state = {0: "awake", 1: "asleep"}.get(code, "unknown")
    return jsonify({
        "state": state,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    })


def _run_action(script_path: str, action: str):
    """Shared handler for wake and suspend actions."""
    try:
        code, _, stderr = run_script(script_path)
    except subprocess.TimeoutExpired:
        logger.error("%s script timed out after %ds", action, config.SCRIPT_TIMEOUT)
        return jsonify({"error": f"{action}_script_failed", "detail": "timeout"}), 500
    except OSError as exc:
        logger.error("%s script could not be run: %s", action, exc)
        return jsonify({"error": f"{action}_script_failed", "detail": str(exc)}), 500

    if code == 0:
        return jsonify({"ok": True, "action": action})
    return jsonify({"ok": False, "action": action, "detail": stderr.strip()}), 502


@app.post("/api/wake")
def api_wake():
    return _run_action(config.WAKE_SCRIPT, "wake")


@app.post("/api/suspend")
def api_suspend():
    return _run_action(config.SUSPEND_SCRIPT, "suspend")


if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT)
