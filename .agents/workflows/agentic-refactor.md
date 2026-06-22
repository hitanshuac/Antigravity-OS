---
name: Agentic Refactor (Architecture Decomposition)
description: A rigid, 5-phase chain-of-thought workflow for decomposing monolithic anti-patterns ("God Objects") into cleanly separated, layered architectures.
---

# Agentic Refactor Workflow

**Trigger:** Mandatory when refactoring legacy code, breaking down files exceeding 500 lines, or resolving complex data flow entanglement.
**Trigger Phrases:** "refactor this", "fix the data flow", "break down this monolith", "apply the agentic refactor workflow".

This workflow enforces the exact chain of thought used by Senior Principal Engineers (and high-functioning LLMs) to safely untangle monolithic architectures without breaking downstream dependencies.

## Phase 1: Current Architecture Analysis (As-Is)
Before writing any code, the agent MUST read the target files and map the current state. The agent must actively hunt for the following anti-patterns:
1. **God Objects**: Files acting as monolithic controllers that handle UI, business logic, and data persistence simultaneously.
2. **Implicit Data Busses**: Untyped global state, flat dictionaries, or session states used to pass data between detached functions.
3. **Side Effects**: Database writes, file I/O, or external API calls happening inside rendering loops or pure logic functions.
4. **Resource Churn**: Redundant network/database connections created and destroyed inside rapid execution loops.
5. **Phantom Architecture**: Dead code, unused modules, or decorative schemas that are defined but never enforced.

*Deliverable:* The agent MUST generate a clear representation (textual, bulleted, or diagrammatic) of the exact "As-Is" data flow to visualize the entanglement.

## Phase 2: Issue Identification & Severity Mapping (Rule Traceability)
The agent must list the identified architectural flaws explicitly and assign them severities based on Rule Traceability. Every identified flaw MUST cite the specific `.agents/rules/` file and Tier level it violates:
- 🔴 **High (Tier 0-1)**: Data integrity and security risks (e.g., `defensive-programming.md` Rule 1 violations, side-effects in render loops, CWE-74).
- 🟡 **Medium (Tier 2)**: Correctness, performance bottlenecks, missing test coverage, or validation bypasses.
- 🟢 **Low (Tier 3-4)**: Compliance, pure maintainability, styling, or documentation issues.

## Phase 3: Layered Decomposition (To-Be)
The agent must formulate a new architecture adhering strictly to the **Separation of Concerns (SoC)**. The proposed architecture MUST explicitly define these layers (if applicable to the stack):
1. **State Management**: Typed, validated models (e.g., Pydantic) acting as the single source of truth.
2. **Domain/Business Logic**: Pure, deterministic functions that take inputs and return outputs with zero side effects.
3. **External Services**: API boundaries, LLM prompt logic, and external integrations isolated from core math.
4. **Presentation/UI**: Thin orchestrators, views, or chart factories containing zero business logic.
5. **Persistence**: Consolidated database or file I/O operations behind connection pools.

*Deliverable:* The agent MUST generate a clear representation (textual, bulleted, or diagrammatic) of the cleanly separated "To-Be" architecture.

> **Automatic Escalation (LLM Council):** If the architectural decomposition is highly ambiguous, involves major framework tradeoffs, or you are unsure how to separate two entangled domains, the agent MUST automatically trigger `.agents/skills/llm-council/SKILL.md` to gain multiple perspectives and resolve the ambiguity before proceeding.

## Phase 4: File-by-File Execution Plan
The agent must draft a precise, actionable execution plan marking specific file changes using the following tags:
- `[NEW] <filename>`: For new, extracted service modules.
- `[MODIFY] <filename>`: For files being stripped down to thin orchestrators.
- `[DELETE] <filename>`: For dead code or phantom architecture.

## Phase 5: Verification & Safety Gates
Before executing the plan, the agent MUST:
1. **Deterministic Decoupling Check**: Before proposing any `[DELETE]` action for phantom architecture or unused modules, the agent MUST execute programmatic `grep_search` operations to mathematically prove zero downstream dependencies exist in the codebase.
2. Generate an `implementation_plan.md` artifact incorporating Phases 1-5.
3. Explicitly ask for human approval before proceeding.
4. Ensure the test suite is mapped to be updated alongside the refactor.

**Post-Execution Import Gate**: After refactoring, the agent MUST run programmatic import assertions via terminal (e.g., `python -c "from src.module import function; print('OK')"`) to prove the application graph and dependencies are not broken.

**Execution begins ONLY after user approval.**
