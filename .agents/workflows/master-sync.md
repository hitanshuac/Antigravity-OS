---
description: A master orchestration workflow that sequentially validates, documents, generates assets, versions, and checkpoints the codebase.
---

# Master Sync Workflow

**Trigger:** Explicit invocation via `/ask run @[.agents/workflows/master-sync.md]`

This is the **top-level orchestrator** for synchronizing the entire codebase. It calls sub-workflows in strict sequential order. Do NOT skip phases.

## Phase 1: Pre-flight Checks
1. **Repository Sanitation**: Scan the project root directory for rogue scratchpad scripts or temporary files (e.g., orphaned `*.py` or `*.txt` files used for testing logic). Delete any files that do not belong in the core production bundle to strictly enforce Code Quality and SRE hygiene rules.
2. Verify that `.agents/product/templates/` contains all 5 product templates (`01_PRD.md` through `05_TICKETS.md`).
3. If any template is missing, halt and execute `.agents/workflows/generate-product-docs.md` to populate them.
4. Run `ruff check .` to verify the codebase passes linting.

## Phase 2: Test Automation Gate
1. Execute `.agents/workflows/test-automation.md`.
2. If any tests fail, execute `.agents/workflows/error-observability.md` to log the failure.
3. Fix the failing code and re-run tests. Do NOT proceed until all tests pass.

## Phase 3: Update Documentation
1. Execute `.agents/workflows/update-docs.md`.
2. This will scan `.agents/` and `src/` to synchronize `README.md`, `HANDOVER.md`, and `BOOTSTRAP.MD` with the current codebase state.

## Phase 4: Regenerate Architecture Diagrams
1. Execute `.agents/workflows/generate-diagrams.md`.
2. This will scan all `.d2` and `.py` diagrams, generate their technical base PNGs, and automatically run the AI styling pass to create the `_showcase` assets.
3. The outputs will be saved to `docs/assets/`.

## Phase 5: Publish Showcase
1. Execute `.agents/workflows/publish-showcase.md`.
2. This verifies the documentation assets (PNG + Mermaid) are present and correctly referenced in `README.md`.
3. Present all proposed changes to the user for final approval.

## Phase 6: Semantic Release
1. Execute `.agents/workflows/semantic-release.md`.
2. Ensure the commit message follows Conventional Commits (`feat:`, `fix:`, `docs:`, etc.).
3. The CI/CD pipeline in `.github/workflows/release.yml` will handle the version bump and changelog generation.

## Phase 7: Conversational Error Harvesting
1. The agent MUST review the conversation log (from the last stable checkpoint up to the present moment).
2. Extract any errors, failed implementation attempts, hallucinations, or dead-ends encountered during this session.
3. Execute `.agents/workflows/error-observability.md` to persist these lessons to the central observability suite so they are never repeated.

## Phase 8: Secure Checkpoint
1. Execute `.agents/workflows/secure-checkpoint.md`.
2. This invokes the Python Git Manager (`src/capabilities/git_manager.py`) to safely stage, commit, and push changes while enforcing error observability.
3. Confirm to the user that all changes are permanently secured on GitHub.
