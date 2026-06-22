# Quarantine & Dead-Letter Queue (DLQ)

This rule establishes the standard operating procedure for handling malformed data and Pydantic validation failures.

## Directives

1. **Never Crash the Loop:** When an ingestion pipeline encounters data that fails Pydantic schema validation, it MUST NOT crash the main application process or event loop.
2. **Isolate Failures:** Malformed data must be safely caught and isolated to prevent upstream and downstream corruption.
3. **Route to DLQ:** All validation failures must be routed to the Dead-Letter Queue (DLQ). The required location for this is `data/quarantine_log.parquet`.
4. **Observability:** Ensure that the original payload, the validation error message, and a timestamp are logged alongside the quarantined record so that agents can autonomously diagnose and retry the processing later.
