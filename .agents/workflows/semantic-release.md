# Workflow: Python Semantic Release

**Trigger:** Automatically on merge to `main`.

## Objective
Enforce mathematically sound, commit-driven versioning and changelog generation using **Python Semantic Release**. This eliminates human error in release management.

## Execution Rules
1. **Pipeline Integration:** Configured in `.github/workflows/release.yml`. It runs automatically after CI checks pass on the `main` branch.
2. **Commit Standard:** All commits MUST follow the Conventional Commits specification (e.g., `feat:`, `fix:`, `chore:`).
3. **Behavior:**
   - `fix:` triggers a Patch release (e.g., 1.0.0 -> 1.0.1)
   - `feat:` triggers a Minor release (e.g., 1.0.0 -> 1.1.0)
   - `BREAKING CHANGE:` inside the commit body triggers a Major release (e.g., 1.0.0 -> 2.0.0)
4. **Agent Guidelines:** Agents generating commit messages during automated workflows MUST strictly adhere to Conventional Commits.
