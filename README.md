# pi-bridge

Minimal homelab dashboard and control bridge for a Raspberry Pi Zero 2 W. Serves a single web page over Tailscale with buttons to wake or suspend an Ubuntu server; status comes from shell scripts on the Pi.

## Requirements

- Python 3.10+ (stdlib + Flask only)
- Raspberry Pi Zero 2 W on your Tailscale tailnet (production target)
- On the Pi, for the power scripts:
  - `wakeonlan` — `sudo apt install wakeonlan`
  - SSH client and key-based auth to the Ubuntu server
  - Passwordless `sudo systemctl suspend` on the server for the suspend script

## Quick start (Pi)

### 1. Clone and create a virtual environment

```bash
git clone <your-repo-url> ~/pi-bridge
cd ~/pi-bridge
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` for your network. Do not commit `.env`.

| Variable | Purpose |
|----------|---------|
| `PI_BRIDGE_HOST` | Bind address (`0.0.0.0` so Tailscale can reach the app) |
| `PI_BRIDGE_PORT` | HTTP port (default `8080`) |
| `PI_BRIDGE_*_SCRIPT` | Paths to status / wake / suspend scripts |
| `PI_BRIDGE_SCRIPT_TIMEOUT` | Seconds before a script call fails |
| `PI_BRIDGE_TARGET_HOST` | Ubuntu server — use its **Tailscale IP** (or LAN IP if the Pi is always at home on that LAN) |
| `PI_BRIDGE_TARGET_MAC` | Server MAC for Wake-on-LAN |
| `PI_BRIDGE_REMOTE_USER` | SSH username on the Ubuntu server |

Export variables when running manually:

```bash
set -a && source .env && set +a
```

For a persistent service, use a systemd `EnvironmentFile` (see Phase 4 / T14 in `tasks.md`).

### 3. Scripts

The repo ships real scripts under `scripts/`:

| Script | Action |
|--------|--------|
| `scripts/status.sh` | `ping` the target host — exit `0` awake, `1` asleep |
| `scripts/wake.sh` | `wakeonlan` magic packet (must run from a host on the **same LAN** as the server) |
| `scripts/suspend.sh` | `ssh` to the server and run `sudo systemctl suspend` |

Make them executable:

```bash
chmod +x scripts/*.sh
```

Test each script before starting Flask (suspend only when safe):

```bash
source .env   # or: set -a && source .env && set +a
./scripts/status.sh; echo "exit: $?"
./scripts/wake.sh;   echo "exit: $?"
# ./scripts/suspend.sh; echo "exit: $?"   # only when you intend to suspend
```

**Tailscale notes**

- Open the dashboard at `http://<pi-tailscale-ip>:8080/` from any device on your tailnet.
- Set `PI_BRIDGE_TARGET_HOST` to the Ubuntu server’s **Tailscale IP** for status and suspend from anywhere on the tailnet.
- Wake-on-LAN does **not** traverse Tailscale; the Pi must stay at home on the LAN where the server lives.

**SSH setup (suspend script)**

From the Pi, passwordless SSH to the server:

```bash
ssh-copy-id youruser@<server-tailscale-or-lan-ip>
ssh youruser@<host> 'sudo systemctl suspend'   # one-time test; server will sleep
```

On the server, allow suspend without a password prompt (example — adjust user/group):

```bash
# /etc/sudoers.d/pi-bridge-suspend
youruser ALL=(ALL) NOPASSWD: /bin/systemctl suspend
```

### 4. Run the app

With the venv active and `.env` exported:

```bash
python3 app.py
```

Then from a phone or laptop on Tailscale:

```
http://<pi-tailscale-ip>:8080/
```

Find the Pi’s Tailscale IP with `tailscale ip -4` on the Pi, or in the Tailscale admin console.

### 5. Local development (laptop)

You can run the same steps on a laptop to develop the UI and API:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env — use the server Tailscale IP for PI_BRIDGE_TARGET_HOST when away from home
set -a && source .env && set +a
python3 app.py
```

Open `http://127.0.0.1:8080/`. Status and suspend can work over Tailscale; WoL still requires being on the home LAN (use the Pi for real WoL).

## API (for debugging)

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Dashboard HTML |
| `GET` | `/api/status` | JSON: `{ "state": "awake\|asleep\|unknown", "checked_at": "..." }` |
| `POST` | `/api/wake` | Run wake script |
| `POST` | `/api/suspend` | Run suspend script |

Example:

```bash
curl -s http://127.0.0.1:8080/api/status | python3 -m json.tool
```

## Project docs

- [`project.md`](project.md) — architecture, API contract, UI spec
- [`tasks.md`](tasks.md) — build checklist
- [`AGENTS.md`](AGENTS.md) — agent execution rules
