# Technical Architecture Document (TAD)

## 1. System Overview
Yeti-Tracker is a Streamlit-based monolithic Python application. It leverages a Hybrid LLM pipeline (Groq), a localized embedded OLAP database (DuckDB), and robust schema validation (Pydantic) to securely manage the transition from natural language inputs to deterministic mathematical outputs.

## 2. Component Architecture
1. **Frontend (Streamlit)**: Single-page application rendering the "Continuous Confessional" loop, verification sliders, Plotly gauges, and conditional Catastrophe image overrides.
2. **Ingestion Layer (Groq LLM + Pydantic)**: A prompt-engineered LLM (`llama-3.3-70b-versatile`) extracts exactly six data points (Car KM, Flight KM, Transit KM, Daily Sleep Hours, Sleep AC On, Daytime AC Hours, Restaurant Meals). A regex-based mathematical interceptor (`_recover_failed_generation`) parses failed mathematical expressions to ensure valid JSON payload extraction.
3. **Deterministic Core (DuckDB)**: A mathematically isolated SQL engine that calculates the cumulative CO2 footprint based *only* on the verified slider inputs and a static 2,500 kg baseline. It tracks session history persistently via UUID and uses `PERCENTILE_CONT(0.9)` to statically detect behavioral variations and spikes against historical data.
4. **Advisory Layer & RAG (Groq LLM)**: The `get_yeti_advice` function uses DuckDB Full-Text Search to pull real Social Cost of Carbon (SCC) values, providing dynamic, gamified reduction strategies at the end of the pipeline based on the Indian baseline.
5. **Observability**: `log_error_to_json` implements a thread-safe, idempotent, strictly typed JSON error logging mechanism per Tier 0 SRE rules.

## 3. Data Flow
`User Text -> LLM JSON -> Math Interceptor -> UI Sliders -> User Approval -> DuckDB Math -> UUID History DB -> UI Gamification -> DuckDB FTS -> LLM Yeti Advisor`

## 4. Dependencies
- **Core**: Python 3.11+, Streamlit
- **Data**: DuckDB, Pydantic
- **AI**: Groq API
- **Visuals**: Plotly, Custom AI-generated PNG assets.
