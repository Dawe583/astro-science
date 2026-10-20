# astro-science Automation

The workspace is automated through four layers: **skills** (knowledge), **agents**
(roles), **loops** (recurring work), and **graphs** (context). This file is the
operator's manual. Start from `CONTEXT.md` for project context.

---

## 1. Skills

Skills are instruction sets the agent loads on demand.

### Global base — `~/.agents/skills/` (reusable across astro projects)

| Skill | Use when |
|---|---|
| `astro-research` | Starting any astro research task — method, units, catalog caveats |
| `astro-data-refresh` | Refreshing datasets / catalogs |
| `astro-notebook-health` | Validating the notebook suite |
| `astro-theory` | Doing derivations or writing theory |

### Project override — `astro-science/.opencode/skill/`

| Skill | Use when |
|---|---|
| `astro-science` | Working inside this workspace — paths, scripts, data layout |
| `astro-loops` | Starting, scheduling, or debugging a loop |
| `astro-graphs` | Running / refreshing the knowledge graphs |

---

## 2. Agents

Four specialized agents in `astro-science/.opencode/agent/`. Dispatch them by name.

| Agent | Role | Typical trigger |
|---|---|---|
| `astro-data-engineer` | Downloads/processes data, rebuilds dashboards | `/astro-refresh-data` |
| `astro-theoretician` | Derives equations, writes theory docs | `/astro-research` |
| `astro-validator` | Runs notebooks, checks formulas/units | `/astro-notebook-health` |
| `astro-reviewer` | Reviews reports for soundness/reproducibility | review step |

Each agent has explicit **gates** it must never skip (see its file).

---

## 3. Loops

Scripts in `astro-science/.opencode/loops/`. Self-contained, log to `logs/`, exit
non-zero on failure.

| Loop | Script | Purpose |
|---|---|---|
| Data refresh | `refresh-data.sh` | Download → process → rebuild dashboards/figures |
| Notebook health | `notebook-health.sh` | Execute every notebook → collect failures |
| Research | `research-loop.sh "<topic>"` | Set up a research work dir + hypothesis template |
| Graph refresh | `refresh-graphs.sh` | Deterministic drift check vs committed graphs → `.ua/refresh-requested.json` |
| Orchestrator | `orchestrator.sh` | Data → notebooks → graph drift; writes `logs/latest-status.json` |

The notebook-health loop writes `.opencode/loops/logs/notebook-health-latest.json`
and exits non-zero when any notebook fails.

The graph-refresh loop is the bridge between automation and the graphs: it never calls
an LLM, it only enumerates what changed (root SHA-256 fingerprints + subdomain file
list) and queues the exact `/understand` work. The orchestrator's
`latest-status.json` exposes `graphRefreshRequested` so an agent session can pick the
work up without re-scanning the tree itself.

### Trigger matrix

| Mode | How |
|---|---|
| Manual (research) | `/astro-research`, `/astro-refresh-data`, `/astro-notebook-health` |
| Shell | `.opencode/loops/<loop>.sh` |
| Scheduled | crontab (see below) |
| Agent heartbeat | RLM heartbeat prompts the session to run a loop (see `rlm-heartbeat` skill) |

### Scheduling examples

```cron
# refresh data weekly (Sundays 03:00)
0 3 * * 0 cd /home/dawe/Projects/astro-science && .opencode/loops/refresh-data.sh

# notebook health nightly
30 1 * * * cd /home/dawe/Projects/astro-science && .opencode/loops/notebook-health.sh

# graph drift nightly (after notebooks)
15 2 * * * cd /home/dawe/Projects/astro-science && .opencode/loops/refresh-graphs.sh
```

Inside an agent session, create a recurring heartbeat:

```python
await rlm_heartbeat.create("run the notebook health loop and report failures",
                           interval="6h", label="notebook-health")
```

---

## 4. Graphs

Three Understand-Anything graphs provide machine-readable context over the workspace.
See `GRAPHS.md` for the architecture and refresh procedure, `astro-graphs` skill for
the workflow, and `.ua/refresh-requested.json` for the current drift queue.

---

## 5. Commands

| Command | Agent | Effect |
|---|---|---|
| `/astro-refresh-data` | astro-data-engineer | Run the data refresh loop |
| `/astro-notebook-health` | astro-validator | Run the notebook health loop |
| `/astro-research` | astro-theoretician | Run the theory workflow |
| `/astro-graphs` | — | Build / refresh the knowledge graphs |
| `/astro-refresh-graphs` | — | Drift check → incremental graph refresh → re-apply cohesion |

---

## 6. End-to-end workflows

### A. Refresh the data and rebuild everything

```
/astro-refresh-data      # data engineer: download → process → dashboards
/astro-notebook-health   # validator: re-execute notebooks
/astro-graphs            # refresh the graphs
```

### B. Advance a research thread

```
/astro-research          # theoretician: question → derivation → figure → theory doc
# then: astro-reviewer audits the report
```

### C. Full autonomous sweep

```
.opencode/loops/orchestrator.sh
```

---

## 7. Rules of the road

- Always `cd /home/dawe/Projects/astro-science` first.
- Use the venv python: `/home/dawe/Projects/astro-science/.venv/bin/python`.
- A loop must never silently fail.
- After data/notebook changes, refresh the graphs.
- No credentials in source, docs, or logs.
