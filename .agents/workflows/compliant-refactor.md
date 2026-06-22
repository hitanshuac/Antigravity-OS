---
name: SRE-Compliant Agentic Refactor
description: Orchestrates agentic-refactor and test-automation while strictly enforcing SRE SOPs, defensive programming, and Hack2Skill competition rules.
---

# SRE-Compliant Agentic Refactor

This master orchestration workflow chains architectural decomposition (`agentic-refactor.md`) with continuous testing (`test-automation.md`) to execute large-scale codebase changes while ensuring zero violations of the project's core rule constraints.

## 🚨 Phase 1: Rule Verification & Constraints Loading

Before writing or modifying any code, the agent MUST read and internalize the following core mandates:

1. **Competition Rules**: `.agents/rules/02-hack2skill-rules.md` (Max 3 attempts, <10MB repo, clean code).
2. **SRE SOP**: `.agents/rules/sre-sop.md` (Strict Inner/Outer Loop execution, no silent failures).
3. **Defensive Programming**: `.agents/rules/defensive-programming.md` (Schema-first I/O, idempotent writes, zero silent data loss).
4. **Code Quality**: `.agents/rules/code-quality-standards.md` (Clean, maintainable, PEP-8 compliant).
5. **Security / SAST**: `.agents/rules/sast-evaluator-standards.md` (CWE prevention, safe inputs).
6. **Data Validation**: `.agents/rules/data-validation.md` (Strict boundaries, Pydantic type enforcement).

*Failure to adhere to these rules during the refactor will result in pipeline failure.*

---

## 🛠️ Phase 2: Agentic Decomposition & Refactor

Invoke the **`.agents/workflows/agentic-refactor.md`** workflow to begin structural changes.

**During execution, the agent MUST ensure:**
- No component is modified without a clear separation of concerns.
- Pydantic models (or strict `TypedDict`s) are used as contracts for all I/O boundary layers.
- Exception handling logs full context (Fail Fast, Never Fail Silent) rather than swallowing errors.
- External API calls are strictly encapsulated and decoupled from raw UI events.

---

## 🧪 Phase 3: SRE Inner Loop Testing

Immediately upon completing code modifications, the agent MUST invoke the **`.agents/workflows/test-automation.md`** workflow.

1. **Execute Tests**: Run the full `pytest` suite autonomously.
2. **Handle Failures**: If any tests fail (Non-Zero Exit Code), the agent MUST halt, diagnose the failure, fix the code according to defensive standards, and retry.
3. **Success Condition**: The refactor is NOT complete until all tests pass (`Exit Code 0`) and the test output explicitly confirms collection/execution.

---

## ✅ Phase 4: Final Compliance Sign-off

Once the Inner Loop succeeds, the agent must verify:
1. No unauthorized secrets or API keys have been hardcoded (SAST compliance).
2. The UI gracefully degrades under load (Defensive compliance).
3. The codebase remains clean, well-commented, and ready for Hack2Skill evaluation.

*The agent will then notify the user of the successful refactor and await approval for the Outer Loop master sync.*
