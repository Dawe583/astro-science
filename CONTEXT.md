# astro-science — Master Context

> **Single source of truth** for the astro-science research workspace.
> All outputs and documentation are in **English**.
> Last updated: 2026-10-20

This file is the entry point for every future session. Read it first, then use the
project skill `astro-science` for path-level detail and the loop skill `astro-loops`
for automation.

---

## 1. What this workspace is

A **scientific research workspace** (not a web app) for astrophysics, focused on:

- **Exotic compact objects** — black holes, wormholes, white holes
- **Gravitational waves** — GWTC/GWOSC catalogs, strain analysis
- **Quantum gravity** — Planck-scale derivations, effective field theory
- **Observational catalogs** — AGN masses, BlackCAT X-ray binaries, Gaia BH candidates

The workspace produces a **portfolio**, not a single product:

| Product | Location |
|---|---|
| Theory documents | `research/projects/*/premium/theory_*.md`, `research/wiki/` |
| Interactive notebooks | `research/projects/*/notebooks/*.ipynb` |
| Dashboards / figures | `research/projects/*/premium/figures/`, `figures/` |
| Catalogs / data products | `research/projects/*/data/processed/` |
| Published site | `research/projects/exotic-compact-objects/premium/` → `docs/` (GitHub Pages) |

---

## 2. Repository & environment

| Item | Value |
|---|---|
| Root | `/home/dawe/Projects/astro-science` |
| Git | initialized (first commit `3bd44d2`), `.gitignore` excludes `.venv`, caches, foreign clones, large binaries |
| Python | `.venv` — **Python 3.14** (`source .venv/bin/activate`) |
| Node | v24.21.0, pnpm 12.11.2 (used by Understand-Anything) |
| Disk | `.venv` ~4.8 GB, `research` ~3.2 GB |

**Important:** `research/projects/exotic-compact-objects/` is a **separate git repo**
(remote `github.com/Dawe583/exotic-compact-objects.git`). It is excluded from the root
repo (it manages its own history) but **is** analyzed by the knowledge graph.

---

## 3. Directory map

```
astro-science/
├── .opencode/                 # OpenCode project config (skills, agents, commands, loops)
├── .ua/                       # Understand-Anything data dir (code graph)
├── research/
│   ├── wiki/                  # Karpathy-pattern knowledge wiki (source of the wiki graph)
│   ├── projects/
│   │   ├── exotic-compact-objects/   # flagship project (separate git repo)
│   │   ├── black-holes/              # GWOSC/GWTC snapshot project
│   │   └── black-holes-wormholes/    # BH/WH fundamentals notebooks
│   ├── notes/                 # research notes
│   └── scripts/               # workspace-level scripts
├── data/                      # small sample data + download scripts
├── simulations/               # sample FITS outputs
├── cmb/                       # sample CMB maps
├── fits/                      # sample galaxy FITS
├── catalogs/                  # sample star/galaxy catalogs
├── notebooks/                 # CLONED upstream tutorials (excluded from graph)
├── mast_notebooks/            # CLONED upstream tutorials (excluded from graph)
├── gaia-jupyter-notebooks/    # CLONED upstream tutorials (excluded from graph)
├── AstroInteractives/         # CLONED upstream tutorials (excluded from graph)
├── CONTEXT.md                 # this file
├── README.md                  # environment/tool inventory
├── SETUP_GUIDE.md, TOOLS_LIST.md, ...
└── start.sh, start-research.sh, check-environment.sh
```

---

## 4. Research projects

### 4.1 `exotic-compact-objects` (flagship)

The main active project. 23 notebooks, ~30 scripts, theory docs, generated English research site.

- **Models** (`models/`): `equations.py`, `formulas.py`, `derivations.py`
- **Notebooks** (`notebooks/`): `01_...` through `24_quantum_gravity.ipynb`
- **Theory** (`premium/*.md`): `theory_black_holes`, `theory_wormholes`,
  `theory_white_holes`, `theory_kerr_newman`, `theory_kerr_newman_adm`,
  `theory_reissner_nordstrom`, `theory_geodesic_equations`, `theory_christoffel_kerr`,
  `theory_raychaudhuri`, `theory_fisher_matrix`, `theory_bh_perturbation`,
  `early_smbh_growth`, `quantum_gravity`
- **Data**:
  - `data/raw/` — GWOSC SQLite snapshot, SXS waveforms (`*.npz`)
  - `data/external/` — HEASARC catalogs, BlackCAT TSVs, EHT, Planck, SDSS, Gaia
  - `data/processed/` — derived CSVs (`gwtc_recent_20_remnants.csv`,
    `agn_reverberation_masses.csv`, `blackcat_dynamical.csv`, ...)
- **Reports** (`reports/`): `gwosc_latest.md`, `compute_data_report.md`,
  `derivations_report.md`, `summary.md`, `remnant_energetics.md`
- **Research site** (`premium/` → `docs/`): generated English static site (dark observatory
  design, dashboard, catalogue tables, model gallery, interactive Plotly figures, auto TOC).
  Build + publish: `$PY scripts/build_premium_site.py --publish`.

