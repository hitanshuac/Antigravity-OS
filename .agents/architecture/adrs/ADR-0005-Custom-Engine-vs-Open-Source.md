# ADR 0005: Custom Agentic Engine vs. Monolithic Open-Source Alternatives

**Date:** 2026-06-23
**Status:** Accepted

## Context
During the agentic bootstrapping phase, the system triggered `.agents/workflows/git-discovery-preflight.md`, which mandates investigating existing open-source solutions before writing custom code. 

The AI agent execution landscape is heavily saturated with highly capable open-source tools:
- **Aider:** Excellent atomic Git rollbacks and AST parsing, but designed as a CLI tool requiring human interaction.
- **OpenHands / OpenDevin:** Excellent sandboxed execution, but requires heavy Docker dependencies.
- **Microsoft AutoGen / LangChain:** Powerful multi-agent routing, but suffers from massive abstraction bloat and unpredictable state management.

The architectural question was raised: Why are we building `Antigravity-OS` (a custom Python sandbox engine in `src/`) instead of leveraging these proven tools?

## Decision
We will reject the use of monolithic open-source agent frameworks in favor of building a custom, lightweight, pure-Python execution engine (`src/sandbox`, `src/capabilities`, `src/orchestrator`).

## Rationale
The primary goal of `Antigravity-OS` is **Zero-Dependency Submodule Integration**. 

This repository is not designed to be a standalone chat application for humans. It is designed to be an "Operating System" that can be injected into *any* existing repository via a simple `git submodule add` command. 
1. If we adopt OpenHands, we force every consuming repository to orchestrate Docker containers just to run an agent.
2. If we adopt Aider, we cannot easily run autonomous, silent, machine-to-machine workflows in the background (like auto-fixing CI/CD errors at 3 AM).
3. If we adopt LangChain, we introduce brittle dependency hell.

By building a hyper-specialized engine that only relies on the standard Python library (e.g., `subprocess`, `ast`), we achieve the determinism and safety of Aider/OpenHands without the bloat. The engine can be deployed anywhere Python runs.

## Consequences
- **Positive:** Maximum portability. Any repository can inherit "Senior Engineer AI capabilities" just by cloning this folder. Zero heavy dependencies.
- **Negative:** We must maintain our own `git_manager.py` and AST parsing logic. This introduces short-term friction (e.g., missing dependency bugs during Day 1 setup), but guarantees long-term deterministic execution.
- **Mitigation:** To combat the risk of "Execution Hallucinations" (where an AI assumes a custom script succeeded without checking), we must enforce rigid exit-code verification in our governance rules.
