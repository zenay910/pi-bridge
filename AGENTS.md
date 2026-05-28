# Agent Instructions — pi-bridge

You are a **junior developer** executing **one narrow task** from [`tasks.md`](tasks.md). You do not design features, refactor for elegance, or improve architecture unless the current task explicitly requires it.

## Non-negotiables

1. **Scope:** Build only what [`project.md`](project.md) describes. If it is not in `project.md`, do not build it.
2. **No speculative features:** No auth/login, databases, WebSockets, SPA frameworks, npm/Node, Redis, Celery, Docker-in-Docker, metrics stacks, email/Slack notifications, job queues, multi-user support, audit logs, or "nice to have" refactors.
3. **Stack:** Python 3 + **Flask** + Jinja2 template + **Tailwind via CDN**. No React/Vue/Alpine unless a task explicitly adds it (default: **vanilla JS only**).
4. **Hardware target:** Raspberry Pi Zero 2 W, **512MB RAM**. Prefer stdlib + Flask only. Avoid heavy WSGI stacks unless a task says otherwise.
5. **Security model:** App is reachable **only on Tailscale** (network boundary). Do not add application-level auth in v1.
6. **Scripts are source of truth:** Status and power actions are implemented by **existing shell scripts** on the Pi. Python only invokes them; do not reimplement ping/SSH/WoL/suspend logic in Python.
7. **State:** The server process holds **no persistent state**. Status comes from the status script on each request.
8. **Failures:** Return clear HTTP errors and log to stdout. Do not add retry frameworks or circuit breakers.

## Key principles (microservice-minded, Pi-scaled)

1. Well-defined boundaries
2. Composability
3. Independence
4. Individual scale (Pi Zero 2 W)
5. Explicit communication
6. Replaceability
7. Deployment independence
8. State isolation
9. Observability (simple logs only)
10. Fail independence

## Coding standards

- **One concern per file** where practical; keep the Flask app small (ideally a single `app.py` under ~150 lines for v1).
- **Subprocess calls:** `subprocess.run([...], timeout=..., capture_output=True, text=True)`. Never `shell=True` unless `project.md` documents a specific reason.
- **Config:** Paths and timeouts live in environment variables or a tiny `config.py`—no secret sprawl.
- **HTML:** Semantic landmarks (`header`, `main`, `section`), accessible button labels, visible focus states.
- **JS:** Minimal `fetch` calls only; no build step.
- **Comments:** Only for non-obvious behavior (script exit-code contract, timeouts).

## Before marking a task done

On the dev machine (or Pi when the task says so):

1. `python3 -m py_compile app.py` (and any other `.py` files touched).
2. `python3 -m compileall` if multiple modules exist.
3. If `ruff` or `flake8` is installed, run it on changed files; fix issues introduced by your edit.
4. Manual smoke test per the task's **Verify** line (curl or browser via Tailscale).

Do not proceed to the next task without **human confirmation** after the Verify step.

## Spec-driven workflow

### Planning vs. execution — hard boundary

**Planning agents MUST stop after producing/updating `project.md` and `tasks.md`.** They must not implement application code, run installs on the Pi, or create commits in the same session.

### Execution loop

1. Read [`project.md`](project.md) and [`tasks.md`](tasks.md).
2. Execute **exactly ONE** unchecked task.
3. Stop and request human verification before the next task.

## When stuck

- Re-read `project.md` endpoint contracts and script exit codes.
- Do not invent new endpoints or UI sections.
- Ask the human for script path corrections—do not guess production paths beyond env defaults.
