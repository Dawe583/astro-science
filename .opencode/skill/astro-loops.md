---
name: astro-loops
description: How the five automation loops (data refresh, notebook health, site publish, graph drift, research) run in astro-science and how to trigger them. Use to start, schedule, or debug a loop.
---

# astro-loops

Five loops orchestrate the workspace. All scripts live in
`/home/dawe/Projects/astro-science/.opencode/loops/`.

## The loops

| Loop | Script | What it does |
|---|---|---|
| Data refresh | `refresh-data.sh` | Downloads new data → processes → rebuilds dashboards/figures |
| Notebook health | `notebook-health.sh` | Executes every notebook → collects failures → writes a report |
| Publish site | `publish-site.sh` | Rebuilds the research site from catalogues and syncs `docs/` (GitHub Pages) |
| Graph drift | `refresh-graphs.sh` | Compares the tree with committed fingerprints → `.ua/refresh-requested.json` |
| Research | `research-loop.sh` | Hypothesis → derivation → figure → report → theory doc |

The graph loop never calls an LLM: it queues an exact work list for the next agent
session, which runs `/understand` and the subdomain merge (see `astro-graphs`).

## Trigger modes

**Manual (recommended for research):**

```bash
.opencode/loops/refresh-data.sh          # or: /astro-refresh-data
.opencode/loops/notebook-health.sh       # or: /astro-notebook-health
.opencode/loops/publish-site.sh          # no command wrapper; deterministic
.opencode/loops/research-loop.sh         # or: /astro-research
.opencode/loops/refresh-graphs.sh        # or: /astro-refresh-graphs
```

**Autonomous (cron / heartbeat):** the scripts are self-contained and log to
`.opencode/loops/logs/`. To run them on a schedule, add entries to crontab, e.g.:

```cron
# refresh data weekly (Sundays 03:00) — also publishes the site
0 3 * * 0 cd /home/dawe/Projects/astro-science && .opencode/loops/refresh-data.sh
# notebook health nightly
30 1 * * * cd /home/dawe/Projects/astro-science && .opencode/loops/notebook-health.sh
# graph drift hourly
15 2 * * * cd /home/dawe/Projects/astro-science && .opencode/loops/refresh-graphs.sh
```

Or, inside an agent session, use an RLM heartbeat (see the `rlm-heartbeat` skill) to
prompt the session to run a loop on an interval.

## Orchestrator

`.opencode/loops/orchestrator.sh` runs data → notebooks → site → graph drift in
sequence and writes `.opencode/loops/logs/orchestrator-<timestamp>.log` plus
`latest-status.json`. Use it for a full sweep; the status JSON is consumed by the
research workspace and by the `pipeline` panel of the AstronomicAL plugin.

## Rules

- Always run from the project root (`cd /home/dawe/Projects/astro-science`).
- Use the absolute venv python: `/home/dawe/Projects/astro-science/.venv/bin/python`.
- A loop must never silently fail: it writes a status line and exits non-zero on error.
- After any data refresh, re-run the graphs (see `astro-graphs`) so the graph stays fresh.
- Publish only from the build script (`build_premium_site.py --publish`); never hand-edit
  files under `docs/`.
