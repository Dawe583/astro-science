---
description: Run the astro-science notebook health loop
agent: astro-validator
---

Run the notebook health loop for the astro-science workspace.

1. Read the `astro-notebook-health` skill.
2. Execute `.opencode/loops/notebook-health.sh` from the project root.
3. For every failure, find the root cause and fix it — never skip silently.
4. Re-run to confirm, then report pass/fail/skip counts and the fixes applied.

A notebook that errors is a failure, not a skip. Do not hand-edit notebook outputs.
