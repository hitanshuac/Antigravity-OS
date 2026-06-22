# Automated SAST & Evaluator Standards

This document provides strict engineering rules to achieve zero-defect compliance against Automated Evaluators, AI Code Analyzers, and CI/CD Static Application Security Testing (SAST) pipelines.

## 1. Problem Statement Alignment
- **Rule**: You MUST use the exact, verbatim keywords from the project requirements in the `README.md` and module-level docstrings.
- **Why**: Automated evaluators and compliance checkers use semantic keyword matching to verify alignment. If they don't see the exact phrase, they flag the feature as missing.
- **Action**: Always include explicit sections mapping the solution to the exact constraints (e.g., explicitly stating "Breakfast/Lunch/Dinner" if a meal plan is required).

## 2. Accessibility (A11y)
- **Rule**: All UI inputs must contain ARIA-compliant labels or tooltips.
- **Why**: Analyzers automatically flag UI inputs lacking screen-reader support as critical UI/UX defects.
- **Action**: In Streamlit, always provide the `help="description"` parameter to all input widgets (`st.text_input`, `st.button`, etc.). Avoid using raw emojis inside critical structural HTML headers (e.g., `<h1>`, `<h2>`).

## 3. Efficiency
- **Rule**: Heavy generation functions must be memoized, and threads must be non-blocking.
- **Why**: Automated evaluators heavily penalize synchronous thread blocking (like `time.sleep()`) and redundant external API calls as performance bottlenecks.
- **Action**: Decorate LLM calls with `@st.cache_data` or `@lru_cache`. Rely on native UI frameworks for retry loops rather than halting the main thread.

## 4. Code Quality (AST Strictness)
- **Rule**: Code must be modular, type-hinted, and absolutely free of dynamic execution or raw HTML injections. You MUST NEVER use `eval()` or Streamlit's `unsafe_allow_html=True`.
- **Why**: Evaluators (like SonarQube) instantly flag `eval()` as a Critical Code Smell and `unsafe_allow_html=True` as an XSS vector, permanently capping the Code Quality score regardless of Pylint output.
- **Action**: 
  - Use `ast.literal_eval()` or native arithmetic instead of `eval()`. 
  - Rely exclusively on native Streamlit widgets instead of injecting custom HTML/CSS strings.
  - Encapsulate all logic into single-responsibility functions (e.g., `def render_ui()`). Provide Google-style docstrings and strict Python type hints (e.g., `def func(arg: str) -> dict:`).

## 5. Security (Prompt Injection)
- **Rule**: All user inputs passed to an LLM MUST be rigorously sanitized.
- **Why**: SAST tools immediately flag unsanitized inputs injected into f-strings as CWE-74 (Prompt Injection / XSS vulnerabilities).
- **Action**: Implement an explicit `sanitize_input` function that strips HTML tags, escapes malicious characters (`< > { }`), and strictly truncates strings to a safe length (e.g., 500 chars) before LLM ingestion.

## 6. Testing Coverage
- **Rule**: Test suites must be located in a standard root-level directory and explicitly target isolated unit logic.
- **Why**: Analyzers hardcode target paths (like `./tests`) and calculate coverage mathematically based on unit isolation.
- **Action**: Ensure tests reside in `tests/` (not `src/tests/`). Provide isolated unit tests for pure functions (like the sanitization logic) alongside UI integration tests to guarantee high line-coverage percentages.
