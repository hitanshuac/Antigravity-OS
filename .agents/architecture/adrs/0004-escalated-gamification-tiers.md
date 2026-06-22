# ADR 0004: Escalated Gamification Tiers

## Context
The user requested that the gamification tier thresholds be escalated by factors of 10 to heighten the dramatic effect. The new tiers are:
- `> 9,000`: Tier 1 Visual Asset
- `> 90,000`: Yeti ("It's over 90000!")
- `> 900,000`: Tier 3 Visual Asset

## Decision
1. **Threshold Scaling**: We updated the trigger conditionals in `app.py` to match `9,000`, `90,000`, and `900,000` respectively.
2. **UI Slider Limits**: The previous maximum slider inputs theoretically capped out at ~98,000 kg/year. To make Godzilla mathematically reachable, the max values for `miles_driven` and `steaks_eaten` were increased to industrial-scale limits (e.g., 50,000 miles and 5,000 steaks).
3. **Gauge Dynamic Scaling**: The Plotly gauge chart was updated to dynamically scale its maximum bound based on the current carbon output, rather than using a hardcoded `15,000`.
4. **Prompt Tuning**: The `get_yeti_advice` system prompts were tuned to mention the specific new magnitudes.

## Consequences
- Users can now input exaggerated, fictional data to experience all gamification tiers.
- The Yeti Tracker now effectively acts as both a realistic personal tracker at low numbers and a ridiculous "industrial pollution" simulator at high numbers.
