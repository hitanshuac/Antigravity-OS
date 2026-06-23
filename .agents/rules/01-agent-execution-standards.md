# Agent Execution Standards

This rule governs the fundamental operational behaviors of any AI agent operating within or pulling from this environment.

## 1. Assert State Currency (Anti-Staleness Protocol)
AI agents have a tendency to hallucinate templates or operate blindly on stale local clones.
- **Rule:** You MUST always assert state currency by running `git pull origin main` immediately prior to executing read/scaffold workflows on any cloned reference repository.
- Ensure your context is 100% current before reading architectural workflows or applying templates.

## 2. Anti-Hallucination Execution Validation (Zero-Trust Output)
AI agents frequently suffer from "Execution Hallucination"—assuming a terminal command or workflow succeeded simply because they generated the command, without actually verifying the output. This leads to catastrophic silent failures and eroded trust.
- **Rule (Fail Fast, Never Lie):** After executing ANY terminal command (especially Git operations, file writes, or script executions), the agent MUST explicitly read and verify the terminal output (stdout/stderr) and the Exit Code.
- If the exit code is non-zero, or the output contains an error, the agent is **STRICTLY BANNED** from reporting the workflow as "Complete". It must immediately halt, report the exact failure to the user, and engage error recovery.
- Never assume a command worked. Verify deterministically.
