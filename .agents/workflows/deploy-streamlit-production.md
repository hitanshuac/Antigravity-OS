---
description: Universal Master workflow to deploy Streamlit applications to Streamlit Community Cloud natively.
---

# Streamlit Production Deployment Workflow

**Trigger:** Explicit invocation via `/ask run @[.agents/workflows/deploy-streamlit-production.md]` or fallback from HF Spaces.

This workflow is explicitly designed for deploying Python-based Streamlit applications. It relies on **Streamlit Community Cloud**, which seamlessly integrates with GitHub and natively supports binary file ingestion (images, databases) without requiring Git LFS overhead or explicit Dockerization.

## Step 1: Pre-Flight Application Checks
1. Verify the repository has a `requirements.txt` containing `streamlit` and all necessary dependencies.
2. Verify the primary application entrypoint (e.g., `app.py` or `streamlit_app.py`) exists at the root of the repository.
3. Verify that all asset loading (images, data CSVs) uses **absolute paths** computed at runtime (e.g., `Path(__file__).parent.resolve()`) to prevent Linux pathing errors on the Streamlit Cloud container.

## Step 2: GitHub Synchronization
Streamlit Community Cloud pulls directly from the public GitHub repository.
1. Ensure the repository is Public (per Hack2Skill requirements).
2. Execute the `.agents/workflows/master-sync.md` workflow to strictly format, lint, test, and checkpoint the repository.
3. Push all changes to the `main` branch.

## Step 3: Streamlit UI Connection
Since Streamlit Cloud requires OAuth access to the developer's GitHub, the agent cannot perform the final deployment button-click. The agent MUST instruct the user to complete the following manual UI sequence:

1. Log into [Streamlit Community Cloud](https://share.streamlit.io/).
2. Click **New app** -> **Deploy a public app from GitHub**.
3. Paste the repository URL (e.g., `HitanshuAC/project-name`).
4. Set the **Main file path** (e.g., `app.py`).
5. Set a custom App URL if desired (e.g., `my-project.streamlit.app`).

## Step 4: Secret Injection (CRITICAL)
If the project uses API keys (e.g., `GROQ_API_KEY`):
1. The agent MUST instruct the user to click **Advanced Settings** before hitting Deploy.
2. The agent MUST generate a TOML-formatted block of the necessary secrets for the user to copy-paste.
   *Example TOML:*
   ```toml
   GROQ_API_KEY = "your_key_here"
   ```
   *(Note: Strings MUST be enclosed in double quotes in TOML, unlike standard `.env` files).*

## Step 5: Smoke Test
1. After the user clicks Deploy and the app finishes building, the agent must ask the user to verify the live URL.
2. Confirm that images load correctly and that any LLM fallback logic successfully triggers.
