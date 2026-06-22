# Idempotency Standards

This rule mandates that all database operations, especially those interacting with DuckDB, must be fully idempotent.

## Directives

1. **No Duplicate Records:** Running the same write or insert operation multiple times must yield the exact same database state as running it once.
2. **Use INSERT OR REPLACE:** When writing to DuckDB, always use `INSERT OR REPLACE INTO ...` instead of `INSERT INTO ...` to prevent duplication on retry loops.
3. **Primary Keys:** Ensure every table has a strongly defined primary key or unique constraint to support the `REPLACE` mechanism.
4. **Data Integrity:** Idempotent operations are critical for fault tolerance, allowing Agentic pipelines to safely retry failed runs without corrupting data state.
