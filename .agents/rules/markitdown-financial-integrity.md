# Financial Data Integrity

This rule defines strict standards for data extracted via MarkItDown or any other ingestion pipeline regarding financial figures.

## 1. Zero-Mutation Policy on Financial Data
- **Rule**: You MUST NEVER modify, forward-fill (ffill), back-fill, impute, or attempt to "correct" financial columns, specifically `RATE` and `AMOUNT`.
- **Why**: Financial data must perfectly reflect the raw invoice. Altering this data—even to fix an obvious formatting mistake made by a vendor—introduces untraceable accounting discrepancies and breaks data lineage.
- **Action**:
  - Extract the raw string/float values exactly as they appear in the markdown or tabular source.
  - If a vendor leaves a `RATE` blank but fills an `AMOUNT`, leave the `RATE` blank.
  - Do not calculate missing values (e.g. `QTY * RATE = AMOUNT`). The missing value must remain `null` or `NaN`.

## 2. No Synthetic Data Generation
- **Rule**: When providing snippets or previews of data extractions, agents MUST ONLY show the exact data present in the file. Synthetic data (hallucinations) to "fill out" a table preview is strictly forbidden.

## 3. Exception Handling
- If a value cannot be safely cast to its required schema type (e.g., parsing a string "N/A" as a float), the pipeline MUST raise a `SchemaError` and halt, rather than silently replacing it with `0` or `0.0` (as per `defensive-programming.md`).
