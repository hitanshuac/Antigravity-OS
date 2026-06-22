# Meta-Agent Formats and Templates

This file acts as the ultimate structural template repository for all AI Agents operating within this workspace. When instructed to produce rules, proposals, reviews, or summaries, agents MUST strictly adhere to the formats defined below.

## 1. Rule Entry Template
Use this template when adding or refactoring reusable rules in the `.agents/rules/` directory.

```markdown
### Rule: <RULE_ID>
- Owner layer: Global | Domain | Project
- Scope: [where this rule applies]
- Stability: core | behavior | experimental
- Status: active | superseded | draft
- Directive: [clear imperative rule]
- Rationale: [why this rule exists]
- Conflict handling: [what overrides this rule or when to escalate]
- Example: [positive example]
- Non-example: [what this rule forbids or does not cover]
```
*Requirement: `Directive`, `Rationale`, and `Conflict handling` must never be omitted.*

## 2. Deliverable / Proposal Template
Use this template when an agent acts as a planner, architect, or the "Generator" phase of an LLM Council.

```markdown
## Deliverable: [title]

### Proposal
[What is being proposed — the solution, plan, or finding]

### Alternatives considered
[At least one alternative approach and why it was not chosen]

### Pros / Cons
| Pros | Cons |
|------|------|
| ...  | ...  |

### Risks
[Each risk with likelihood, impact, and mitigation — or "None identified"]

### Recommendation
[Clear, actionable recommendation for the user or the next agent]
```

## 3. Review / Audit Output Template
Use this template for review-first roles (like `risk-reviewer` or the "Peer Review" phase of the LLM Council).

```markdown
## Review: [title]

### Findings
- [severity] [file:line] [issue]

### Open questions / assumptions
- [question or assumption]

### Residual risks
- [remaining risk after review, or "None"]

### Summary
[Short conclusion: Accept / Accept with changes / Reject with reason.]
```

## 4. Execution Checkpoint Template
Use this template when an agent encounters ambiguity, high-risk operations, or requires human approval before proceeding.

```markdown
## Checkpoint: [gate name]

**Current state**: [what has been done so far]
**Proposal**: [what will happen next]
**Risks**: [what could go wrong]
**Decision needed**: [specific yes/no or choice the user must make]

Waiting for approval before proceeding.
```
