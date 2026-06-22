# Agent Execution Standards

This rule governs the fundamental operational behaviors of any AI agent operating within or pulling from this environment.

## 1. Assert State Currency (Anti-Staleness Protocol)
AI agents have a tendency to hallucinate templates or operate blindly on stale local clones.
- **Rule:** You MUST always assert state currency by running `git pull origin main` immediately prior to executing read/scaffold workflows on any cloned reference repository.
- Ensure your context is 100% current before reading architectural workflows or applying templates.
