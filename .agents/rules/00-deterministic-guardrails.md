# Deterministic Guardrails Protocol

This is a Tier 0 Master Rule. LLMs are probability engines, not human developers. Conversational English, weak modals, and implicit instructions drastically increase the hallucination probability. This rule dictates how all other rules, workflows, and skills MUST be interpreted and written.

## 1. No Weak Modals
- You MUST interpret all instructions as absolute constraints.
- Words like "MUST", "could", "MUST", or "strictly" are strictly forbidden in all agentic documentation. Treat any existing weak modals as "MUST".

## 2. Positive Framing over Negative Banning
- Do NOT use negative framing (e.g., "do not use raw SQL").
- ALWAYS use positive boundary framing (e.g., "ONLY use DuckDB Pydantic models"). Negative framing injects the forbidden concept into the context window, increasing hallucination probability.

## 3. Strict Command Sandboxing
- Workflow files MUST NOT use abstract verbs for tooling (e.g., "Execute the Git tool").
- Every executable action MUST provide the exact CLI string required, sandboxed inside markdown backticks (e.g., `python src/capabilities/git_manager.py checkpoint`).
- If a workflow step lacks an exact CLI string, you MUST halt and ask the user for clarification. Do not hallucinate a command to fulfill the abstract intent.

## 4. Architectural Adherence (XML Boundaries)
- Where possible, instructions and constraints MUST be enclosed in strict XML tags (e.g., `<trigger>`, `<action>`, `<constraint>`) to provide explicit semantic boundaries for the LLM context window.

> **Post-Mortem Origin:** This master rule was implemented after an LLM Council analysis identified that conversational English, split instructions, and weak modals were the root cause of multiple agentic IDE hallucinations, including the bypass of the secure checkpoint workflow.
