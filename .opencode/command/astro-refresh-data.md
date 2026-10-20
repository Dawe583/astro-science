---
description: Run the astro-science data refresh loop
agent: astro-data-engineer
---

Run the data refresh loop for the astro-science workspace.

1. Read `CONTEXT.md` and the `astro-science` skill for the exact script paths.
2. Execute `.opencode/loops/refresh-data.sh` from the project root, or run the
   download/process/dashboard scripts directly with the venv python.
3. Report what changed (counts, new events, deltas) and confirm no silent failures.
4. After the refresh, re-run the knowledge graphs (see `/astro-graphs`).

Do not fabricate data. If a source is unavailable, record the skip.
