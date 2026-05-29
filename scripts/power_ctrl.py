#!/usr/bin/env python3
import os
import sys
import time

# --- CONFIGURATION ---

TARGET_MAC = "aa:bb:cc:dd:ee:ff" 


TARGET_HOST = "100.64.0.1" 

# Your Ubuntu Username on the server
REMOTE_USER = "youruser"
# ---------------------

def wake_server():
    print(f"--- Sending Magic Packet to {TARGET_MAC} ---")
    # This sends the WoL packet via the local network
    os.system(f"wakeonlan {TARGET_MAC}")

def sleep_server():
    print(f"--- Sending Sleep Command to {TARGET_HOST} ---")
    # This uses SSH over Tailscale to tell Ubuntu to suspend
    # 'systemctl suspend' is the standard way to sleep Linux
    cmd = f"ssh {REMOTE_USER}@{TARGET_HOST} 'sudo systemctl suspend'"
    os.system(cmd)

def check_status():
    # Pings the Tailscale name to see if it's online
    response = os.system(f"ping -c 1 -W 1 {TARGET_HOST} > /dev/null")
    if response == 0:
        print(f"STATUS: {TARGET_HOST} is ONLINE.")
        return True
    else:
        print(f"STATUS: {TARGET_HOST} is OFFLINE.")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 power_ctrl.py [on|off|status]")
        sys.exit(1)

    action = sys.argv[1].lower()

    if action == "on":
        wake_server()
    elif action == "off":
        sleep_server()
    elif action == "status":
        check_status()
    else:
        print("Invalid command. Use 'on', 'off', or 'status'.")