**Key rebuild commands** (from the project dir, with the workspace venv):

```bash
cd /home/dawe/Projects/astro-science/research/projects/exotic-compact-objects
PY=/home/dawe/Projects/astro-science/.venv/bin/python
$PY scripts/download_gwosc.py          # refresh GWOSC snapshot
$PY scripts/download_heasarc.py        # refresh HEASARC catalogs
$PY scripts/build_theoretical_data.py  # rebuild derived grids
$PY scripts/build_gwtc_remnant_dashboard.py
$PY scripts/build_agn_reverberation_dashboard.py
$PY scripts/build_blackcat_dashboard.py
$PY scripts/process_blackcat.py
$PY scripts/add_bh_derived_quantities.py
$PY scripts/verify_formulas.py
```

### 4.2 `black-holes`

GWOSC/GWTC catalog snapshot project.

- **Scripts**: `scripts/update_gwosc.py`, `scripts/update_heasarc_candidates.py`
- **Data**: `data/black_holes.sqlite` (catalog snapshot + `fetch_log`)
- **Figures**: `figures/gwtc_total_mass.png`, `figures/gwtc_snr.png`
- **Reports**: `reports/latest.md`

**Refresh:**

```bash
cd /home/dawe/Projects/astro-science
.venv/bin/python research/projects/black-holes/scripts/update_gwosc.py
```

> Note: the script replaces the catalog table with a snapshot. Back up the DB first if
> you need historical versions.

### 4.3 `black-holes-wormholes`

Pedagogical BH/WH fundamentals notebooks (`notebooks/01_black_hole_fundamentals.ipynb`,
`02_geodesics_orbits.ipynb`). Contains a large `GW150914_28.zip` (~438 MB, gitignored).

### 4.4 `exoplanets`

Exoplanet demographics, detection, and habitability project (NEW — previously undocumented).

- **Models** (`models/`): `equations.py` (escape velocity, equilibrium temperature, Jeans parameter, atmospheric mass loss)
- **Scripts** (`scripts/`): `download_exoplanets.py`, `process_exoplanets.py`
- **Notebooks** (`notebooks/`): `01_exoplanet_catalog.ipynb`
- **Theory** (`premium/`): `theory_atmospheric_escape.md`, `theory_demographics.md`,
  `theory_detection_methods.md`, `theory_habitability.md`, `theory_orbital_dynamics.md`
- **Reports** (`reports/`): `demographics.md`

**Status:** catch-up required (Phase C of `docs/ROADMAP.md`) — needs more notebooks,
formula verification, and integration into the premium site.

---

## 5. Data sources

| Source | Access | Script |
|---|---|---|
| GWOSC / GWTC | REST API (public) | `download_gwosc.py`, `update_gwosc.py` |
| HEASARC (XRB, ULX, M87, Sgr A*) | TAP / CSV | `download_heasarc.py`, `update_heasarc_candidates.py` |
| SXS waveforms | Zenodo/SXS | `download_sxs.py` |
| EHT (M87, Sgr A*) | archive | `download_eht.py` |
| Planck | archive | `download_planck.py` |
| SDSS | SkyServer | `download_sdss.py` |
| Gaia DR3 | archive | `download_gaia_dr3.py` |
| BlackCAT | VizieR TSV | `download_blackcat.py` + `process_blackcat.py` |
| GWB / strain | GWOSC | `download_gwb.py`, `download_strain_marquee.py` |
| X-ray binaries | HEASARC | `download_xray_binaries.py` |

Local sample data: `data/`, `catalogs/`, `cmb/`, `fits/`, `simulations/`
(downloaded by `data/download_sample_data.py`, `data/download_direct_data.py`).

---

## 6. Knowledge graphs (Understand-Anything)

Understand-Anything is installed globally (`~/.understand-anything/repo`, skills linked to
`~/.agents/skills`). The plugin is built (`packages/core/dist`).

**Data directory:** `.ua/` in the project root. `.gitignore` keeps `.ua/` except
`intermediate/`, `tmp/`, `.trash-*`, `diff-overlay.json`, and the plugin-generated
`.ua/.understandignore`.

**Three graphs are maintained (all committed):**

| Graph | Command | Output | Size (2026-10-20 build) |
|---|---|---|---|
| Code graph (root + subdomain merge) | `/understand` | `.ua/knowledge-graph.json` | 184 nodes / 233 edges / 10 layers / 18 tour steps |
| Domain flows | `/understand-domain` | `.ua/domain-graph.json` | 58 nodes (4 domains, 10 flows, 44 steps) / 59 edges |
| Knowledge wiki graph | `/understand-knowledge research/wiki` | `.ua/wiki-graph.json` | 82 nodes (17 articles, 7 topics, 24 entities, 34 claims) / 176 edges |

Transient merge inputs (recreated on refresh, safe to restage):

- `.ua/exotic-compact-objects-knowledge-graph.json` — subdomain code graph for the
  nested repo (92 nodes / 62 edges), merged into the root graph via
  `merge-subdomain-graphs.py` (report: `.ua/merge-report.json`).
