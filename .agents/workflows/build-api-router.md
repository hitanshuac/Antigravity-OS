# Workflow: Build API Router

**Trigger:** Explicit invocation via `/ask run @[.agents/workflows/build-api-router.md] <API description>`

## Objective
Scaffold and build a production-grade FastAPI router cascade. The agent must follow the 12-Factor methodology, Router Alignment rule, and all security governance.

## Pre-Conditions
1. The Product Templates in `.agents/product/templates/` MUST be populated and approved before executing this workflow. Specifically:
   - `02_TAD.md` (component architecture and data flow)
   - `03_SECURITY.md` (authentication strategy, RBAC, secret management)
   - `04_FRONTEND.md` (API contracts)
2. The agent must reference `.agents/rules/router_alignment.md` for system prompt injection and `.agents/rules/context_compaction.md` for payload management.

## Execution Steps

### Phase 1: Route Design
1. Read `04_FRONTEND.md` § API Contracts to understand the expected endpoints.
2. Read `03_SECURITY.md` to understand the authentication and authorization strategy.
3. Design the route structure following RESTful conventions.

### Phase 2: Router Construction
1. Build FastAPI route handlers in `src/`.
2. Implement the system prompt injection per `router_alignment.md`.
3. Implement the Context Compaction pipeline per `context_compaction.md`.
4. Wire up Pydantic request/response models per `data-validation.md`.

### Phase 3: Security Hardening
1. Implement authentication middleware as specified in `03_SECURITY.md`.
2. Ensure all secrets are loaded via environment variables per `12-factor-rules.md` Factor III.
3. Apply CORS, rate limiting, and input sanitization.

### Phase 4: Testing
1. Execute `.agents/workflows/test-automation.md` to generate and run the test plan for the API routes.
2. All tests must pass before handing the router back to the user.
