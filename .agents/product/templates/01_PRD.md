# Product Requirements Document (PRD)

**Project Name:** Yeti-Tracker: Indian Carbon Gamification Pivot
**Date:** 2026-06-18
**Status:** Approved

## 1. Objective
Build an "Indian Behavioral Variation & Anomaly Tracker" that helps individuals understand, track, and reduce their carbon footprint. The platform pivots away from a generic calculator to an enterprise-grade observability tool tracking daily variations against a mathematically rigorous deterministic floor (World Bank 2,500 kg baseline). It leverages gamification and a "Hybrid LLM Pipeline" to achieve this.

## 2. Target Audience / Personas
- **Persona 1 (The Indian Commuter):** A daily user looking for frictionless ways to log their day (e.g., Metro rides in Mumbai, AC usage during summer) and understand their financial and environmental impact.
- **Persona 2 (The Hackathon Judge):** An AI evaluator looking for proper integration of "Smart Assistants," dynamic intent-driven development, deterministic state tracking, and secure, high-quality code.

1. **The Continuous Confessional**: Frictionless data ingestion via an LLM parsing messy, natural language daily diaries, utilizing a recursive UI loop that tracks history per-session.
2. **The Verification Gate**: The LLM must populate human-verifiable UI sliders (strictly using Kilometers and Hours) to guarantee data integrity and bypass LLM math hallucinations.
3. **Sleep-Based Electricity Gamification**: Calculates an undeniable electricity baseline by extracting sleep vs. awake hours, removing abstract usage metrics in favor of daily behavioral reality.
4. **The INR Gamified Mirror & Anomaly Detection**: A deterministic DuckDB engine uses the 90th percentile `PERCENTILE_CONT(0.9)` to identify behavioral spikes against a static 2500 kg baseline, triggering "Catastrophe Tiers" and aggressive visual overrides.
5. **The Smart Yeti Advisor**: A secondary LLM call dynamically generates a personalized, context-aware reduction strategy (Maximum Impact vs. Convenience) guaranteeing at least a 20% footprint reduction without redundant advice.

## 4. Out of Scope (Non-Goals)
- **Complex 3D Topography**: Avoided to prevent UX lag and math instability.
- **Enterprise FinOps**: Pivoted away from SRE AWS data to align with the "individual" prompt requirement.
- **Vision LLMs**: Avoided due to severe latency and API constraints.

## 5. Success Metrics
- **Idempotency**: `f(x) = y` is guaranteed via DuckDB deterministic pipelines.
- **Zero Hallucination Mathematics**: The LLM has zero agency over the final calculations; math expressions are intercepted and computed strictly by the engine.
- **Emotional Resonance**: Measured by the visual impact of the Catastrophe tier override states and aggressive INR tax metrics.
