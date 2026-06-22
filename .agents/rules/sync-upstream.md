---
name: Sync Upstream (Backport)
description: Safely backports locally hardened rules and workflows to the upstream Antigravity template repository without raising conflicts.
---

# Sync Upstream Workflow

This workflow automates the backporting of newly hardened rules and workflows from the local project to the master `Antigravity_Environment_Max` template repository. It solves the issue of keeping the upstream template expanded without triggering painful Git merge conflicts.

## Strategy: Local as Source of Truth
When an agent hardens a rule locally (e.g., after a post-mortem), the local `.agents/` folder becomes the most advanced version of the framework. Therefore, the upstream repository should simply **adopt** the local changes entirely.

## Execution Steps

1. **Identify Hardened Rules via Git**
   - The agent MUST use Git to programmatically identify modified framework files. Run commands like `git diff --name-status origin/main...HEAD .agents/` or check `git log` to find all newly created or modified rules, workflows, and skills inside the `.agents/` directory.
   - Rely entirely on Git as the index. There is no need to maintain a manual tracking file.

2. **Generate the Handover Template**
   - DO NOT pollute the main repository `HANDOVER.md` (which is reserved for LLM context switching).
   - Create or overwrite `docs/handover-template.md`.
   - Document the exact file paths of the modified `.agents/` files that need to be upstreamed, alongside a brief summary of the diff/changes (e.g., "Added Pydantic validation to prevent data loss").

3. **Human-in-the-Loop Sync**
   - DO NOT attempt to run automated `git clone` or aggressive `rm -rf` operations to force-copy the files. This strictly adheres to `.agents/rules/00-no-unauthorized-deletions.md`.
   - Inform the user that `docs/handover-template.md` has been generated. The developer will use this isolated checklist to manually copy-paste the modified files into the `Antigravity_Environment_Max` template repository.
