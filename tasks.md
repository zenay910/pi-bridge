# pi-bridge — Build tasks (v1, ~2 hours)

Execute **one task at a time**. Check the box only after **Verify** passes and a human confirms.

---

## Phase 0 — Reasoning layer (this session)

- [x] **T0** — `AGENTS.md`, `project.md`, `tasks.md` committed to repo root  
  **Verify:** Files exist and match `project.md` scope (no extra features).

---

## Phase 1 — Project skeleton (~15 min)

- [x] **T1** — Create `requirements.txt` with pinned `flask` (e.g. `flask>=3.0,<4`)  
  **Verify:** `pip install -r requirements.txt` succeeds in a venv.

- [x] **T2** — Create `.env.example` with all variables from `project.md`  
  **Verify:** Copy to `.env` locally; values are documented.

- [x] **T3** — Create `config.py` reading env vars with defaults from `project.md`  
  **Verify:** `python3 -c "import config; print(config.PORT)"` prints default.

- [x] **T4** — Add `scripts/status.sh`, `scripts/wake.sh`, `scripts/suspend.sh` **stubs** that echo and exit 0/1 for local dev (or document "skip stubs" if using real scripts on Pi only)  
  **Verify:** `chmod +x scripts/*.sh` and `./scripts/status.sh; echo $?` works.

- [x] **T5** — On the Pi: copy or symlink **real** scripts to match `PI_BRIDGE_*_SCRIPT` paths; set `.env`  
  **Verify:** Run each script manually over SSH; exit codes match contract in `project.md`.

---

## Phase 2 — Backend (~35 min)

- [x] **T6** — Create `app.py` with Flask app factory or single `app`, `run_script()` helper (`subprocess.run`, timeout from config, no `shell=True`)  
  **Verify:** `python3 -m py_compile app.py`

- [X] **T7** — Implement `GET /api/status` (map exit 0→awake, 1→asleep, else→unknown; ISO `checked_at`)  
  **Verify:** `curl -s http://127.0.0.1:8080/api/status | python3 -m json.tool`

- [X] **T8** — Implement `POST /api/wake` and `POST /api/suspend` (200 on exit 0, 502 on non-zero, 500 on timeout)  
  **Verify:** `curl -s -X POST http://127.0.0.1:8080/api/wake` and suspend return expected JSON.

- [x] **T9** — Add `if __name__ == '__main__'` entry using `config.HOST`/`config.PORT`  
  **Verify:** `python3 app.py` starts; endpoints respond locally.

---

## Phase 3 — UI (~30 min)

- [x] **T10** — Create `templates/index.html`: semantic layout, Tailwind CDN, status card + action buttons per `project.md`  
  **Verify:** Open `/` in browser; page renders without console errors.

- [x] **T11** — Wire `fetch` for status, refresh, wake, suspend (loading/disabled states, 60s auto-refresh, 3s post-action refresh)  
  **Verify:** Buttons call API; status pill updates; errors show a simple message.

- [x] **T12** — Implement `GET /` route rendering `index.html`  
  **Verify:** `/` and `/api/status` both work in one running process.

---

## Phase 4 — Pi deployment & verification (~25 min)

- [x] **T13** — Add `README.md` section: venv, `.env`, run command, Tailscale URL, script setup  
  **Verify:** Another reader can follow steps without chat context.

- [x] **T14** — Create `systemd` unit example in README (or `deploy/pi-bridge.service`): `WorkingDirectory`, `EnvironmentFile`, `ExecStart=/path/to/venv/bin/python3 app.py`, restart on failure  
  **Verify:** `sudo systemctl enable --now` on Pi; service stays running after reboot (human test).

- [ ] **T15** — **End-to-end on Tailscale:** from phone/laptop, open dashboard, confirm status matches reality, test wake and suspend (only when safe)  
  **Verify:** All success criteria in `project.md` met.

---

## Phase 5 — Optional hardening (only if time remains; still v1)

- [ ] **T16** — Bind check: document Pi firewall (`ufw allow` only on `tailscale0` or tailnet IP) in README  
  **Verify:** Port not reachable from LAN WAN interface (human checks).

---

## Task rules

- Do not skip human **Verify** between tasks.
- Do not batch multiple tasks in one commit unless the human explicitly allows it.
- If a task fails, fix only that task's scope—no drive-by refactors.
