# Enterprise Code Quality Standards

This document codifies the strict requirements for achieving a perfect maintainability and reliability score against automated SAST and AI Code Analyzers (e.g., SonarQube, DeepSource). These rules must be strictly adhered to during all code generation and refactoring.

## 1. Project Structure & Imports (Pylint/Flake8 Compliance)
- **Rule**: Never use `sys.path.append()` hacks.
- **Why**: Analyzers heavily penalize runtime `sys.path` manipulation, flagging them as `E0401` (Unable to import) and `C0413` (Wrong import position).
- **Action**:
  - Ensure every package directory (`src/`, subdirectories, `tests/`) has an `__init__.py` file.
  - Rely on `pyproject.toml` or `conftest.py` for path resolution.
  - All imports must be at the top of the file, ordered: stdlib -> third-party -> local (isort standard).

## 2. Formatting & Cleanliness
- **Rule**: Code must be meticulously formatted with zero PEP-8 hygiene violations.
- **Why**: Evaluators deduct points proportionally for trailing whitespace (W291) and structural issues.
- **Action**:
  - **Zero trailing whitespace** in any file.
  - Exactly **2 blank lines** between top-level function/class definitions.
  - Maximum line length of **120 characters**.
  - No blank line at the end of the file (W391), just a single newline.

## 3. Strict Linting Requirements
- **Rule**: Eliminate all code smells and anti-patterns.
- **Why**: Analyzers look for common Python pitfalls.
- **Action**:
  - **No broad exceptions**: Replace `except Exception as e:` with specific exceptions like `except (ValueError, ConnectionError):`.
  - **No inline imports**: Never `import` inside a function.
  - **No mutable defaults**: Change `def func(arg: dict = None):` to `def func(arg: Optional[dict] = None):`.
  - **No pointless re-raises**: Avoid using `raise e` inside an except block without adding context.
  - **Zero Hacks**: NEVER use `# pylint: disable` or `# noqa` suppression comments. You must natively fix the underlying AST violation to pass structural AI evaluators.

## 3.5 Structured Error Handling (12-Factor XI: Logs)
- **Rule**: Exception handlers must NEVER swallow errors with generic static messages.
- **Why**: Generic fallback strings (e.g., "Something went wrong", "I'm having trouble connecting") violate 12-Factor Factor XI (Logs as Event Streams), make debugging impossible, and waste significant developer time. See `defensive-programming.md` Rule 2 for the full mandate.
- **Action**:
  - Every `except` block must log `type(e).__name__` and `str(e)` to the observability layer (`error-observability.md`) BEFORE returning any user-facing message.
  - The user-facing message MAY be friendly and generic, but the log entry MUST contain the real exception class, message, and component.
  - Replace bare `except:` and `except Exception:` with specific exception types. If a catch-all is truly needed, it must be the LAST handler and must log at ERROR level with full context.
  - Reference: `defensive-programming.md` Rule 2, `rule-conflict-resolution.md` Tier 0.

## 4. Cyclomatic Complexity (Radon CC = A-Grade)
- **Rule**: All functions must score an 'A' grade (CC ≤ 5).
- **Why**: High complexity scores (B-grade and above) deduct from the maintainability index.
- **Action**:
  - If a function exceeds CC=5, extract branching logic into private helper functions.
  - **Pre-compile regex patterns** (`re.compile`) at the module level rather than inside functions.
  - Extract magic numbers and strings into uppercase module constants.
  - Keep functions under 25 lines of core logic.

## 5. Documentation & Typing
- **Rule**: Every function and module must be typed and documented.
- **Why**: Missing docstrings and types trigger Pylint/Mypy penalties.
- **Action**:
  - Include a module-level docstring at the top of every `.py` file.
  - Use **Google-style docstrings** with explicit `Args:`, `Returns:`, and `Raises:` sections.
  - Add explicit type hints on every parameter and return value.
  - Void functions must explicitly declare `-> None`.

## 6. Pre-Push Verification Commands
Before concluding any major codebase update, run the following verification suite:
```bash
pylint src/ --fail-under=9.5
flake8 src/ tests/ --max-line-length=120 --count
radon cc src/ -a -s -n B   # Output must be empty
radon mi src/ -s           # All must be 'A'
pytest tests/ -v           # All must pass
```
