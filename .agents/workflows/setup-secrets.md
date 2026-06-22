---
description: Autonomously audit, prompt, and securely inject required API keys into GitHub Secrets via the GitHub CLI.
---

# Setup Secrets Workflow

This workflow ensures the executing Agent autonomously establishes the required CI/CD credentials securely in the GitHub repository, eliminating the need for humans to use a web browser.

## Prerequisites
- The official GitHub CLI (`gh`) must be installed, authenticated, and linked to the target repository (completed via `setup-git.md`).

## Execution Steps

1. **Audit Existing Secrets**
   - Execute `gh secret list` in your terminal to view all currently configured GitHub Actions secrets.
   - Cross-reference this list against the required secrets for your current deployment pipeline (e.g., `HF_TOKEN`, `HF_SPACE_REPO`).

2. **Prompt the Human (If Missing)**
   - If any required secrets are missing, immediately halt execution.
   - Politely ask the human user in the chat to provide the exact values for the missing secrets.
   - **Agent Rule:** Never hallucinate API keys. Only proceed once the user has explicitly provided them in the chat.

3. **Securely Inject Secrets**
   - Once the user provides a secret, use your terminal execution tool to inject it into the repository:
     ```bash
     gh secret set <SECRET_NAME> -b"<PROVIDED_VALUE>"
     ```
   - Do this for every missing secret.

4. **Verify Configuration**
   - Execute `gh secret list` one final time to assert that the missing secrets have been successfully stored and are now active in the repository.
   - Report success to the user and seamlessly resume the parent deployment workflow.
