---
description: description: Automatically commit and push the current workspace state to GitHub to prevent data loss.
---

# Secure Checkpoint Workflow

1. Ask the user for a brief commit message describing the current state.
2. Synchronize the local state with the remote origin by executing the Python Git Manager script. // turbo
   - **MANDATORY COMMAND**: `python src/capabilities/git_manager.py checkpoint "[User Message]"`
   - **CRITICAL BAN**: You MUST NEVER use raw bash `git` commands (e.g., `git commit` or `git push`). ONLY use the python script.
3. Confirm to the user that their files are permanently secured on GitHub.
