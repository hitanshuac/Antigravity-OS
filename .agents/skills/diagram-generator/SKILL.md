---
name: Diagram Generator Skill
description: Instructions for programmatically generating high-fidelity architecture diagrams using Diagrams-as-Code to minimize LLM token usage and prevent image gibberish.
---

# Diagram Generator Skill

When instructed to update or generate an architecture diagram (e.g., during the `publish-showcase.md` workflow), you must **NEVER** use an AI image generator (like DALL-E or Imagen). Instead, you must use **Diagrams-as-Code** to generate pixel-perfect PNGs.

## Supported Tools
The Base Agentic Environment supports two industry-standard tools. Choose the right tool based on the diagram's requirements:

### 1. Python `diagrams` (mingrammer)
**Best for:** Cloud architecture, specific technology nodes (AWS, GCP, Python, Databases), and SRE visual flow.
- **Dependency:** Ensure `diagrams` is in `requirements.txt`.
- **Execution:** Create a script (e.g., `docs/generate_architecture.py`), define the nodes, and run it via `python <script>.py`. Ensure `graph_attr` and `cluster_attr` enforce Dark Mode (`bgcolor="#0D1117"`).
- **Note:** Graphviz must be installed on the system path.

### 2. D2 (Declarative Diagramming)
**Best for:** Fast sketch-style diagrams, generic software flowcharts, UML replacements, and abstract component logic.
- **Dependency:** D2 binary is pre-installed via winget.
- **Execution:** Create a `.d2` text file (e.g., `docs/architecture.d2`) with D2 syntax (`A -> B: request`).
- **Render:** Run `d2 docs/architecture.d2 docs/assets/architecture_diagram.png --theme=200 --sketch` (Theme 200 is mandatory for dark mode).

## Workflow Execution
1. Read the `README.md` to understand the conceptual relationships.
2. Select the appropriate tool.
3. Generate the code (Python or D2).

### The Strict AI Styling Pass (Dual-Audience Rule)
Because raw programmatic diagrams lack visual flair, you MUST apply a stylistic pass using the `generate_image` tool for recruiter-facing or showcase assets.

**CRITICAL RULES:**
1. **NEVER ask the AI to "redraw" a diagram loosely.** AI generators hallucinate spellings.
2. **ALWAYS pass `docs/assets/handover_flow.png` as a direct style reference image** via `ImagePaths` alongside the technical base. This is the canonical aesthetic standard.
3. **ALWAYS enumerate every node label explicitly in the prompt text.** Do not say "preserve the text." Instead, literally list every node name and connection label so the AI has zero ambiguity.

**Execution Steps:**
1. Generate the base programmatic diagram: `docs/assets/<diagram_name>_technical.png`.
2. Read the `.d2` or `.py` source file to extract the exact list of node labels, cluster names, and edge labels.
3. Call `generate_image` with **two images in `ImagePaths`**:
   - `docs/assets/<diagram_name>_technical.png` (structural base)
   - `docs/assets/handover_flow.png` (aesthetic style reference)
4. Use this **exact prompt template**, filling in the specific node/edge labels from step 2:
   ```
   Create a highly professional architecture diagram. Use the SECOND provided image
   (dark dashboard with glassmorphism nodes, neon cyan/purple accents) as the EXACT
   aesthetic style reference. Use the FIRST provided image as the structural content
   reference.

   The diagram must contain these exact nodes and connections:
   [LIST EVERY CLUSTER, NODE LABEL, AND EDGE LABEL HERE — SPELLED EXACTLY]

   Style: Dark navy background (#0D1117), glassmorphism node boxes with subtle glow,
   neon cyan and purple accent colors, clean enterprise dashboard aesthetic matching
   the second reference image exactly. Include watermark "github.com/hitanshuac".

   CRITICAL: Every word of text must be spelled EXACTLY as listed above.
   ```
5. Save the output as `docs/assets/<diagram_name>_showcase.png`.
6. Present `<diagram_name>_showcase.png` to recruiters. Keep `<diagram_name>_technical.png` for engineers.
