# Rule: Linting & Formatting Standards

**Trigger:** Pre-commit and CI/CD pipelines.

## Objective
Enforce exponential-speed static analysis and formatting using **Ruff**. This replaces legacy tooling (`flake8`, `black`, `isort`, `bandit` syntax checks).

## Configuration
- Target Python Version: 3.11+
- Line Length: 120 (to accommodate Agentic payload signatures)
- Rules Enforced:
  - `E`, `F` (Pyflakes, pycodestyle)
  - `I` (isort)
  - `UP` (pyupgrade)
  - `RUF` (Ruff-specific rules)

## Agent Guidelines
1. **Never Bypass:** Do not use `# noqa` unless absolutely necessary (e.g., complex DuckDB macro imports). If used, you must document the reason.
2. **Auto-fixing:** The CI/CD pipeline does not auto-fix. All code must pass `ruff check .` and `ruff format --check .` locally before pushing.
