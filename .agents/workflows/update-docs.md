---
description: Update all markdown documentation (README, Handover, etc.) to strictly match the current state of the codebase.
---

# Update Docs Workflow

**Trigger:** Invoked by `master-sync.md` Phase 3, or manually via `/ask run @[.agents/workflows/update-docs.md]`

## Objective
Ensure that all project documentation accurately reflects the current state of the codebase. This is the **single source of truth** for documentation generation — it replaces the legacy `generate-readme.md` workflow.

## Execution Steps

### Phase 1: Environment Scan
Scan the following directories to build a complete inventory of the environment's capabilities:
1. `.agents/rules/` — Identify all active governance constraints.
2. `.agents/skills/` — Catalog all loaded skills.
3. `.agents/workflows/` — List all automated workflows.
4. `.agents/product/templates/` — Verify product design templates exist.
5. `.agents/architecture/adrs/` — Check for Architecture Decision Records.

### Phase 2: Source Code Analysis
1. Read the current contents of `src/capabilities/` and any active application source files.
2. Identify all public functions, classes, and API endpoints.
3. Note any new dependencies added to `requirements.txt`.

### Phase 3: README Synthesis
Update `README.md` to reflect the latest state. The README must contain:
- **Header & Badges**: Title and relevant tech badges.
- **Architecture Diagram**: Reference to `docs/assets/architecture_diagram.png`.
- **Overview**: Split-Plane Architecture summary.
- **Dynamic Skill Integration**: Statement about composable skill imports.
- **Installation & Setup**: Clone, venv, pip install instructions.
- **Current Capabilities**: Dynamic lists of Rules, Python APIs, Product Templates, Skills, and Workflows discovered in Phases 1-2.
- **Directory Structure**: Overview of `src/`, `data/`, `.agents/`, `.antigravity/`.
- **Adoption Method**: Instructions for injecting the Agentic Brain into other projects.
- **Visual Reference Appendix**: Architecture PNG and Mermaid diagrams.
- **Acknowledgments**: Credit to the study antigravity repository.

### Phase 4: Supporting Documentation
1. Update `HANDOVER.md` if new sections, workflows, or rules have been added.
2. Update `BOOTSTRAP.MD` if new phases or verification steps are needed.
3. Do NOT update `HANDOVER.md` or `BOOTSTRAP.MD` if no structural changes have occurred.

### Phase 5: Review
1. Create a `walkthrough.md` artifact summarizing the documentation changes.
2. Present the proposed changes to the user for approval before committing.
