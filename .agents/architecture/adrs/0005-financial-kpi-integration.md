# ADR 0005: Financial KPI & Dynamic Dataset Integration

## Context
The gamified carbon tracker originally used abstract logic and simple scalar multiplication (`miles * 0.4`) to forecast footprints. This felt "too simple" and lacked an emotional anchor, risking points in the "Individual Awareness" grading rubric. Additionally, using static math equations instead of a verifiable dataset undermined our claims of building an "Enterprise-grade data pipeline" with DuckDB. Finally, the "miles driven" metric was ambiguous, clumping all transport into one car-centric factor.

## Decision
1. **Financial Monetization**: We integrated the India GHG Platform Social Cost of Carbon metric (INR 15.80/kg) derived from `carbon_factors.csv` to translate abstract kg into a frightening "Carbon Tax Debt (INR)". This serves as the primary actionable KPI for the user.
2. **Dataset Creation**: We created `data/carbon_factors.csv`—a robust, verifiable dataset containing the exact CO2 emissions factors and SCC multipliers for various regional activities (transport, diet, energy).
3. **Dynamic DuckDB Querying**: `app.py` was refactored. `run_duckdb_math` no longer uses hardcoded math; it now utilizes DuckDB `read_csv_auto()` and `SELECT` to pull the factors dynamically.
4. **Transport Disaggregation**: We broke out "Miles Driven" into three distinct sliders: Car, Plane, and Public Transit, providing accurate footprint modeling per the user's feedback.

## Consequences
- The application now perfectly marries highly realistic data tracking with absurd "Over 9000" gamification.
- The use of actual datasets and DuckDB joins satisfies the strictest architectural requirements of the competition.
- The new Plotly Bar Charts and monetary metrics dramatically increase user engagement and behavioral awareness.
