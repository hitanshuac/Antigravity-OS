# Global Git Command Ban (Anti-Hallucination Protocol)

This rule was implemented to prevent Semantic Override failures where the agent hallucinates a local git command instead of executing upstream synchronization protocols.

## 1. Strict Prohibition of Raw Git Commands
- **Rule**: You MUST NEVER execute raw `git` commands in the terminal (e.g., `git add`, `git commit`, `git push`, `git pull`).
- **Why**: Bypassing the Python Git Manager (`git_manager.py`) disables the error observability layer, breaks pre-commit hooks, and can result in local checkpoints that fail to synchronize with remote state.

## 2. Mandatory Method for Version Control
- All source control and versioning operations MUST be routed exclusively through the Python Git Manager.
- **Command**: `python src/capabilities/git_manager.py checkpoint "[Your descriptive commit message]"`
- This Python script safely wraps the staging, committing, and pushing processes.

## 3. Workflow Annotations
- If a workflow file (like `secure-checkpoint.md`) contains a `// turbo` flag next to an instruction to checkpoint the codebase, do NOT interpret this as authorization to use raw `git` commands. It strictly authorizes auto-running the `git_manager.py` tool.

> **Post-Mortem Origin:** This rule was enacted after an LLM Council analysis identified that agents were overriding workflow scripts due to pre-training bias when encountering generic terms like "stage, commit, and push". This rule serves as a Tier 1 structural constraint to block the behavior entirely.
