# Workflow: Generate All Diagrams

**Trigger:** Invoked by `master-sync.md` Phase 4, or manually via `/ask run @[.agents/workflows/generate-diagrams.md]`

## Objective
A generalized, universal pipeline to scan the project for any programmatic diagram definitions (D2 or Python), compile them into structured images, and autonomously apply the Strict AI Styling Pass to guarantee aesthetic quality without spelling hallucinations.

## Execution Steps

### Phase 0: Codebase Extraction (Auto-Sync)
1. Execute `python scripts/diagram_extractor.py` to parse the `src/` directory.
2. Ensure the script successfully outputs `docs/assets/auto_architecture.d2`.

### Phase 1: Diagram Discovery
1. Scan the `docs/` folder (and any subfolders) for all `.d2` and `.py` diagram definition files.
2. For each identified diagram file, extract the base `<diagram_name>` (e.g., `handover_flow.d2` -> `handover_flow`).

### Phase 2: Generate Technical Diagrams
1. Iterate through the discovered `.d2` files. Run `d2 docs/<diagram_name>.d2 docs/assets/<diagram_name>_technical.png --theme=200 --sketch`.
2. Iterate through any discovered `.py` diagram files. Run `python docs/<diagram_name>.py` (Output must be configured to generate `docs/assets/<diagram_name>_technical.png`).
3. Verify that all base `<diagram_name>_technical.png` files exist and are non-zero bytes.

### Phase 3: The Showcase Styling Pass (Dual-Audience Rule)
1. Per the `.agents/skills/diagram-generator/SKILL.md` rules, iterate through the list of generated `_technical.png` files.
2. For each diagram, read its `.d2` or `.py` source to extract every node label, cluster name, and edge label.
3. Call `generate_image` with **two images in `ImagePaths`**:
   - `docs/assets/<diagram_name>_technical.png` (structural content base)
   - `docs/assets/handover_flow.png` (canonical aesthetic style reference)
4. Use the exact prompt template from `SKILL.md`, **explicitly listing every label** extracted in step 2.
5. Save the AI-styled output as `docs/assets/<diagram_name>_showcase.png`.

### Phase 4: Verification & Update
1. Ensure `README.md` correctly references both the `_showcase` and `_technical` versions of core architecture diagrams where applicable.
2. Report the generation of the dual diagram sets to the user.

### Phase 5: Lossless Compression (WebP)
1. You MUST execute a Python snippet using the `Pillow` library to convert all newly generated `docs/assets/*.png` files into lossless `.webp` format.
2. You MUST delete the original `.png` files after successful conversion.
3. You MUST update `README.md` and any other references to point to the `.webp` files instead of `.png`.
