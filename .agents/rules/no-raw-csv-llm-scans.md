# Strict Constraint: No Raw CSV LLM Scans

This rule applies to all ingestion, auditing, and scanning workflows within the Hybrid AI Router Vision pipeline.

## 1. The Core Constraint
- **Rule**: NEVER pass a raw `.csv` or raw `.xlsx` file directly into an LLM context window.
- **Why**: Raw CSVs contain massive amounts of noisy tokens (commas, empty strings, repetitive structural elements). Passing them directly to an LLM causes severe token inflation, hallucinations (where the LLM loses track of column indices), and immediate context window exhaustion, violating the Context Compaction rule.

## 2. Mandatory Abstraction Layers
- Before any LLM operation is performed on tabular or document data, the file **MUST** be processed locally using a structured parsing package.
- **For Tabular Data (CSV/XLSX)**: Use `markitdown` (via `MarkItDown().convert()`) or `pandas` to structure the grid. If an LLM needs to understand the table, pass it the clean Markdown output from `markitdown` or a highly truncated JSON sample of the headers—never the raw comma-separated text.
- **For Unstructured Documents (PDF/Images)**: Use `docling` (via `DocumentConverter`) or the established Vision Cascade to extract bounding boxes and structured JSON representation.

## 3. Implementation of the Shadow Copy / Silver Layer
When building "Shadow Copies" or extracting data to a Silver Layer, do not rely on an LLM to parse the entire grid. Instead:
1. Use `markitdown` or `docling` to extract the document content.
2. If schema mapping is needed, pass *only* the Markdown headers to the LLM to identify the column positions (Schema-on-Read).
3. Perform the actual data extraction, mathematical validations (e.g., `qty * rate`), and anomaly flagging deterministically in Python.
