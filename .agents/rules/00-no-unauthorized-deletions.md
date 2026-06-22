# Rule 00: The No-Deletion Mandate

**Strict Enforcement:** This rule overrides all other workflows, scripts, and instructions.

1. **Never Delete Without Explicit Approval:** Under no circumstances is the AI agent allowed to automatically execute deletion commands (e.g., `Remove-Item`, `rm -rf`) against an existing project directory or file.
2. **Conflict Resolution:** If a file from this Base Environment collides with an existing file in the target project, the incoming file supersedes the existing one *only after* the conflict has been presented to the user and manually approved.
3. **Non-Destructive Enhancer:** This repository acts strictly as a booster/enhancer to existing projects. It must never act destructively.
4. **Semantic Merge Exemption:** The Autonomous Semantic Merge Protocol defined in `.agents/workflows/merge-conflict-resolution.md` (union merges for `.gitignore`, dependency appends for `requirements.txt`, and isolated `AGENT_DOCS.md` linking for `README.md`) does **NOT** constitute deletion or overwriting. These non-destructive, additive operations are explicitly exempt from the manual approval requirement above.
