# Gamification Pivot and the Hybrid Deterministic Pipeline

Date: 2026-06-16

## Status

Accepted

## Context

For Hack2Skill Challenge 3 ("Prompt Wars Virtual"), the core application must be a "Carbon Footprint Awareness Platform" that helps *individuals* understand, track, and reduce their carbon footprint. The SME emphasized creating an "emotional, behavioral, or cognitive connection" (e.g., gamification).

Our initial architecture pivoted to a highly technical "SRE GreenOps/FinOps Engine" using DuckDB CROSS JOINS on CCF AWS instance data. While mathematically robust, this completely missed the "individual awareness" prompt constraint and risked failing the AI grading rubric.

Furthermore, we attempted to use an LLM (`llama-3.1-8b-instant`) to parse natural language into math variables. We discovered that LLMs are statistically non-deterministic, meaning the exact same string could yield different numbers, destroying the idempotency and scientific integrity of our math engine.

## Decision

We executed a "Gamification Pivot" with the following architectural components:
1. **The "Over 9000" Metaphor**: We abandoned AWS data and returned to Personal Tracking. If the user's carbon footprint exceeds 9,000kg/year, the sleek UI "breaks" and massive AI-generated assets (a dynamic Catastrophe Tier visual) overtake the screen. This satisfies the SME's gamification and emotional awareness requirement.
2. **The Hybrid Pipeline**: To solve the LLM non-determinism, we implemented a "Human Verification Gate". The LLM parses a user's natural language "diary" (e.g., "I drove 20 miles") and updates explicit Streamlit Sliders. The DuckDB math engine *only* pulls from the Sliders, never the raw LLM output.
3. **The Yeti Advisor**: To fulfill the "Smart Dynamic Assistant" requirement, we added a secondary LLM call at the end of the pipeline that uses the deterministic math to dynamically generate a sarcastic, personalized reduction strategy.

## Consequences

* The application mathematically guarantees that `f(x) = y` every single time, preserving data integrity.
* The application perfectly fulfills the Hackathon rubric (Individual Awareness, Gamification, Smart Assistant).
* By using LLMs on both the ingestion side (parsing text) and output side (generating personalized advice), we fully demonstrate "intent-driven development using AI orchestration."
