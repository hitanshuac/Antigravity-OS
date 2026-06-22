---
name: Sync Upstream (Git SSOT)
description: Safely backports locally hardened rules and workflows to a remote Git repository acting as the Single Source of Truth.
---

# Sync Upstream Workflow (Git SSOT)

**Trigger:** Explicit invocation via `/ask run @[.agents/workflows/sync-upstream.md] <URL_OF_SSOT_REPO>`

This workflow automates the backporting of newly hardened rules and workflows from the local project to a central Git repository acting as the **Single Source of Truth (SSOT)**. This solves the issue of keeping the upstream template expanded without relying on manual copy-pasting or risking local hard drive paths.

## Execution Steps

### 1. Pre-Flight Check & Repo Validation
- The user MUST provide the remote Git URL of the upstream repository (e.g., `https://github.com/hitanshuac/Antigravity_Environment_Max`).
- The agent must verify it has access to the standard Git CLI tools.

### 2. Autonomous Cloning
- The agent MUST create a temporary directory inside the local workspace (e.g., `./tmp_ssot_sync`).
- Add `./tmp_ssot_sync/` to the `.gitignore` of the current project if not already present.
- Clone the remote upstream repository into `./tmp_ssot_sync/`.

### 3. File Delta Extraction & Patching
- The agent uses Git to programmatically identify modified framework files in the current repository:
  ```bash
  git log --name-status --oneline .agents/
  ```
- Identify all newly created or modified rules, workflows, and skills inside the local `.agents/` directory that represent "hardened" improvements.
- Copy the identified files from the local `.agents/` folder directly into the `./tmp_ssot_sync/.agents/` folder, overwriting existing files or creating new ones.

### 4. Commit and Push to SSOT
- Navigate the terminal into `./tmp_ssot_sync/`.
- Stage the newly copied files using `git add .agents/`.
- Commit the changes with a semantic message (e.g., `feat: backport hardened rules and workflows from project`).
- Push the changes to the upstream remote repository (`git push origin main`).

### 5. Cleanup
- Navigate back to the root of the local project.
- Safely delete the `./tmp_ssot_sync` directory using `rm -rf ./tmp_ssot_sync` (or PowerShell `Remove-Item` on Windows).
- Remove the `./tmp_ssot_sync` entry from `.gitignore` if it was added in Step 2.

### 6. Handover Documentation
- Inform the user that the sync is complete.
- Print out the list of rules/workflows that were successfully backported to the remote SSOT repository.
