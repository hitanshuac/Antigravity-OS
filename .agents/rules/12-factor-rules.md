---
name: 12-Factor Governance
description: Enforces all 12 factors of the 12-Factor App methodology for AI-generated architectural changes.
---

# 12-Factor App Methodology

When generating code, scaffolding architecture, or debugging issues within this repository, you MUST adhere to **all twelve** of the following principles. This repository is not a script; it is a **Production-Ready Agentic Environment**.

## Factor I: Codebase
*One codebase tracked in revision control, many deploys.*
- All architectural logic, including this very rule file, must be tracked in version control.
- Ensure the `.agents` folder is accurately updated when AI behavior needs to change globally.
- There is exactly one canonical repository. Deploys (dev, staging, production, HF Spaces) are all derived from this single codebase.

## Factor II: Dependencies
*Explicitly declare and isolate dependencies.*
- All Python dependencies must be declared in `requirements.txt` with pinned or range-locked versions.
- Never rely on implicit system-level packages. If a skill or workflow requires a library, it must be in `requirements.txt`.
- Use virtual environments (`.venv/`) for local isolation. The `.gitignore` must exclude `.venv/`.

## Factor III: Config
*Store config in the environment.*
- **STRICT PROHIBITION**: You are strictly forbidden from hardcoding API keys, secrets, or environment-specific connection strings into the source code (`src/`).
- Use the **BYOK (Bring Your Own Keys)** strategy. Configuration must be injected dynamically via environment variables (`os.environ`), `.secrets/` text files, or the `.config/antigravity/project_settings.toml` manifest.
- Config that varies between deploys (database URLs, API keys, ports) must never be committed to the repository.

## Factor IV: Backing Services
*Treat backing services as attached resources.*
- DuckDB databases, external APIs, message queues, and any third-party service must be treated as attached resources addressable via a URL or connection string stored in config (Factor III).
- The application must be able to swap a local DuckDB instance for a remote MotherDuck endpoint without code changes — only config changes.
- No backing service MUST be treated as "special." Local and third-party services are interchangeable.

## Factor V: Build, Release, Run
*Strictly separate build and run stages.*
- **Build:** Install dependencies, compile assets, run linting (`ruff check .`) and SAST (`semgrep ci`).
- **Release:** Combine the build with deploy-specific config. Tag with a semantic version via `python-semantic-release`.
- **Run:** Execute the application in the target environment. The run stage must never modify source code.
- These stages are strictly separated. You cannot patch code at runtime.

## Factor VI: Processes
*Execute the app as one or more stateless processes.*
- The application (e.g., FastAPI gateway) must execute **statelessly**.
- The router MUST hold no memory of past requests.
- Stateful persistence must be delegated to backing services (e.g., DuckDB telemetry, Parquet Dead-Letter Queues).
- Never store session state in local memory or the filesystem within `src/`.

## Factor VII: Port Binding
*Export services via port binding.*
- The application must be self-contained and bind to a port to serve requests.
- For Hugging Face Spaces: bind to `0.0.0.0:7860` (see `hf-deployment-standards.md`).
- For local development: bind to `0.0.0.0:8000` (or as configured via environment variable `PORT`).
- No external web server injection (e.g., Apache, Nginx) MUST be assumed at the application layer.

## Factor VIII: Concurrency
*Scale out via the process model.*
- Design for horizontal scalability. Each process MUST be stateless (Factor VI) and disposable (Factor IX).
- On constrained environments (HF Spaces free tier), run a single worker (`--workers 1`) to avoid OOM kills.
- On production environments, scale by increasing the number of identical worker processes, not by adding threads to a monolith.

## Factor IX: Disposability
*Maximize robustness with fast startup and graceful shutdown.*
- Systems must gracefully handle sudden provider crashes.
- Do not let the main event loop freeze.
- Rely on Circuit Breakers (`error-recovery.md`) and Dead-Letter Queues (`data/quarantine_*.parquet`) to isolate faults and keep the system alive.
- Startup must be fast. Shutdown must flush all pending DuckDB WAL writes before exiting.

## Factor X: Dev/Prod Parity
*Keep development, staging, and production as similar as possible.*
- The same DuckDB schemas, Pydantic models, and FastAPI routes must be used across all environments.
- Avoid "works on my machine" by using the same `requirements.txt`, `ruff.toml`, and `.pre-commit-config.yaml` everywhere.
- Time gap (deploy quickly), personnel gap (developers who wrote it deploy it), and tools gap (same database engine everywhere) must all be minimized.

## Factor XI: Logs
*Treat logs as event streams.*
- Treat logs as continuous event streams. Never write to local log files within `src/`.
- Use lock-free background threadpools to push telemetry directly to the DuckDB metrics plane.
- In production, logs are captured by the runtime environment (Docker, HF Spaces). The application only writes to `stdout`/`stderr`.
- Document immutable architectural decisions natively in ADRs (`.agents/architecture/adrs/`).

### Factor XI Addendum: Lightweight Contexts
When 12-Factor Factor XI conflicts with project constraints that prohibit databases (see `rule-conflict-resolution.md` for priority hierarchy):
- Logs MAY be written to local JSON files as a fallback, but MUST still follow the Pydantic schema validation mandate from `data-validation.md` Rule 4 and `defensive-programming.md` Rule 1.
- The JSON log file is treated as a "poor man's event stream" and must be **append-only**. The agent must NEVER truncate, overwrite, or reset existing log entries.
- Before writing, a `.bak` backup must be created per `error-recovery.md` Step 3b.
- After writing, the Pre-Write Verification gate (`error-observability.md` Step 1.5) must confirm data integrity.

## Factor XII: Admin Processes
*Run admin/management tasks as one-off processes.*
- Database migrations, one-time data fixes, and diagnostic scripts must be run as isolated one-off commands, not baked into the application startup.
- Admin scripts MUST live in a dedicated `scripts/` directory (or be invoked via `python -m`) and use the same codebase and config as the running application.
- Never modify production data via ad-hoc SQL. Use versioned migration scripts that are idempotent.
