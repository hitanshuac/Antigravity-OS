---
name: Delegate Execution (Bridge to Headless Engine)
description: A bridge workflow that allows the IDE AI to seamlessly trigger the Python Headless Execution Engine to perform coding loops without consuming IDE tokens.
---

# Delegation Workflow

**Trigger:** The user wants to execute a heavy coding loop, refactor, or generation task using the cheap/free API keys in the `.env` file rather than using the expensive IDE AI tokens.
**Trigger Phrases:** "delegate this", "run the python engine for this", "execute headless", "delegate execution".

## The Concept (The Bridge)
This repository operates in two modes:
1. **Interactive Mode (IDE Chat):** High-level architecture design and rule interpretation (Uses IDE tokens).
2. **Autonomous Mode (Headless Engine):** Heavy coding, testing, and Git rollbacks via `src/orchestrator/run.py` (Uses `.env` API keys).

As the IDE AI, you act as the *Manager*. When this workflow is triggered, you must format the user's task and pass it to the Python engine (the *Worker*), verify it ran successfully, and report back.

## Phase 1: Task Formatting
When the user asks you to "delegate this task", you must cleanly extract the exact requirements of the task. 
Do NOT write the code yourself. Your job is to construct the command string.

## Phase 2: Execution
You MUST use your terminal execution tool to run the following Python command. 

```bash
python src/orchestrator/run.py --task "YOUR SUMMARIZED TASK HERE"
```

*Note: If the task is long, write it to a temporary `data/task_payload.txt` file and run `python src/orchestrator/run.py --file data/task_payload.txt` (if supported by the entrypoint), or ensure the command line argument is properly escaped.*

## Phase 3: Monitoring & Exit Code Verification
You must wait for the terminal command to finish.
Per the `.agents/rules/01-agent-execution-standards.md` Anti-Hallucination rule:
1. You MUST verify the exit code of the Python process.
2. If it succeeds (Exit Code 0), read the final terminal output and summarize what the Headless Engine accomplished.
3. If it fails (Non-Zero Exit Code), explicitly report the failure and ask the user if you should adjust the task prompt and retry.

**DO NOT HALLUCINATE COMPLETION. VERIFY THE TERMINAL OUTPUT.**
