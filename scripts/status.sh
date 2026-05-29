#!/usr/bin/env bash
# Checks if the server is reachable via ping.
# Exit contract (project.md): 0=awake, 1=asleep, 2=unknown
TARGET_HOST="${PI_BRIDGE_TARGET_HOST:-100.64.0.1}"

ping -c 1 -W 2 "$TARGET_HOST" > /dev/null 2>&1
case $? in
  0) echo "online"; exit 0 ;;
  1) echo "offline"; exit 1 ;;
  *) echo "unknown"; exit 2 ;;
esac
