---
name: Universal Ingestion (MarkItDown)
description: Implements Microsoft's markitdown library to flatten unstructured proprietary file formats into clean, LLM-digestible markdown streams.
---

# Universal Ingestion Skill

This skill documents the Standard Operating Procedure (SOP) for safely converting messy, unstructured, and proprietary files (PDF, DOCX, XLSX, CSV, PPTX) into a uniform Markdown format using Microsoft's `markitdown`.

## 1. Core Principles

- **Never pass raw proprietary files to an LLM.** Always flatten them into Markdown first.
- **Never pass massive files to an LLM.** To prevent `ContextWindowExceeded` and `RateLimitError` crashes, always truncate the output.
- **Always use secure temporary files.** Do not permanently save user uploads to the `/data` directory unless explicitly required by a stateful logging workflow.

## 2. Dependencies
Ensure `markitdown` and its dependencies are present in `requirements.txt`:
```text
markitdown
```

## 3. Implementation Blueprint

When an Agent needs to build a file uploader or ingestion pipeline, it MUST follow this Python implementation pattern:

### Step 1: Secure Temporary Storage
Use Python's `tempfile` module to temporarily hold the user's uploaded binary stream.

```python
import tempfile
import os
from markitdown import MarkItDown

# Assuming `uploaded_file` is a Streamlit or FastAPI UploadFile object
md = MarkItDown()
with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
    tmp.write(uploaded_file.getvalue()) # or .read()
    tmp_path = tmp.name
```

### Step 2: The Conversion
Pass the temporary file path to `MarkItDown`.

```python
try:
    result = md.convert(tmp_path)
    target_text = result.text_content
except Exception as e:
    # Always implement Defensive Programming Observability
    log_error_to_json(type(e).__name__, "markitdown", str(e))
    target_text = ""
finally:
    # Always cleanly delete the temporary file
    if os.path.exists(tmp_path):
        os.remove(tmp_path)
```

### Step 3: SRE Context Safeguard (Mandatory Truncation)
To protect the LLM (like Groq, OpenAI, or Gemini) from Out-of-Memory (OOM) failures or massive billing spikes, the markdown string MUST be truncated.

For Header Mapping & Structured Extraction:
```python
# Truncate to the first 25,000 characters
if len(target_text) > 25000:
    target_text = target_text[:25000]
```
*Rationale:* 25,000 characters is roughly 5,000 to 6,000 tokens, which safely fits inside Groq's 8,000-token context window limit.

## 4. Integration with Pydantic
Once the `target_text` is securely extracted and truncated, it can be seamlessly passed to the `parse_messy_text` LLM function to map the headers and extract the JSON schema validated by Pydantic.
