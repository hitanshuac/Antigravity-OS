# Workflow: Static Application Security Testing (SAST)

**Trigger:** Automatically on Push to `main` and Pull Requests.

## Objective
Enforce deep semantic dataflow analysis across all codebase additions using **Semgrep**, ensuring no hardcoded secrets, insecure API patterns, or 12-factor violations are introduced.

## Execution Rules
1. **Pipeline Integration:** Semgrep is configured in `.github/workflows/semgrep.yml`. It runs asynchronously on every PR.
2. **Rule Selection:** We utilize `p/default` (community standard), `p/owasp-top-ten`, and `p/secrets`.
3. **Blocking Policy:** Any `ERROR` severity finding will strictly block the merge. `WARNING` findings are logged as annotations but do not block the pipeline.
4. **Agent Guidelines:** Agents generating code must ensure no secrets are hardcoded. Use `os.getenv()` or `pydantic-settings` exclusively.
