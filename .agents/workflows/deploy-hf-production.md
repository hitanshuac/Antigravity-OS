---
description: Universal Master workflow to deploy ANY codebase as a Docker container to Hugging Face Spaces.
---

# Universal HF Production Deployment Workflow

This workflow orchestrates the deployment pipeline. It is entirely language-agnostic and relies on Hugging Face Docker Spaces to deploy arbitrary environments (Node.js, Go, Rust, Python, etc.) via native Git commands.

## Step 1: Pre-Flight Credential & Asset Provisioning
1. Execute the `.agents/workflows/setup-secrets.md` workflow.
2. Ensure `HF_TOKEN` and `HF_SPACE_REPO` are securely pushed to GitHub Actions via the `gh` CLI.
3. **IMAGE CHECK (CRITICAL)**: Scan the repository for any `*.jpg`, `*.png`, or `*.webp` files. If any binary image files exist in the repository (e.g., in `data/assets/`), Hugging Face Spaces will silently fail to clone the repository without Git LFS configured.
   - **Action**: If images exist, **HALT** this workflow immediately and execute `.agents/workflows/deploy-streamlit-production.md` instead. Do not proceed with HF Deployment.

## Step 2: Stack Detection & Dockerization
To deploy a generic repository to Hugging Face Spaces, it MUST use a Docker Space.
1. **Detect Language Stack:** Identify the repository's core framework.
2. **Generate Dockerfile:** If a `Dockerfile` does not exist at the repository root, create one.
   - **CRITICAL HF DOOCKER RULES:**
     - The container MUST expose port `7860`.
     - The container MUST run as a non-root user (e.g., `RUN useradd -m -u 1000 user`).
     - The application MUST bind to `0.0.0.0:7860`.

## Step 3: HF Frontmatter Injection
Hugging Face requires a specific YAML block at the very top of `README.md` to configure the Space.
1. Scan the top of `README.md`.
2. Ensure the following frontmatter exists and is accurate:
   ```yaml
   ---
   title: <Project Name>
   emoji: 🚀
   colorFrom: blue
   colorTo: indigo
   sdk: docker
   app_port: 7860
   pinned: false
   ---
   ```

## Step 4: Codebase-to-Document Synchronization
1. Synchronize API schemas, route definitions, and architecture diagrams across `docs/` and `.agents/rules/`.
2. Update version designations to the current release (e.g., `v1.0.0`).
3. Ensure the recruiter-facing static PNG and technical Mermaid flow are visible in `README.md`.

## Step 5: Git-Native Deployment to Hugging Face
**DO NOT** use custom Python scripts (like legacy `upload_to_hf.py`) to deploy. Hugging Face Spaces are standard Git repositories.
1. Ensure `.github/workflows/deploy_hf.yml` is configured to push the codebase directly to Hugging Face using the secrets.
   Example Action snippet:
   ```yaml
   - name: Push to HF Spaces
     run: git push https://user:${{ secrets.HF_TOKEN }}@huggingface.co/spaces/${{ secrets.HF_SPACE_REPO }} main
   ```
2. Commit and push all local changes to GitHub (`origin/main`).
3. The GitHub Action will trigger and seamlessly clone the repo into the Hugging Face Space.
