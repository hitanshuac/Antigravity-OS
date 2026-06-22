---
description: Verify showcase assets, synthesize documentation, and prepare the README for publishing.
---

# Publish Showcase Workflow

**Trigger:** Invoked by `master-sync.md` Phase 5, or manually via `/ask run @[.agents/workflows/publish-showcase.md]`

## Objective
Verify that all recruiter-facing and technical documentation assets are present, correctly referenced, and up to date. This workflow does **NOT** handle git operations — those are delegated to `secure-checkpoint.md`.

## Execution Steps

### Step 1: Synthesize Documentation
1. Read the current project documentation (`README.md`, `HANDOVER.md`, and any existing `retrospective.md` or `walkthrough.md` if present).
2. Synthesize these files to update the `README.md` with the newest version baseline, SRE guardrails, and metrics.

### Step 2: Verify Documentation Assets (Dual-Presentation Mandate)
1. **Recruiter-Facing PNG:** Confirm that `docs/assets/architecture_diagram_showcase.png` exists and is referenced at the top of `README.md` via `![Architecture Diagram](docs/assets/architecture_diagram_showcase.png)`.
   - If the PNG is **missing or stale**, execute `.agents/workflows/generate-diagrams.md` to regenerate all diagrams programmatically. Do NOT use an AI image generator directly outside of the strict rules.
2. **Technical Mermaid Diagram:** Confirm that an inline Mermaid diagram is present in the Visual Reference Appendix section of `README.md`.
   - If it is missing, generate one from the current `src/` architecture.

### Step 3: User Approval
1. Show the proposed changes to the user for approval.
2. Once approved, the changes are ready to be staged by the parent orchestrator (`master-sync.md`) or by a manual `secure-checkpoint.md` invocation.
