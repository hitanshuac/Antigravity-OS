# Security & Access Control

## 1. Authentication & Authorization
- **App Access**: Yeti-Tracker is designed as a zero-trust local analytical tool. There is no user authentication implemented in the MVP dashboard.
- **API Access**: The application communicates with the Groq inference engine. The `GROQ_API_KEY` is strictly excluded from version control via `.gitignore` and must be provided via a local `.secrets/.env` file.

## 2. Input Validation (Defense in Depth)
- **Prompt Injection (CWE-74)**: All natural language inputs passed to the LLM are sanitized via the `sanitize_input()` function, which truncates length to 15,000 characters and strips structural characters (`<`, `>`, `{`, `}`).
- **Schema Validation**: The LLM output is strictly validated against the `ParsedPersonalData` Pydantic schema before it is allowed to interact with the UI.

## 3. Data Integrity & Idempotency
- **Error Observability**: The `log_error_to_json` function relies on a pre-write atomic temp-file rename to prevent corruption of the `error_logs.json` file if the process crashes during a write. It implements a rigorous post-write assertion check to guarantee data is never silently dropped.
- **Math Determinism**: The LLM does not execute math. The mathematical engine strictly reads typed integers from standard UI sliders.
