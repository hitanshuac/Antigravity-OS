# Testing Standards

This rule governs all testing practices across the Agentic Environment. It enforces industry-standard test structure, naming, and the strict prohibition of shipping untested code.

## 1. Never Ship Untested Code
- Every function, route, and pipeline component that is part of a ticket in `05_TICKETS.md` MUST have at least one corresponding test.
- If a ticket has no acceptance criteria, the agent must ask the user to define them before proceeding.
- Pull Requests with zero test coverage on new code MUST be rejected by CI.

## 2. Test Pyramid Enforcement
- **Unit Tests** must form the majority (~70%) of the test suite. They test pure logic in isolation with mocked dependencies.
- **Integration Tests** (~20%) test boundaries between components (e.g., API → database, validator → DLQ).
- **End-to-End Tests** (~10%) test the full user-facing flow. These are the most expensive and MUST be used sparingly.

## 2.5 State-Aware Integration Tests (Mandatory for I/O)

> **Post-Mortem Origin:** This rule was added after unit tests using Pytest `tmpdir` (clean-slate isolation) passed 100% but missed a critical schema mismatch with a real production file. The bug silently wiped `data/error_logs.json`.

- **Rule**: Any module that reads or writes persistent files (JSON, DB, Parquet) MUST have at least one integration test that operates on pre-populated fixture data matching the REAL production schema.
- **Why**: Unit tests with `tmpdir` only verify that code works on a clean slate. They cannot catch schema mismatches between what the code expects and what the data actually looks like.
- **Action**:
  - Create test fixtures in `tests/fixtures/` containing representative samples of real production data (e.g., `tests/fixtures/error_logs_sample.json`).
  - Integration tests must read from these fixtures, perform the operation (e.g., append a log entry), and verify no data was lost or corrupted.
  - At minimum, assert: `len(after) >= len(before)` for all append operations.
  - Fixtures must include edge cases: empty files, files with the canonical schema, and files with legacy schemas (e.g., the old dictionary format) to verify migration logic.
  - Reference: `defensive-programming.md` Rule 1 (Schema-First Data Contracts).

## 3. Naming Conventions
- Test files: `test_<module_name>.py` (e.g., `test_compaction.py`)
- Test functions: `test_<feature>_<behavior>_<expected>` (e.g., `test_compaction_strips_filler_prefix_correctly`)
- Test classes (when grouping): `TestCompaction`, `TestDLQRouting`

## 4. Fixture & Setup Standards
- Shared fixtures must be defined in `src/tests/conftest.py`.
- Database tests must use in-memory DuckDB instances (`:memory:`) unless testing persistence specifically.
- API tests must use FastAPI's `TestClient` — never make real HTTP calls in unit tests.
- External API dependencies must be mocked using `unittest.mock` or `pytest-mock`.

## 5. Test Execution Protocol
- Tests must be run after **every** code change, not just at the end of a feature.
- Use `python -m pytest src/tests/ -v --tb=short` as the standard command.
- The CI/CD pipeline (`.github/workflows/main.yml`) must run the full test suite on every push.

## 5.5 Contract Tests for Data Schemas

- **Rule**: Every Pydantic model or `TypedDict` used for file I/O MUST have a corresponding contract test that validates a known-good fixture file against the model.
- **Why**: Contract tests catch schema drift between what the code expects and what the data actually looks like. They are the bridge between unit tests (which test logic) and integration tests (which test boundaries).
- **Action**:
  - Test file: `tests/test_contracts.py`
  - Each test loads a fixture file from `tests/fixtures/` and asserts it deserializes successfully through the Pydantic model without validation errors.
  - If a fixture fails validation, the TEST fails (not the app). This ensures schema changes are intentional and documented, not accidental.
  - Contract tests must run BEFORE integration tests in the test suite execution order.
  - Reference: `data-validation.md` Rule 4, `defensive-programming.md` Rule 1.

## 6. Failure Handling
- If a test fails, the agent must first check `.agents/workflows/error-observability.md` for historical context.
- The agent must fix the **implementation code**, not weaken the test, unless the test itself contains a genuine error.
- After 3 failed debugging iterations on the same test, the agent must flag it for manual user review and move on.

## 7. Anti-Solipsism Verification (Human Testing)
- **Rule:** Never rely solely on internal, solipsistic verification (reading your own terminal outputs).
- Always explicitly provide the human user with the exact, step-by-step UI and CLI testing commands required to run and test the full-stack system locally (e.g., how to start the backend, how to start the frontend, what URL to open) upon completion of any task.
