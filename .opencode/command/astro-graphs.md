---
description: Run/refresh the astro-science knowledge graphs
---

Run and refresh the three Understand-Anything knowledge graphs for astro-science.

1. Read the `astro-graphs` skill.
2. Full build (first time):

   ```
   /understand --language en
   /understand-domain
   /understand-knowledge research/wiki
   ```

3. Later updates are incremental by default — just re-run `/understand`.
4. Explore with `/understand-dashboard`.

Data dir: `.ua/` (English). Keep the graph fresh after any data or notebook change.
