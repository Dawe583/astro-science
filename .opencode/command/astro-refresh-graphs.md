---
description: Check graph drift, refresh the knowledge graphs, and re-apply cohesion
---

Refresh the astro-science knowledge graphs after code/doc changes.

1. Read the `astro-graphs` skill.
2. Detect drift (deterministic, no LLM):

   ```
   .opencode/loops/refresh-graphs.sh
   ```

   If `.ua/refresh-requested.json` exists, it lists the exact added/changed/removed
   files — use it as the work list.

3. Rebuild what drifted:

   ```
   /understand                      # root code graph (incremental)
   ```

   If the request lists subdomain files, rebuild the subdomain graph from
   `research/projects/exotic-compact-objects` and merge:

   ```
   python3 ~/.agents/skills/understand/merge-subdomain-graphs.py
   ```

4. Re-apply cohesion edges (idempotent) and update the counts in `docs/GRAPHS.md`:

   ```
   .venv/bin/python .ua/tools/add-cohesion-edges.py
   ```

5. Refresh the derived graphs when content changed:

   ```
   /understand-domain
   /understand-knowledge research/wiki
   ```

Data dir: `.ua/` (English). `wiki-graph.json` is deliberately not named
`*knowledge-graph*` so the subdomain merge glob cannot ingest it.
