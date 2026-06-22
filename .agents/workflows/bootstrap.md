---
name: Local Bootstrapper
description: Workflow to scaffold and verify the local environment before execution.
---

# Bootstrap Workflow

This workflow has two modes of operation:
- **First Run:** Scaffolds the Antigravity Environment from scratch in a new or existing repository.
- **Upgrade Run:** Detects an older installed version and safely merges the latest Antigravity assets without destroying host project code.

Execute the phases sequentially. Phase 0 is only relevant for repositories that have already been bootstrapped once.

---

## Phase 0: Environment Upgrade Protocol (Existing Repositories Only)

**Skip this phase if this is the first time running bootstrap in this repository.**

1. **Detect Existing Installation:** Check if `.agents/workflows/` already exists. If it does, this is an upgrade run.
2. **Clone Latest Upstream:** // turbo
   - Run `git clone https://github.com/hitanshuac/Antigravity_Environment_Max.git .agents/tmp/antigravity_latest`
3. **Verify Semantic Release Context:** Confirm that `.agents/tmp/antigravity_latest/.agents/workflows/semantic-release.md` exists. This anchors the version context for the upgrade.
4. **Additive Document Merge:**
   - Compare `.agents/tmp/antigravity_latest/.agents/` against the local `.agents/` directory.
   - Copy all entirely *new* `.md` files (workflows, rules, product templates) into the local `.agents/` folder.
   - Copy all entirely *new* root-level files (e.g., `ruff.toml`, `.pre-commit-config.yaml`) into the project root.
   - **Do NOT overwrite** any existing files that the host project has already modified.
5. **Union Merge Boilerplate:** Execute `.agents/workflows/merge-conflict-resolution.md` to safely union-merge `.gitignore` and `requirements.txt`.
6. **Cleanup:** Delete `.agents/tmp/` entirely, then proceed to Phase 1.

---

## Phase 1: Verify Codebase Integrity

1. Confirm the `.agents/` folder is intact and contains `workflows/`, `rules/`, and `product/templates/`.
2. Confirm the `src/` directory exists with at least one module.

## Phase 2: Verify Dependencies

1. Confirm `requirements.txt` exists and all dependencies are pinned.
2. Run `pip install -r requirements.txt` inside the virtual environment. // turbo
3. Confirm `.venv/` is excluded by `.gitignore`.

## Phase 3: Verify Config & Secrets

1. Check if `.secrets` or `.env` exists. If not, generate a placeholder.
2. Run a search for leaked API keys inside `src/`. If any are found, immediately purge them and move them to `.secrets`.
3. Ensure `.gitignore` is active and blocking `.secrets/`, `.env`, and `data/`.
4. **Remote CI/CD Alignment:** Execute `.agents/workflows/setup-secrets.md` to ensure the upstream GitHub repository is provisioned with any required Action secrets.

## Phase 4: Verify Product Design Gate

1. Confirm that `.agents/product/templates/` exists and contains all 5 templates (`01_PRD.md`, `02_TAD.md`, `03_SECURITY.md`, `04_FRONTEND.md`, `05_TICKETS.md`).
2. If the user is building a new project, execute `.agents/workflows/generate-product-docs.md` to populate them before allowing any code generation.

## Phase 5: Verify Observability

1. Ensure the `data/` directory exists (with `.gitkeep`).
2. Confirm `data/error_logs.json` exists or can be initialized by the `error-observability.md` workflow.

## Phase 6: Verify Local Enforcement (Pre-commit & Linting)

1. Confirm `.pre-commit-config.yaml` exists at the repo root.
2. Run `pre-commit install` to ensure hooks are active. // turbo
3. Run `ruff check .` and `ruff format --check .` to validate the codebase passes linting. // turbo

## Phase 7: Verify Testing Infrastructure

1. Confirm `src/tests/` exists with at least one test file.
2. Run `python -m pytest src/tests/ -v` to ensure all existing tests pass. // turbo
3. If tests fail, execute `.agents/workflows/error-observability.md` to log and diagnose the failures.

## Phase 8: Verify Zero-Touch Automation

1. Confirm `src/capabilities/git_manager.py` exists for safe Git operations.
2. Confirm `src/capabilities/ci_log_fetcher.py` exists for remote CI/CD log syncing.
3. Confirm `src/capabilities/watch_ci.ps1` exists for autonomous background monitoring.
