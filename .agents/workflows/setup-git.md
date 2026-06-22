---
description: Autonomously initialize Git, provision a remote GitHub repository, and link them using the official GitHub CLI.
---

# Setup Git Workflow

This workflow ensures the local workspace is securely connected to a remote GitHub repository, completely eliminating manual gatekeeping.

## Prerequisites
- The official GitHub CLI (`gh`) must be installed and authenticated.

## Execution Steps

1. **Verify Git Initialization**
   - Check if the repository is initialized locally (`git status`).
   - If not, execute `git init` and perform an initial safe commit.

2. **Verify GitHub CLI**
   - Execute `gh auth status` to verify the user is logged into GitHub.
   - If `gh` is missing, run `winget install --id GitHub.cli --silent --accept-source-agreements --accept-package-agreements` (on Windows).
   - If `gh` is installed but unauthenticated, instruct the user to run `gh auth login` in their terminal and pause execution until they confirm.

3. **Provision Remote Repository**
   - Check if an `origin` remote exists via `git remote -v`.
   - If missing:
     - Scan the `README.md` to extract the Project Title and Description.
     - Execute `gh repo create "<Extracted_Title>" --private --source=. --remote=origin --description "<Extracted_Description>"` to seamlessly create the repository on GitHub and link it to the local folder.

4. **Verify Linkage**
   - Execute `git remote -v` to ensure the `origin` is now correctly bound.
   - The environment is now fully connected and ready for `git push`.

5. **Inject Remote Secrets**
   - Once the remote repository is established, you must immediately seed it with deployment credentials.
   - Execute `.agents/workflows/setup-secrets.md` to prompt the user and inject the required API keys via `gh secret set`.
