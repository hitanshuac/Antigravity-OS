# Hack2Skill PromptWars: Strict Agent Constraints

The following rules are NON-NEGOTIABLE and dictate the boundaries of this repository. If you violate these, the project will be disqualified.

## 1. Git & Version Control (The Single-Branch Rule)
* **CRITICAL:** You are strictly forbidden from creating, suggesting, or checking out new Git branches. 
* All commits must be made directly to the `main` branch. 
* Do not generate complex merge/rebase workflows. Keep it strictly linear.

## 2. Storage & Asset Management (< 10MB Limit)
* The entire repository MUST stay under 10 MB.
* **No Bloat:** Do not suggest installing heavy dependencies.
* **Data Handling:** Do not generate or save large mock CSV/JSON files in the tracked repository. All database files (`.duckdb`), raw telemetry, and large datasets MUST be explicitly added to `.gitignore`.

## 3. The README.md Contract (Submission Requirements)
When asked to generate or update the `README.md`, you MUST include these exact sections prominently at the top:
1. **Vertical/Persona:** State clearly that this is the "Sustainability / Enterprise ESG" vertical built for an "Enterprise Sustainability Officer".
2. **Approach & Logic:** Explain the Bronze -> Silver -> Gold DuckDB pipeline.
3. **Assumptions Made:** List any technical or business assumptions we made during the hackathon sprint.

## 4. Evaluation Criteria (Code Standards)
All generated code must pass these quality gates:
* **Efficiency:** Use vectorized operations (PyArrow/DuckDB) over standard Python loops.
* **Testing:** Ensure components are modular and testable.
* **Accessibility:** Any frontend UI (HTML/React) must include semantic tags, ARIA labels, and proper contrast for enterprise accessibility standards.
