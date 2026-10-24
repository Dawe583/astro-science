---
title: Data Provenance
date: 2026-10-24
tags:
  - data
  - provenance
  - reproducibility
---

# Data Provenance — astro-science

> Scientific-integrity note: **no generated/synthetic data may be presented as a real
> measurement.** Every dataset below is classified as **REAL** (live measurement /
> published catalog), **DERIVED** (computed from real data or theory), or
> **SYNTHETIC (test)** (generated for pipeline validation only).

## REAL — live data / published catalogs (downloaded, not generated)

| Dataset | Source | Script | Notes |
|---|---|---|---|
| GWTC events (391) | GWOSC eventapi | `download_gwosc.py`, `update_gwosc.py` | Real GW events, refreshed 2026-10-24 |
| HEASARC catalogs (xrbcat, ulxrbcat, m87cxo, sgraregcsc, …) | HEASARC TAP | `download_heasarc.py` | Real X-ray binary / source catalogs (SSL cert issue as of 2026-10-24; cached CSVs from earlier successful run are real) |
| BlackCAT (tables A1–A4) | VizieR J/A+A/587/A61 | `download_blackcat.py` | Real dynamical BH measurements |
| SDSS DR17/DR18 quasars | SDSS SkyServer | `download_sdss.py` | Real spectra/photometry |
| Gaia DR3 (BH candidates) | Gaia archive | `download_gaia_dr3.py` | Real astrometry |
| Planck PR4 (CMB spectra/maps) | PLA | `download_planck.py` | Real CMB (some fallbacks if PLA unreachable) |
| Strain HDF5 (GW170817, GW190814, GW190521) | GWOSC 4 kHz R1 | `download_strain_marquee.py` | Real strain time series |
| GWB (NANOGrav/EPTA/PPTA/IPTA) | Published 15-yr results | `download_gwb.py` | Published (not re-downloaded) amplitudes/indices |
| EHT (M87*, Sgr A*) | EHT public archive (GitHub eventhorizontelescope/2019-D01-01) | `download_eht.py` | **REAL** — 8 calibrated M87* CSVs (no registration needed) + metadata |

## DERIVED — computed from real data or theory (labeled as derived)

| Dataset | Script | Notes |
|---|---|---|
| `blackcat_dynamical.csv` | `process_blackcat.py` | Derived quantities from real BlackCAT |
| `gwtc_recent_20_remnants.csv` | `add_bh_derived_quantities.py` | Derived (ISCO, Hawking T, …) — label as derived |
| `agn_reverberation_masses.csv` | `add_bh_derived_quantities.py` | Derived |
| Theoretical grids | `build_theoretical_data.py` | Model grids — label as model-derived |
| Dashboards/figures | `build_*_dashboard.py`, `make_premium_figures.py` | Visualizations of real/derived data |

## SYNTHETIC (test) — generated, NOT measurements

These exist for pipeline validation only and **must not** be cited as measurements:

| Dataset | Script | Status |
|---|---|---|
| SXS BBH waveforms (240 npz) | `download_sxs.py` (`generate_synthetic_waveforms`) | **SYNTHETIC** — `sxs_waveform_analysis.md` caveats updated |
| SXS BBH waveforms (real subset, 5 sims) | `download_sxs.py` (sxs package) | **REAL** — real NR simulations via sxs package (metadata in `data/external/sxs_catalog/`) |
| EHT visibility data | `download_eht.py` (`generate_synthetic_visibilities`) | **REAL** — now uses public calibrated CSVs from GitHub (no synthetic generation) |
| MAXI/Swift-BAT/NICER/XRB synthetic catalogs | `download_xray_binaries.py` | **SYNTHETIC** — marked in premium site (badge "synthetic (test)") |
| Sample FITS galaxy / CMB map | `data/download_direct_data.py`, `data/download_sample_data.py` | **SYNTHETIC** — tutorials only |

## Real-data replacement plan

- **SXS:** use the `sxs` Python package to fetch real NR waveforms (Zenodo) instead of synthetic; update `download_sxs.py`.
- **EHT:** public calibrated data now downloaded via `download_eht.py` (no registration needed). ✅ Done.
- **X-ray binaries:** rely on the real HEASARC catalogs (`download_heasarc.py`: xrbcat, ulxrbcat, …); deprecate synthetic catalogs in `download_xray_binaries.py`.
- **Sample data:** keep synthetic (clearly labeled) for tutorials; never use in research outputs.

## Convention

Per `CONTEXT.md` §11: catalog values reported with confidence intervals; model-derived
quantities (e.g. Hawking temperature) labeled as derived; never treat synthetic data
as a population-unbiased sample.
EOF
echo "written"