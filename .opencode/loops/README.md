# astro-science loops

Automation loops for the workspace. All scripts are self-contained, log to
`logs/`, and exit non-zero on failure.

| Script | Loop | Purpose |
|---|---|---|
| `refresh-data.sh` | Data refresh | Download → process → rebuild dashboards/figures |
| `notebook-health.sh` | Notebook health | Execute every notebook → collect failures, write `logs/notebook-health-latest.json` |
| `research-loop.sh "<topic>"` | Research | Set up a research work dir + hypothesis template |
| `refresh-graphs.sh` | Graph refresh | Detect code/doc drift vs the committed graphs, write `.ua/refresh-requested.json` |
| `orchestrator.sh` | All | Runs data → notebooks → graph drift, writes `logs/latest-status.json` |

## Run manually

```bash
cd /home/dawe/Projects/astro-science
.opencode/loops/refresh-data.sh
.opencode/loops/notebook-health.sh
.opencode/loops/research-loop.sh "ISCO radius vs spin"
.opencode/loops/refresh-graphs.sh
.opencode/loops/orchestrator.sh
```

Or via OpenCode commands: `/astro-refresh-data`, `/astro-notebook-health`,
`/astro-research`, `/astro-graphs`, `/astro-refresh-graphs`.

## Loop ↔ graph contract

`refresh-graphs.sh` never calls the LLM. It compares the working tree against
`fingerprints.json` (root, SHA-256 of UTF-8 content) and the subdomain graph's file
list, then drops a precise work list into `.ua/refresh-requested.json`. The next agent
session executes `/understand` (+ subdomain merge), re-runs
`.ua/tools/add-cohesion-edges.py`, and clears the request. The orchestrator records
the state in `logs/latest-status.json` (`graphRefreshRequested: true|false`).

## Schedule autonomously

The scripts are cron/heartbeat-ready. Example crontab:

```cron
0 3 * * 0 cd /home/dawe/Projects/astro-science && .opencode/loops/refresh-data.sh
30 1 * * * cd /home/dawe/Projects/astro-science && .opencode/loops/notebook-health.sh
15 2 * * * cd /home/dawe/Projects/astro-science && .opencode/loops/refresh-graphs.sh
```

Inside an agent session, an RLM heartbeat (see the `rlm-heartbeat` skill) can prompt
the session to run a loop on an interval.

## Environment

- Python: `/home/dawe/Projects/astro-science/.venv/bin/python`
- Logs: `.opencode/loops/logs/`
- Notebooks execute with a 900 s timeout (override with `NOTEBOOK_TIMEOUT`).
