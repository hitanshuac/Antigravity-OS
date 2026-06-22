# Agent Terminal Execution Constraint (Anti-Hallucination Protocol)

This rule defines the strict operational boundaries for the AI Agent when executing terminal commands, specifically targeting the prevention of synthetic data hallucination caused by asynchronous race conditions or failed executions.

## 1. Zero-Tolerance for Hallucinated Output
- **Rule**: If an exploratory or ad-hoc terminal command (e.g., `run_command`) fails with a non-zero exit code or encounters a missing dependency, the agent **MUST NEVER** attempt to answer the user's prompt based on anticipated success or pre-training priors.
- **Why**: Providing synthetic snippets when actual data is unavailable corrupts the user's trust and violates the core principles of data engineering.

## 2. Explicit Failure Reporting
- **Rule**: Upon a failed command execution, the agent MUST explicitly state to the user: "The command failed with [Error Message]."
- **Action**: Do not hide Python tracebacks, module not found errors, or syntax errors behind conversational apologies. Surface the exact exception.

## 3. Mandatory Re-Execution Loop
- **Rule**: If the agent attempts to autonomously fix the error (e.g., by running `pip install` or fixing a syntax error), it MUST explicitly re-run the original extraction/analysis command and successfully read the output BEFORE formulating a response about the data.
- **Action**: You must verify the exit code of the final command is `0` and wait for the `command_status` to return the real textual output before parsing it for the user.

## 4. Interaction with Other Rules
- This rule is considered Tier 0 (Safety & Truthfulness) under `rule-conflict-resolution.md`. It overrides any conversational bias to "be helpful" or "keep the chat moving." The truthfulness of the terminal output is absolute.

## 5. Meta-Agent SOP: Building New Rules
Because the Antigravity repository relies heavily on autonomous execution, any future AI Agent tasked with creating or modifying a rule in `.agents/rules/` MUST adhere strictly to the **Rule Entry Template** defined in `meta-agent-templates.md`.

If an agent builds a rule without following the exact `Scope`, `Stability`, `Directive`, `Rationale`, and `Conflict handling` structure, it is considered invalid.

### Checkpoints and Deliverables
When generating proposals, orchestrating council peer-reviews, or pausing for human intervention, the agent MUST use the precise formatting templates defined in `meta-agent-templates.md`.

### Hierarchy Checks
Before saving a new rule, the agent MUST run `grep_search` across `.agents/rules/` or view `rule-conflict-resolution.md` to ensure the new rule does not conflict with existing Tier 0 or Tier 1 safety constraints.
