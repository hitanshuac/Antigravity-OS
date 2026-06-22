---
description: Critical constraints and requirements for deploying applications to Hugging Face Spaces.
---

# Hugging Face Spaces Deployment Standards

To ensure zero-cost, permanent offsite availability, applications are deployed to Hugging Face (HF) Spaces. Any changes to the architecture, dependencies, or deployment pipeline MUST adhere to the following constraints to prevent regressions or build failures.

## 1. Network & Container Constraints
* **Port Binding:** HF Spaces routes external traffic strictly to port `7860`. The application server must bind to `0.0.0.0:7860`.
* **Privilege Level:** The Docker container must run as a non-root user (uid `1000`).
* **Workers:** Free tier Spaces only allocate 2 vCPUs and 16GB RAM. Run the ASGI server with a single worker (`--workers 1`) to prevent OOM kills and CPU starvation.

## 2. Dependency Locking
* **Pin All Dependencies:** Always use pinned or range-locked versions in `requirements.txt` to prevent Docker build failures caused by upstream breaking changes.
* **Known Conflict:** If using `python-telegram-bot`, it strictly requires `httpx~=0.26.0`. Never upgrade `httpx` to `>=0.27.0` alongside it.

## 3. Deployment Mechanism (CI/CD ONLY)
* **No Git Push:** Do NOT use `git push` directly to the Hugging Face remote to avoid large file issues (LFS) and credential complexities.
* **Use the SDK:** Always deploy using the custom `upload_to_hf.py` script via the Hugging Face Hub SDK.
* **CRITICAL:** Do NOT run `upload_to_hf.py` locally. It must ONLY be executed by the `.github/workflows/deploy_hf.yml` GitHub Action runner which securely accesses the `HF_TOKEN`. All deployment triggers must happen via `git push origin main`.

## 4. UI Integration
* **Single Endpoint:** The Space exposes a single web port. If the application requires multiple interfaces (e.g., a dashboard and a chat console), they must be served on `/` via a unified, tabbed interface to maximize utility without requiring multi-container setups (which HF free tier does not support).
