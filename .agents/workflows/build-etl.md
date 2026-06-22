# Workflow: Build ETL Pipeline

**Trigger:** Explicit invocation via `/ask run @[.agents/workflows/build-etl.md] <data source description>`

## Objective
Scaffold and build a fault-tolerant ETL (Extract, Transform, Load) pipeline for a given data source. The agent must strictly follow the Pipeline Architect skill and all relevant governance rules.

## Pre-Conditions
1. The Product Templates in `.agents/product/templates/` MUST be populated and approved before executing this workflow. Specifically, the `02_TAD.md` (data flow) and `05_TICKETS.md` (backlog) must be complete.
2. The agent must load skills from `.agents/skills/` — specifically the **Pipeline Architect** (`pipeline-architect/SKILL.md`) and **DuckDB Optimizer** (`duckdb-optimizer/SKILL.md`).

## Execution Steps

### Phase 1: Schema Design
1. Read `02_TAD.md` § Database Schema to understand the target schema.
2. Design the DuckDB tables following `sql-standards.md` (idempotent `INSERT OR REPLACE`).
3. Define Pydantic models for incoming data following `data-validation.md`.

### Phase 2: Pipeline Construction
1. Build the Extract layer (HTTP clients, file readers, API integrations).
2. Build the Transform layer (data cleaning, normalization, type coercion).
3. Build the Load layer (DuckDB ingestion via staging tables).
4. Wire up the Dead-Letter Queue for Pydantic validation failures (`data/quarantine_*.parquet`).

### Phase 3: Observability
1. Integrate telemetry logging per `error-observability.md`.
2. Integrate the Circuit Breaker per `error-recovery.md`.

### Phase 4: Testing
1. Execute `.agents/workflows/test-automation.md` to generate and run the test plan for the ETL pipeline.
2. All tests must pass before handing the pipeline back to the user.
