---
description: Mandatory error logging, monitoring, and context compression workflow.
---

# Error Observability & Remediation Workflow

This workflow forces strict error logging, historical context checking, and resolution documentation to ensure the AI agent never repeats past mistakes, while maintaining strict context window compression constraints.

## Step 1: Pre-Execution Log Verification (Mandatory)
Before generating or modifying any code, the agent MUST:
1. Check for the existence of `data/error_logs.json`. If it does not exist, initialize it as an empty JSON array `[]`.
2. **Canonical Schema Contract:** The `data/error_logs.json` file MUST conform to this exact schema:
   ```json
   [
     {
       "timestamp": "2026-06-13T12:49:00+05:30",
       "error_type": "AssertionError",
       "component": "tests/test_sanitization.py",
       "message": "Phone regex failed on international format",
       "stack_trace_summary": "line 42 in test_phone_masking",
       "status": "UNRESOLVED",
       "resolution_strategy": null
     }
   ]
   ```
   The file is a **JSON array** of objects. Each object MUST contain: `timestamp` (str), `error_type` (str), `component` (str), `message` (str), `status` (str: `"UNRESOLVED"` or `"RESOLVED"`). Optional: `stack_trace_summary` (str), `resolution_strategy` (str or null).
3. **Schema Migration:** If the existing file contains a DIFFERENT structure (e.g., a dictionary `{"session_errors": [...]}` from a prior session), the agent MUST migrate the data into the canonical array format BEFORE appending. The agent MUST NEVER overwrite or discard existing entries. See `defensive-programming.md` Rule 1.
4. **Database Scaling:** If `data/error_logs.json` becomes too large or inefficient to query, the agent MUST autonomously initialize a local database (e.g., `data/error_metrics.db` via SQLite or DuckDB) to migrate and store all future error context.
5. Read the recent error history (from JSON or DB) to understand past failures and attempted fixes.
6. **DO NOT** repeat strategies that have already been documented as "failed" in the logs.

## Step 1.5: Pre-Write Verification (Data Integrity Gate)
Before writing to ANY persistent file (not just error logs), the agent MUST:
1. Read the current file content and deserialize it.
2. Count the existing entries (e.g., `len(logs)` for the error log array).
3. Perform the append/update operation.
4. After writing, re-read the file and verify the entry count is exactly `previous_count + N` (where N is the number of new entries).
5. If the count is wrong (data was lost or corrupted), immediately halt, restore from backup (see `error-recovery.md` Step 3b), and flag for user review.
6. Reference: `defensive-programming.md` Rule 3 (Idempotent File Operations).

## Step 2: Context Window Compression (jCodeMunch)
To avoid overloading the LLM context window with raw stack traces and massive log files:
1. Use the **jCodeMunch** MCP Server (configured in `.config/antigravity/mcp.json`) to retrieve only the relevant structural symbols or AST nodes related to the error.
2. Instead of dumping raw file contents, extract and summarize the specific function/class where the failure occurred.
3. Keep log entries concise. Extract the core exception message and the exact line of failure.

## Step 3: Monitor & Log Failures
When an error, test failure, or pipeline crash occurs:
1. Append a new entry to the error log following the canonical schema from Step 1.
2. Format:
   - `timestamp`: Current UTC time (ISO 8601 with timezone).
   - `error_type`: The exact Python exception class name (e.g., `ValueError`, NOT `"Error"`).
   - `component`: The function or module that broke (retrieved via jCodeMunch).
   - `message`: The actual `str(e)` from the exception. NEVER a generic placeholder.
   - `stack_trace_summary`: A highly compressed summary of the stack trace.
   - `status`: `"UNRESOLVED"`.
3. Execute the Pre-Write Verification gate (Step 1.5) to confirm no data was lost.

## Step 4: Document the Fix
After successfully resolving an error and passing tests:
1. Return to the error log and update the specific entry.
2. Change `status` to "RESOLVED".
3. Add a `resolution_strategy` field detailing *exactly* what was changed to fix the issue.
4. Keep this resolution brief to conserve future context windows.
