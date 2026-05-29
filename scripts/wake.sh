#!/usr/bin/env bash
# Sends a Wake-on-LAN magic packet via wakeonlan.
# Requires: wakeonlan package (sudo apt install wakeonlan)
# Exit contract: 0=packet sent, non-zero=failure
TARGET_MAC="${PI_BRIDGE_TARGET_MAC:-aa:bb:cc:dd:ee:ff}"

wakeonlan "$TARGET_MAC"
exit $?
