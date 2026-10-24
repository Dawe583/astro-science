# Goal

**Objective:** Complete the astro-science research workspace autonomously — refresh all
knowledge graphs, keep every dataset traceable to real measurements (no synthetic
data presented as real), keep all notebooks green, keep the premium site published,
and keep documentation (CONTEXT.md, ROADMAP.md, DATA_PROVENANCE.md) current.

**Status:** In progress. Phases A (mostly), B (data refresh, notebooks, formulas),
D (site publish) done. Phase C (exoplanets) partially. Phase E (Obsidian) deferred
per user. Phase F (research loop) ongoing. Phase G (automation) partially.

**Remaining:**
- Understand-Anything graph refresh (`/understand` incremental/full) for 2 stale premium docs.
- Real SXS/EHT data replacement (requires registration).
- Exoplanets formula verification expansion + site integration.
- (Obsidian removed from scope per user decision 2026-10-24.)

**Autonomous operation (configured 2026-10-24):**
- systemd user timers: `astro-graph-refresh.timer` (every 30 min), `astro-orchestrator.timer` (daily).
- Understand-Anything `autoUpdate: true` in `.ua/config.json` (graph refresh on commit).
- Linger not enabled (no sudo); timers run while user is logged in.
- rlm-heartbeat/goal APIs require the active Python kernel; set via harness when available.