# Execution Backlog (Tickets)

All tickets for the Yeti-Tracker Hack2Skill project have been completed.

- `[x]` **TICKET-001: Establish Observability**
  - Implement Tier-0 error logging via `log_error_to_json`.
  - Enforce pre-write validation and atomic file renames.

- `[x]` **TICKET-002: LLM Ingestion Pipeline**
  - Integrate Groq (`llama-3.1-8b-instant`).
  - Write `parse_messy_text()` with strict Pydantic schema fallback logic.

- `[x]` **TICKET-003: DuckDB Math Engine**
  - Implement `run_duckdb_math()` to forecast 365-day carbon footprints and tree offsets.

- `[x]` **TICKET-004: Frontend Visuals (Normal State)**
  - Implement dark-mode Plotly Gauges via `create_gauge_fig`.

- `[x]` **TICKET-005: Gamification Pivot ("Over 9000")**
  - Generate AI image assets (`tier2_alert.png`, `tier3_alert.png`).
  - Implement dynamic UI overrides based on mathematical thresholds.

- `[x]` **TICKET-006: Human-in-the-Loop Hybrid Gate**
  - Bind LLM output to standard UI Sliders.
  - Decouple LLM hallucination risk from the DuckDB Math Engine.

- `[x]` **TICKET-007: Yeti Advisor**
  - Implement secondary LLM call (`get_yeti_advice()`) for dynamic reduction strategies.

- `[x]` **TICKET-008: Indian Carbon Engine Pivot**
  - Transition from USD/miles to INR/km based on the ₹15.80/kg Social Cost of Carbon (SCC).
  - Modify LLM extraction parsing layer to recover from mathematical expressions (Regex Evaluator).
  - Force Continuous Confession loop, updating UUID session state natively.

- `[x]` **TICKET-009: Behavioral Variation Tracker Pivot**
  - Anchor baseline statically to World Bank 2500 kg to prevent double-counting of survival electricity.
  - Implement Sleep-based gamification logic for electricity footprint (Sleep vs Awake vs Daytime AC).
  - Expose DuckDB `PERCENTILE_CONT(0.9)` anomaly detection math directly in the UI.

- `[x]` **TICKET-010: High-Fidelity Transport & Scientific Transparency**
  - Refactored LLM schemas to separate `two_wheeler_km` and `auto_rickshaw_km` from `car_km`.
  - Display full transparency matrix (Agencies, Factors) via `carbon_factors.csv`.
  - Fix JSON validation math expressions in Groq payload.
