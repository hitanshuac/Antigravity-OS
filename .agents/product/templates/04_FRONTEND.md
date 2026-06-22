# Frontend Architecture & Design

## 1. UX/UI Principles
- **Framework**: Streamlit is used to rapidly construct the UI and bind state natively to Python execution without React/Node boilerplate.
- **Color Palette**: Dark mode by default (`#0e1117`).
- **Gamified Metaphors**: Visceral impact is prioritized over dry statistics. The UI visually degrades when absurd footprint thresholds are crossed.

## 2. Layout Structure
A 2-column layout (`col1`, `col2`) to separate the Data Visualization (Left) from the Data Ingestion (Right).

### Right Column: The Ingestion & Verification
1. **The Continuous Confessional**: A `st.text_area` for natural language input. A primary button ("Extract Data") triggers the LLM. It appends the Yeti Advisor's responses directly into the text area to form a continuous conversational log.
2. **Human Verification Sliders**: Five standard `st.slider` components mapped to Streamlit Session State (Car KM, Flight KM, Transit KM, AC Hours, Restaurant Meals). The math engine listens to these, not the LLM.

### Left Column: The Dashboard / Gamification
1. **State 1 (Human)**: Displays Plotly gauges showing Yearly Carbon and the Monthly Carbon Tax mapped to an INR scale.
2. **State 2 (Category 1 Warning)**: Triggers at > 9,000kg.
3. **State 3 (Category 2 & 3 Catastrophe)**: Triggers at > 15,000kg and > 30,000kg. Displays massive red HTML headers, visual overrides (`tier3.jpg`, `tier2.jpg`), and aggressive roasts.
4. **The Yeti Advisor**: A secondary button at the bottom triggering the LLM roasting function `get_yeti_advice` and appending the dynamic mitigation strategies to the confessional.
