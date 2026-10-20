---
name: astro-science
description: Project map of the astro-science research workspace — paths, research projects, scripts, data, and graph config. Use whenever working inside /home/dawe/Projects/astro-science.
---

# astro-science project

Workspace root: `/home/dawe/Projects/astro-science`. Venv: `.venv` (Python 3.14).
Start with `CONTEXT.md` at the root — it is the authoritative index.

## Research projects

| Project | Path | Role |
|---|---|---|
| exotic-compact-objects | `research/projects/exotic-compact-objects/` | flagship (separate git repo, remote `Dawe583/exotic-compact-objects`) |
| black-holes | `research/projects/black-holes/` | GWOSC/GWTC snapshot |
| black-holes-wormholes | `research/projects/black-holes-wormholes/` | BH/WH fundamentals |

Always `cd` into the target project before running its scripts, and use the absolute
venv python: `/home/dawe/Projects/astro-science/.venv/bin/python`.

## Key script groups (exotic-compact-objects)

- **Download**: `scripts/download_gwosc.py`, `download_heasarc.py`, `download_sxs.py`,
  `download_eht.py`, `download_planck.py`, `download_sdss.py`, `download_gaia_dr3.py`,
  `download_blackcat.py`, `download_gwb.py`, `download_strain_marquee.py`,
  `download_xray_binaries.py`, `download_gwosc_o4.py`
- **Process**: `scripts/build_theoretical_data.py`, `process_blackcat.py`,
  `add_bh_derived_quantities.py`
- **Dashboards**: `scripts/build_gwtc_remnant_dashboard.py`,
  `build_agn_reverberation_dashboard.py`, `build_blackcat_dashboard.py`
- **Validation**: `scripts/verify_formulas.py`, `compute_with_data.py`
- **Generators**: `scripts/make_notebook*.py`, `make_premium_figures.py`,
  `create_animations.py`

## Data layout (exotic-compact-objects)

- `data/raw/` — GWOSC SQLite snapshot, SXS waveforms (`.npz`)
- `data/external/` — HEASARC, BlackCAT TSVs, EHT, Planck, SDSS, Gaia CSVs
- `data/processed/` — derived CSVs (`gwtc_recent_20_remnants.csv`,
  `agn_reverberation_masses.csv`, `blackcat_dynamical.csv`, ...)
- `models/` — `equations.py`, `formulas.py`, `derivations.py`
- `premium/` — theory markdown + HTML site
- `reports/` — `gwosc_latest.md`, `compute_data_report.md`, `derivations_report.md`

## Workspace-level data

- `data/` — sample data + `download_sample_data.py`, `download_direct_data.py`
- `catalogs/`, `cmb/`, `fits/`, `simulations/` — sample FITS artifacts
- `research/scripts/check_environment.py` — environment sanity check

## Graphs (Understand-Anything)

Data dir: `.ua/` (English output, set in `.ua/config.json`). See the `astro-graphs`
skill for the exact commands and the three graphs.

## Conventions (enforced)

- All outputs in **English**.
- State units; use `astropy.units`.
- Record assumptions + data source for every result.
- Catalog values: report with confidence intervals; do not treat as population-unbiased.
- Label model-derived quantities (e.g. Hawking temperature) as derived.
- Scripts must be re-runnable; record environment versions.
