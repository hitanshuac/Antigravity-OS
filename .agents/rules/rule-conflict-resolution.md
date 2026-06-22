---
description: Establishes a strict priority hierarchy for resolving conflicts between rules and workflows.
trigger: always_on
priority: tier_0_safety
---

# Rule Conflict Resolution Protocol

When two or more `.agents/rules/` files issue contradictory instructions, the agent MUST NOT silently pick one over the other. This rule establishes a deterministic resolution hierarchy.

> **Post-Mortem Origin:** This rule was created after a root-cause analysis where a "no databases" project constraint (Tier 3) silently overrode `sql-standards.md` (Tier 2), causing the agent to use raw `json.load()` without schema validation. The resulting code silently wiped the error log file. A priority hierarchy would have forced the agent to find a non-database implementation of schema validation (e.g., Pydantic) instead of skipping validation entirely.

## 1. Rule Priority Hierarchy

Rules are organized into 5 tiers. Higher tiers ALWAYS take precedence over lower tiers.

| Tier | Category | Rules | Rationale |
|---|---|---|---|
| **0** | **Safety (Data Integrity)** | `00-no-unauthorized-deletions.md`, `defensive-programming.md` | Preventing data loss is non-negotiable |
| **1** | **Security** | `sast-evaluator-standards.md` Rule 5 (CWE-74), `12-factor-rules.md` Factor III (secrets) | Security vulnerabilities are career-ending |
| **2** | **Correctness** | `testing-standards.md`, `data-validation.md`, `sql-standards.md`, `error-observability.md` | Correct behavior trumps style and compliance |
| **3** | **Compliance** | `project-specific-rules.md`, `compliance-standards.md`, `sast-evaluator-standards.md`, `hf-deployment-standards.md` | Platform rules are important but negotiable in implementation |
| **4** | **Style** | `code-quality-standards.md`, `linting-standards.md`, `context_compaction.md` | Code style is the least critical dimension |

## 2. Conflict Resolution Protocol

When the agent detects a conflict between two rules from different tiers:

1. **Identify the Conflict:** Explicitly state which two rules conflict and what the contradiction is.
2. **Apply the Higher Tier:** The higher-tier rule wins. The lower-tier rule's intent must be satisfied through an alternative implementation that does not violate the higher-tier rule.
3. **Document the Override:** Add a code comment at the point of conflict: `# RULE OVERRIDE: [higher rule] takes precedence over [lower rule]. See rule-conflict-resolution.md.`
4. **Log an ADR (if Architectural):** If the conflict resolution changes the system architecture (e.g., swapping DuckDB for Pydantic+JSON), record an ADR in `.agents/architecture/adrs/`.

### Example: "No Database" Constraint vs. Schema Validation

- **Conflict:** `project-specific-rules.md` (Tier 3) says "NEVER use heavy local databases." `defensive-programming.md` (Tier 0) says "ALL persistent data MUST be validated against a Pydantic schema."
- **Resolution:** Tier 0 wins. The agent MUST implement Pydantic schema validation. Since databases are forbidden, it uses Pydantic models to validate JSON files instead of DuckDB schemas. Both rules are satisfied.
- **Forbidden Resolution:** Skipping schema validation entirely because "we can't use a database."

## 3. Same-Tier Conflicts

When two rules from the SAME tier conflict:

1. The more specific rule takes precedence over the more general rule.
2. If specificity is equal, the agent MUST halt and ask the user for a decision.
3. The resolution must be documented as an ADR.

## 4. Workflow vs. Rule Conflicts

- **Rules** (`.agents/rules/`) define constraints that are ALWAYS active.
- **Workflows** (`.agents/workflows/`) define procedures that are invoked on demand.
- If a workflow step contradicts an always-on rule, the rule wins.
- The workflow step must be adapted to comply with the rule, not the other way around.
