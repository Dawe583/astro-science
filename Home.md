---
title: Astro-Science Workspace
date: 2026-10-24
tags:
  - moc
  - index
  - astro-science
aliases:
  - Home
  - Index
  - Dashboard
---

# Astro-Science Workspace

Map of content for the [[CONTEXT|Master Context]]. This folder is an **Obsidian vault** (root = project root).

## Projects

- [[research/projects/exotic-compact-objects/README|exotic-compact-objects]] — flagship (BH/WH/white holes, GW, QG)
- [[research/projects/black-holes/README|black-holes]] — GWOSC/GWTC snapshot
- [[research/projects/black-holes-wormholes/README|black-holes-wormholes]] — BH/WH fundamentals
- [[research/projects/exoplanets/README|exoplanets]] — NEW (undocumented in CONTEXT; see [[ROADMAP]])

## Knowledge Graphs (Understand-Anything)

- Code graph: `.ua/knowledge-graph.json` (184 nodes) — view via `/understand-dashboard`
- Domain flows: `.ua/domain-graph.json`
- Wiki graph: `.ua/wiki-graph.json`
- Wiki articles: `research/wiki/` (22 notes)

## Knowledge Graph (graphify)

- Interactive: `graphify-out/graph.html` (1295 nodes / 1717 edges / 274 communities)
- Report: `graphify-out/GRAPH_REPORT.md`
- Obsidian export: `graphify-out/obsidian/` (1569 notes + `graph.canvas`) — open as its own vault

## Plans & Docs

- [[docs/ROADMAP]] — detailed development plan
- [[CONTEXT]] — master context
- [[README]] — environment & tool inventory
- [[docs/GRAPHS]] — graph workflow
- [[docs/AUTOMATION]] — loops & automation

## Conventions

- All outputs in **English**; state units (`astropy.units`); record assumptions + data source.
- Catalog values: report with confidence intervals.
- Derived quantities (e.g. Hawking temperature) labelled as derived.

## Quick Start

```bash
cd /home/dawe/Projects/astro-science
source .venv/bin/activate
.opencode/loops/refresh-graphs.sh
```

See [[docs/AUTOMATION]] for the five loops.
