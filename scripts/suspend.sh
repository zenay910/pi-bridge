#!/usr/bin/env bash
# Sends a suspend command to the server over SSH.
# Requires: passwordless SSH key auth + passwordless sudo for systemctl on the server.
# -o BatchMode=yes prevents SSH from hanging on a password prompt in a non-interactive subprocess.
# Exit contract: 0=command sent, non-zero=failure (SSH error or sudo denied)
TARGET_HOST="${PI_BRIDGE_TARGET_HOST:-100.64.0.1}"
REMOTE_USER="${PI_BRIDGE_REMOTE_USER:-youruser}"

ssh -o BatchMode=yes -o ConnectTimeout=10 "${REMOTE_USER}@${TARGET_HOST}" 'sudo systemctl suspend'
exit $?
