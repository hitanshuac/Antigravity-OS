---
description: Unified standard operating procedure defining the "Inner Loop" and "Outer Loop" rhythm that all AI agents must follow.
trigger: always_on
priority: tier_2_correctness
---

# SRE Standard Operating Procedure (SOP)

This rule defines the strict rhythmic loops that all AI agents must follow during the Software Development Life Cycle (SDLC) to ensure continuous quality, observability, and synchronized documentation.

## 1. The "Inner Loop" (Continuous Iteration)
The Inner Loop runs continuously during active development, ensuring that no code is shipped broken.

- **Trigger:** After EVERY code modification (even a single line change).
- **Action:** The agent MUST autonomously execute the `.agents/workflows/test-automation.md` workflow.
- **Enforcement:**
  1. The agent MUST execute `pytest`.
  2. **Failure Condition (Non-Zero Exit Code):** If tests fail, the agent MUST execute `.agents/workflows/error-observability.md` to log the failure, then fix the code, and retry.
  3. **Halt Condition:** If the agent fails to fix the test after three (3) consecutive attempts, it MUST halt execution immediately and ask the user for manual intervention.
  4. **Success Condition (Exit Code 0):** The Inner Loop is only considered successful when `pytest` returns exit code `0` AND the test output explicitly shows that at least 1 test was collected and passed (preventing false positives from empty test suites).
  5. Upon meeting the Success Condition, the agent MUST provide the user with explicit UI/CLI commands to test the feature manually (Anti-Solipsism Protocol per `testing-standards.md` Rule 7) and wait for the human user to reply "approved" or "works" before moving to the next task.

## 2. The "Outer Loop" (Ticket Conclusion)
The Outer Loop runs when a logical chunk of work is finished, preparing the codebase for production release.

- **Trigger:** When all Acceptance Criteria for the current ticket in `docs/05_TICKETS.md` are marked complete `[x]`, and the Inner Loop Success Condition is met.
- **Action:** The agent MUST autonomously execute the `.agents/workflows/master-sync.md` workflow.
- **Enforcement:** The `master-sync.md` workflow will automatically handle the sequential orchestration of documentation updates, diagram generation, and secure Git checkpoints. The agent MUST NOT begin work on the next ticket until the Outer Loop has successfully completed.

## 3. Workflow Integration
This SOP binds the bifurcated workflows into a unified strategy. Do not ask the user for permission to run the Inner Loop; testing is mandatory. You must ask for permission before executing the Outer Loop (the `master-sync.md` commit).
