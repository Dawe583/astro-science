# astro-science — GitHub ecosystem

Curated GitHub repositories that power this workspace. Star counts were pulled from the
GitHub REST search API on **2026-10-20** and are approximate. Installation status is
read from `.venv/bin/pip list` and the system PATH.

> Honest finding: astro-specific repositories almost never exceed 4k stars. Only two do.
> The tools that actually make astrophysics work possible are the scientific Python stack
> (Tier 3), which is all ≥4k. Tier 2 is therefore included despite being below 4k —
> otherwise the list would be useless for this work.

---

## Tier 1 — astrophysics-specific, ≥4k stars

| Repo | Stars | What it is | Fit for astro-science |
|---|---|---|---|
| [astropy/astropy](https://github.com/astropy/astropy) | ~5.4k | Units, coordinates, FITS/WCS I/O, constants, modeling, timeseries | **Core.** Used in every notebook (installed 8.0.2) |
| [Stellarium/stellarium](https://github.com/Stellarium/stellarium) | ~10.1k | Real-time OpenGL sky rendering (desktop planetarium) | Visualization/education only; already installed as AppImage |

## Tier 2 — astrophysics-specific essentials (<4k, direct fit)

| Repo | Stars | What it is | Installed? |
|---|---|---|---|
| [einsteinpy/einsteinpy](https://github.com/einsteinpy/einsteinpy) | ~705 | Geodesics, metrics, Christoffel, symbolic GR | yes 0.4.0 |
| [gwpy/gwpy](https://github.com/gwpy/gwpy) | ~383 | GW strain, Timeseries, spectrograms, frame data (upstream on GitLab) | yes 4.1.0 |
| [gwastro/pycbc](https://github.com/gwastro/pycbc) | ~392 | Matched filtering, signal detection, parameter estimation | no |
| [bilby-dev/bilby](https://github.com/bilby-dev/bilby) | ~129 | Bayesian GW inference; wraps dynesty/ultranest/emcee | yes 2.8.2 |
| [OpenSpace/OpenSpace](https://github.com/OpenSpace/OpenSpace) | ~1.3k | Astrovisualization (C++/WebGL), interactive tours | no |
| [sunpy/sunpy](https://github.com/sunpy/sunpy) | ~1.0k | Solar physics: images, time series, coordinates, maps | yes 8.0.1 |
| [poliastro/poliastro](https://github.com/poliastro/poliastro) | ~1.0k | Astrodynamics, orbits, maneuvers, interplanetary | no |
| [astropy/astroquery](https://github.com/astropy/astroquery) | ~798 | Catalog/MAST/HEASARC/SIMBAD/Vizier programmatic access | yes 0.4.11 |
| [dfm/corner.py](https://github.com/dfm/corner.py) | ~576 | Posterior corner plots for MCMC | yes 2.3.0 |
| [yt-project/yt](https://github.com/yt-project/yt) | ~559 | Volumetric data analysis (cosmology, grids, particles) | yes 4.4.3 |
| [lightkurve/lightkurve](https://github.com/lightkurve/lightkurve) | ~544 | Kepler/TESS time-series photometry | no |
| [dfm/emcee](https://github.com/dfm/emcee) | ~1.6k | Affine-invariant ensemble MCMC | yes 3.1.6 |
| [joshspeagle/dynesty](https://github.com/joshspeagle/dynesty) | ~426 | Dynamic nested sampling (Bayesian posteriors + evidences) | yes 3.1.0 |
| [gammapy/gammapy](https://github.com/gammapy/gammapy) | ~292 | Gamma-ray astronomy | yes 2.1 |
| [healpy/healpy](https://github.com/healpy/healpy) | ~323 | HEALPix spherical maps (CMB, all-sky) | yes 1.20.1 |
| [cmbant/CAMB](https://github.com/cmbant/CAMB) | ~261 | Boltzmann code: CMB power spectra, cosmology | yes 2.0.5 |
| [jobovy/galpy](https://github.com/jobovy/galpy) | ~285 | Galactic dynamics: potentials, orbits, action-angle | no |
| [pynbody/pynbody](https://github.com/pynbody/pynbody) | ~193 | N-body / SPH analysis for simulations | no |
| [exoplanet-dev/exoplanet](https://github.com/exoplanet-dev/exoplanet) | ~241 | Exoplanet transit/radial-velocity MCMC | no |
| [astropy/reproject](https://github.com/astropy/reproject) | ~128 | Astronomical image reprojection across WCS | no |

## Tier 3 — scientific stack ≥4k (this is what the loops and notebooks run on)

| Repo | Stars | Role in this workspace | Installed? |
|---|---|---|---|
| [scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn) | ~67.8k | ML used in `18_ml_astronomy`, outlier detection on catalogs | yes 1.9.1 |
| [numpy/numpy](https://github.com/numpy/numpy) | ~33.1k | Array core of every script | yes 2.5.4 |
| [scipy/scipy](https://github.com/scipy/scipy) | ~15.1k | ODE/optimisation/special functions (geodesics, fits) | yes 1.18.1 |
| [matplotlib/matplotlib](https://github.com/matplotlib/matplotlib) | ~23.4k | Every figure and dashboard | yes 3.11.2 |
| [pandas-dev/pandas](https://github.com/pandas-dev/pandas) | ~50.2k | Catalog dataframes, CSV/SQLite joins | yes 3.0.6 |
| [sympy/sympy](https://github.com/sympy/sympy) | ~15.0k | Symbolic derivations (Christoffel, geodesic equations) | yes 1.14.0 |
| [jupyterlab/jupyterlab](https://github.com/jupyterlab/jupyterlab) | ~15.3k | Notebook authoring environment | yes 4.6.4 |
| [pymc-devs/pymc](https://github.com/pymc-devs/pymc) | ~9.8k | Bayesian modelling; natural next step for GWTC population fits | yes 6.3.2 |
| [plotly/plotly.py](https://github.com/plotly/plotly.py) | ~18.8k | Interactive premium figures | yes 7.1.0 |
| [mwaskom/seaborn](https://github.com/mwaskom/seaborn) | ~14.1k | Statistical figures on catalog samples | yes 0.13.2 |
| [holoviz/panel](https://github.com/holoviz/panel) | ~5.8k | Dashboard apps; alternative to the premium HTML site | yes 1.9.4 |
| [numba/numba](https://github.com/numba/numba) | ~11.2k | JIT for the N-body/rebound analyses | yes 0.68.0 |
| [dask/dask](https://github.com/dask/dask) | ~13.9k | Parallel over large catalogs/FITS | yes 2026.8.0 |
| [jax-ml/jax](https://github.com/jax-ml/jax) | ~36.5k | Differentiable physics, fast autodiff integrators | no |
| [typst/typst](https://github.com/typst/typst) | ~56.7k | Fast typesetting for theory/reports | no (binary) |
| [jgm/pandoc](https://github.com/jgm/pandoc) | ~46.7k | Markdown ↔ PDF/HTML conversions | no (binary) |
| [quarto-dev/quarto-cli](https://github.com/quarto-dev/quarto-cli) | ~6.1k | Reproducible scientific publishing (notebooks → PDF) | no (binary) |
| [streamlit/streamlit](https://github.com/streamlit/streamlit) | ~46.1k | Rapid dashboards over catalogs | no |
| [iterative/dvc](https://github.com/iterative/dvc) | ~15.9k | Version data + pipeline stages | no |
| [mlflow/mlflow](https://github.com/mlflow/mlflow) | ~28.5k | Experiment/run tracking for the research loops | no |
| [treeverse/lakeFS](https://github.com/treeverse/lakeFS) | ~4.6k | Versioned data lake for large catalogs | no |

---

## What is already installed (verified)

`astropy`, `astroquery`, `bilby`, `camb`, `corner`, `dask`, `dynesty`, `emcee`,
`gammapy`, `gwpy`, `healpy`, `h5py`, `holoviews`, `jupyterlab`, `matplotlib`, `nbconvert`,
`numba`, `numpy`, `pandas`, `panel`, `plotly`, `pymc`, `rebound`, `scikit-learn`, `scipy`,
`seaborn`, `sunpy`, `sympy`, `xarray`, `yt`, `zarr`. System: `julia`, `maxima`, `ds9`,
`Stellarium` (AppImage).

## Recommended next moves for astro-science

1. **GW inference chain** — `gwpy` + `PyCBC` + `bilby` + `corner`/`emcee`/`dynesty`/`pymc`
   are the natural stack for the GWTC remnant thread. Only PyCBC is missing.
2. **Bayesian population fits** — `pymc` is installed; pair it with `corner` for posterior
   corner plots of remnant masses/spins.
3. **CMB / cosmology** — `camb` + `healpy` cover power spectra and all-sky maps; `healpy`
   is installed, CAMB 2.0.5 is installed.
4. **Reproducible publishing** — add `quarto` (notebooks → PDF reports) and `typst`
   (theory documents) instead of hand-editing HTML.
5. **Dashboards** — `panel` (installed) or `streamlit` can host the catalog dashboards the
   premium site currently generates as static HTML.
6. **Large-data workflows** — `dask` (installed) + `xarray`/`zarr`/`h5py` for tiled catalogs
   and FITS mosaics.
