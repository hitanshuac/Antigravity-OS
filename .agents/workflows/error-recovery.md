# Circuit Breaker: Error Recovery Workflow

**Description:** This workflow defines the emergency "Circuit Breaker" protocol for handling severe API rate limiting or upstream outages, preventing endless retry loops and guaranteeing data state consistency.

## Workflow Steps

1. **Monitor API Responses**
   - Track HTTP status codes during the Extract (Fetch) phase.
   - Specifically watch for `429 Too Many Requests` or `503 Service Unavailable`.

2. **Trigger the Circuit Breaker**
   - If the system encounters three (3) consecutive `429` or `503` errors, immediately trip the circuit breaker.
   - Halt all further outbound API requests for the current execution cycle.

3. **Secure the Database State**
   - Trigger an immediate `duckdb-checkpoint` to flush the Write-Ahead Log (WAL) to disk.
   - This ensures that any data ingested prior to the failure is permanently saved and will not be lost.

3b. **Secure the File State (Non-Database Fallback)**
   > When project constraints prohibit heavy local databases (e.g., strict client guidelines), the Circuit Breaker must still protect data state using filesystem operations. See `rule-conflict-resolution.md` for why Tier 0 Safety overrides Tier 3 Compliance.
   - Before any file write operation, create a backup copy: `data/file.json` -> `data/file.json.bak`.
   - If the write operation fails, corrupts data, or the Pre-Write Verification (see `error-observability.md` Step 1.5) detects data loss, restore from the `.bak` backup immediately.
   - After a successful and verified write, the `.bak` file may be deleted to conserve disk space.
   - This ensures the same data-integrity guarantees as the DuckDB WAL checkpoint, using only filesystem operations.

4. **Graceful Exit**
   - Do not attempt endless retries.
   - Log a critical SRE alert detailing the rate limit failure.
   - Exit the pipeline gracefully with a non-zero status code, leaving the database ready for an idempotent retry once the upstream system recovers.