- `.ua/wiki-graph.json` is deliberately **not** named `*knowledge-graph*` so the
  subdomain-merge glob cannot ingest it as a code subdomain.

- Output language: **English** (stored in `.ua/config.json`).
- Incremental updates are the default (only changed files re-analyzed).
- `.understandignore` excludes `.venv`, caches, cloned upstream repos, and large binaries.
  The nested `exotic-compact-objects` repo **is** analyzed (via its code, not its data).
- See the project skill `astro-graphs` for exact commands.

---

### 6.5 Companion tools

- **graphify** (installed via `uv tool`, v0.9.95): builds a queryable knowledge graph
  of the whole workspace. Outputs in `graphify-out/`: `graph.html`, `GRAPH_REPORT.md`,
  `graph.json`, `obsidian/` (1569 notes + `graph.canvas`), `manifest.json`.
  Re-run: `graphify .` (full) or `graphify . --update` (incremental).
- **Obsidian vault**: the project root is an Obsidian vault (`.obsidian/` gitignored).
  Entry point: `Home.md` (MOC). The graphify export is also openable as its own vault
  (`graphify-out/obsidian/`). Obsidian app: `~/Applications/Obsidian-1.14.5.AppImage`.
- **obsidian-skills**: installed at `~/.opencode/skills/obsidian-skills` (6 skills).

---

## 7. Skills

**Global base** (`~/.agents/skills/`) — reusable across astro projects:

- `astro-research` — master research method, conventions, data-source rules
- `astro-data-refresh` — the data-refresh loop
- `astro-notebook-health` — the notebook health loop
- `astro-theory` — the theory/derivation loop

**Project override** (`astro-science/.opencode/skill/`):

- `astro-science` — this workspace's paths, projects, scripts, graph config
- `astro-loops` — how the five loops run here and how to trigger them
- `astro-graphs` — how to run/refresh the three graphs

---

## 8. Agents

Four specialized agents live in `astro-science/.opencode/agent/`:

| Agent | Role |
|---|---|
| `astro-data-engineer` | Downloads/processes data, rebuilds dashboards, writes catalogs |
| `astro-theoretician` | Derives equations, writes theory docs, validates physics |
| `astro-validator` | Runs notebooks, checks formulas/units, audits results |
| `astro-reviewer` | Reviews reports for scientific soundness and reproducibility |

---

## 9. Loops & workflows

Five loops, orchestrated by `.opencode/loops/orchestrator.sh`:

| Loop | Script | Purpose |
|---|---|---|
| Data refresh | `refresh-data.sh` | Download → process → rebuild dashboards/figures |
| Notebook health | `notebook-health.sh` | Execute all notebooks → fix → report |
| Publish site | `publish-site.sh` | Rebuild the research site + sync `docs/` for GitHub Pages |
| Research | `research-loop.sh` | Hypothesis → derivation → figure → report → theory doc |
| Graph refresh | `refresh-graphs.sh` | Drift check vs committed graphs → `.ua/refresh-requested.json` |

The orchestrator runs data → notebooks → site → graph drift and writes
`.opencode/loops/logs/latest-status.json`; the graph loop never calls an LLM — it
queues exact `/understand` work. Trigger modes: OpenCode commands (`/astro-*`) for
manual runs; the scripts are cron/heartbeat-ready for autonomous runs. See `astro-loops`.

---

## 10. Commands

Project commands in `astro-science/.opencode/command/`:

- `/astro-refresh-data` — run the data refresh loop
- `/astro-notebook-health` — run the notebook health loop
- `/astro-research` — run the research loop
- `/astro-graphs` — run/refresh the knowledge graphs
- `/astro-refresh-graphs` — drift check → refresh → re-apply cohesion edges

---

## 11. Conventions

- **Language:** English for all outputs, docs, and graph content.
- **Units:** always state units; use `astropy.units`. Assume nothing silently.
- **Assumptions:** every result must record assumptions and data source.
- **Reproducibility:** scripts must be re-runnable; record environment versions.
- **Catalog values:** report catalog measurements with confidence intervals; never
  treat catalog events as population-unbiased samples unless corrected.
- **Derived quantities:** label model-derived values (e.g. Hawking temperature) as such.
- **No credentials** in source, docs, or logs.
- **Git:** never force-push shared history; use revert commits.

---

## 12. Quick start

```bash
cd /home/dawe/Projects/astro-science
source .venv/bin/activate

# 1. Refresh data
.opencode/loops/refresh-data.sh

# 2. Check notebooks
.opencode/loops/notebook-health.sh

# 3. Rebuild + publish the research site
.opencode/loops/publish-site.sh

# 4. Detect graph drift (then /understand if requested)
.opencode/loops/refresh-graphs.sh

# 5. Explore the graph
/understand-dashboard
```

To continue a specific thread, read the relevant project report under
`research/projects/*/reports/` and the matching theory doc under
`research/projects/*/premium/`.
