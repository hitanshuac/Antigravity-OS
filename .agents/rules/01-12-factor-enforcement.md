# 12-Factor App Enforcement

This rule mandates that all code deployed within the Agentic Environment strictly adheres to the 12-Factor App methodology.

## Key Directives

1. **Codebase:** One codebase tracked in revision control, many deploys.
2. **Dependencies:** Explicitly declare and isolate dependencies (e.g., `requirements.txt`).
3. **Config:** Store configuration in the environment. **NEVER hardcode API keys or secrets.** Use `.env` locally or GitHub Secrets in CI/CD.
4. **Backing Services:** Treat backing services (databases, caches) as attached resources.
5. **Build, Release, Run:** Strictly separate build and run stages.
6. **Processes:** Execute the app as one or more stateless processes.
7. **Port Binding:** Export services via port binding (e.g., FastAPI on port 8000).
8. **Concurrency:** Scale out via the process model.
9. **Disposability:** Maximize robustness with fast startup and graceful shutdown.
10. **Dev/Prod Parity:** Keep development, staging, and production as similar as possible.
11. **Logs:** Treat logs as event streams. Do not manage log files directly (output to stdout/stderr), except for designated observability files like `data/error_logs.json`.
12. **Admin Processes:** Run admin/management tasks as one-off processes.
