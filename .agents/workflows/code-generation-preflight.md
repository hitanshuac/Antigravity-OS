---
name: Code Generation Pre-Flight
description: Mandatory pre-coding checklist enforcing industry-standard Design Review, constraints checking, and TDD alignment before writing code to disk.
---

# Code Generation Pre-Flight (Design Review)

**Trigger:** Mandatory BEFORE the AI agent writes, generates, or modifies any Python/source code for a new feature or ticket.

This workflow simulates the "Design Review" and "Technical Spec" phases of a high-performing product development team's SDLC. It forces the agent to cross-examine its intended implementation against the rigorous `.agents/rules/` constraints, preventing context fragmentation and architectural drift.

## Phase 1: Requirement & Ecosystem Validation
Before designing the code, the agent MUST:
1. **Ticket Alignment:** Verify the intended code perfectly satisfies the current Acceptance Criteria in `docs/05_TICKETS.md`.
2. **DRY (Don't Repeat Yourself) Check:** Search the existing `src/` directory. Is there an existing utility, Pydantic model, or helper function that can be reused instead of writing new code?
3. **Git Discovery:** If bringing in external patterns, execute `.agents/workflows/git-discovery-preflight.md` to check for open-source precedent.

## Phase 2: The Core Constraints Checklist
The agent MUST explicitly verify its proposed implementation against the following active rules. If the proposed code violates ANY of these, the agent MUST redesign the approach.

- [ ] **Tier 0 Safety (`defensive-programming.md`)**
  - Are we doing file I/O? If yes, is a Pydantic/TypedDict schema explicitly defined?
  - Are we using guard clauses at the top of the function?
  - Are we handling exceptions explicitly (no bare `except:`) and logging them before returning fallbacks?
- [ ] **Tier 1 Security (`sast-evaluator-standards.md`, `12-factor-rules.md`)**
  - Are all user inputs rigorously sanitized (CWE-74)?
  - Are we absolutely sure no API keys or secrets are hardcoded?
- [ ] **Tier 2 Correctness (`data-validation.md`, `testing-standards.md`)**
  - How will this code be tested? Have we identified the necessary mocked dependencies and fixtures?
- [ ] **Tier 3 Compliance (Platform & SRE Constraints)**
  - Does this architecture adhere strictly to deployment limits and platform constraints (e.g., repo size, database restrictions)?
  - Does the implementation plan align with the strict SRE Inner/Outer loop rhythms (`sre-sop.md`)?
  - Have all SAST compliance standards (`sast-evaluator-standards.md`) been accounted for?
- [ ] **Tier 4 Style (`code-quality-standards.md`)**
  - Will this function exceed Cyclomatic Complexity 5? If yes, break it into smaller helpers now.
  - Are exact type hints (`-> str`, `: int`) and Google-style docstrings included in the design?

## Phase 3: TDD Handoff
1. The agent MUST NOT write the implementation code directly to the `src/` files yet.
2. The agent MUST first initiate the **Red** phase of the Red-Green-Refactor loop by executing Phase 1 and 2 of `.agents/workflows/test-automation.md` to generate the failing test scaffolds.

## Phase 4: Peer Review (Human-in-the-Loop)
1. Before proceeding to write the actual implementation (the **Green** phase), the agent MUST present a brief summary of the intended architecture (Function signatures, data schemas, and the chosen constraint validations) to the user.
2. The agent MUST explicitly wait for the user to reply "approved" or "looks good" before committing the implementation code to disk.
