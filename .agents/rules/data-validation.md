# Pydantic Data Validation Standards

This rule governs the data validation layer using Pydantic, focusing on fault tolerance and isolating bad records without halting the entire pipeline.

## 1. Non-Blocking Validation
- If incoming data violates the defined Pydantic schema, it must **NOT** crash the pipeline or raise an uncaught `ValidationError`.
- The pipeline must continue processing healthy records while safely isolating the malformed data.

## 2. Quarantine Protocol
- Any record that fails Pydantic validation must be caught and routed to a quarantine file.
- Save the bad records in a `.parquet` file located within the `data/` directory (e.g., `data/quarantine_YYYYMMDD.parquet`).
- Include the original payload and the specific validation error message in the quarantine record for manual review.

## 3. Graceful Degradation
- Allow partial batch successes. If a batch contains 90% valid data and 10% invalid data, the 90% must be ingested into DuckDB while the 10% is quarantined.
- Log a warning for SRE teams to review the quarantine file, but do not exit the pipeline with a non-zero status code solely due to validation failures.

## 4. File-Based Data Validation (Non-Database Contexts)

> **Post-Mortem Origin:** This rule was added after an incident where a JSON error log was silently wiped because the agent used raw `json.load()` + `isinstance()` instead of schema validation. The existing Rules 1-3 only covered DuckDB/pipeline contexts, leaving JSON files unprotected.

- **Rule**: When project constraints prohibit databases (e.g., strict client lightweight rules), the Pydantic validation mandate still applies to ALL persistent data files.
- **Why**: A JSON file is a schema-less database. Without validation, any code that reads it must guess the structure, and guesses can silently destroy data.
- **Action**:
  - Define a Pydantic model (or `TypedDict` with explicit validation) for every JSON/YAML/TOML file the application reads or writes.
  - Deserialize file content THROUGH the Pydantic model. If validation fails, route the error to the observability layer (`error-observability.md`) using the same quarantine pattern as Rule 2.
  - This rule applies even when the persistence layer is "just a JSON file." Treat it with the same rigor as DuckDB.
  - Reference: `defensive-programming.md` Rule 1, `rule-conflict-resolution.md` (Tier 0 Safety overrides Tier 3 Compliance).

## 5. Source Baseline Verification vs. Hallucinated Precision
- **Rule**: Never build highly specific tracking logic (e.g., splitting "Transit" into "CNG Bus", "Electric Bus", "AC Metro") unless the underlying reference dataset contains explicit, verified baseline KPIs for those exact sub-categories.
- **Why**: An idempotent system with mathematically robust logic is still generating a hallucination if the source baseline is unverified. Pretending to track carbon at a highly granular level using estimated or averaged baseline data destroys the integrity of the tracking application.
- **Action**:
  - Before expanding data models or Pydantic schemas to track granular habits, verify the source of truth (`data/emissions_factors.csv`, etc.).
  - If the dataset only contains generic `bus_km` (0.06 kg/km), do NOT split the UI/schema into `cng_bus` and `electric_bus` until verified metrics are obtained.
  - Grouping variables is acceptable if their baseline variance is minimal (< 10-20%). If variance is high but verified data is absent, flag it as a data dependency blocker rather than hallucinating an average.
