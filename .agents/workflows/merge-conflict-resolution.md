# Workflow: Safe Merge & Conflict Resolution

**Trigger:** MANDATORY Pre-flight check. Must be executed *before* scaffolding or merging this Base Agentic Environment into any existing project.

## Objective
This repository must act purely as an addon, booster, or enhancer. It must **NEVER** instruct the deletion of any existing project files without explicit manual approval from the user. This is a strict mandate rule.

## Execution Steps

### 1. Identify File Collisions
- Scan the target repository and compare it against the incoming Base Environment files.
- Identify all file collisions (e.g., if the target project already has a `README.md`, `data/error_logs.json`, or `HANDOVER.md`).

### 2. Autonomous Semantic Merge Protocol (Zero-Conflict)
Do NOT pause for manual approval on predictable boilerplate collisions. Instead, execute the following semantic merges automatically:

- **`.gitignore` (Union Merge):** Read the target project's `.gitignore` and the Base Environment's `.gitignore`. Compute the mathematical union (combine both lists), remove duplicates, sort them, and write the combined list back to the target project.
- **`requirements.txt` (Dependency Append):** Parse both dependency lists. Identify any packages required by the Base Environment that are missing from the target project. Append *only* the missing packages. If there is a version conflict on a shared package, you MUST **FLAG IT FOR REVIEW** and pause execution for manual user resolution.
- **`README.md` (Isolation Strategy):** DO NOT overwrite the target project's `README.md`. Keep the Base Environment documentation isolated in a separate file named `AGENT_DOCS.md`. Read the target project's `README.md` and append a single link to it (e.g., `[View Agentic Environment Documentation](AGENT_DOCS.md)`) at the bottom of the file. Ensure that credits to the original "study antigravity repo" are included in `AGENT_DOCS.md`.

### 3. Absolute No-Deletion Mandate
- If you encounter obsolete folders (like a stale `.antigravity/` cache) or files that you believe MUST be deleted to prevent conflicts, **DO NOT DELETE THEM AUTOMATICALLY.**
- Any deletion must be proposed to the user and requires explicit authorization to proceed.

### 4. Proceed to Scaffolding
- After successfully resolving boilerplate collisions using the Semantic Merge Protocol, automatically proceed with the actual merge and bootstrapping phases without waiting for user intervention.
