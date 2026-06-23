# Antigravity OS

Antigravity OS is the core Agentic Engine (Single Source of Truth) that provides the "hands" for an AI agent. It allows an LLM to reliably edit files, run terminal commands, and revert mistakes without human intervention.

## Core Features
- **Zero External Dependencies**: Pure Python implementation to avoid brittle dependencies.
- **Atomic File Swaps**: Ensures partial writes never corrupt the codebase.
- **Git State Management**: Autonomous checkpointing and rollbacks.
- **Process Group Isolation**: Prevents orphaned background processes during timeout failures.

## Architecture
The core engine primitives are located in `src/sandbox/`.
- `bash.py`: Bounded chunked stream reading, OOM protections, and cross-platform process isolation.
- `git.py`: Git-based state manager providing atomic checkpoints and absolute rollbacks.
- `editor.py`: Strict unified-diff parser with atomic edits and semantic fallback validation.
- `__init__.py`: Package interface exporting `BashExecutionTool`, `GitRollbackManager`, and `FileEditorTool`.

The context engine primitives are located in `src/context/`.
- `repomap.py`: Parses the repository AST structure, filters ignored paths, and builds a compressed map of classes, functions, and signatures.

The capabilities engine primitives are located in `src/capabilities/`.
- `git_manager.py`: Secure Python wrapper for Git state management, eliminating raw bash commands.

The brainstem and execution state machine are located in `src/orchestrator/`.
- `engine.py`: Contains the `ReActEngine`, a deterministic state machine orchestrating Reason + Act iterations with a 3-strike verification loop and Git rollback constraints.
- `llm.py`: Contains the `UniversalLLMClient` adapter, supporting OpenAI, Groq, OpenRouter, and NVIDIA NIM via a unified structured-tooling interface.

## Execution Modes
Antigravity OS supports a dual-mode architecture bridged by a delegation workflow:

1. **Interactive Mode (IDE Chat):** You chat with your IDE AI (burning IDE tokens) to design architecture. The IDE AI acts as the "Manager" by reading the `.agents/rules/`.
2. **Autonomous Mode (Headless Engine):** The pure Python engine operates without a chat window. It uses the API keys in `.env` to execute cheap, rapid coding loops (burning `.env` tokens).

**The Delegation Bridge:**
To seamlessly switch from Interactive to Autonomous mode without memorizing terminal commands, tell your IDE AI to **"Delegate this task."** 
This triggers `.agents/workflows/delegate-execution.md`, instructing the IDE AI to format your task and automatically execute `python src/orchestrator/run.py --task "..."` on your behalf.

## Governance
This repository contains the master `.agents/` folder (SRE SOPs, Defensive Programming rules, Workflows). 
For any new application you build, include this repository as a Git Submodule to inherit the engine and rules.
