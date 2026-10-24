# Astrofyzikální Výzkumné Prostředí (v3 - Kompletní)

Kompletní sada nástrojů pro astrofyziku, teoretickou fyziku, matematiku, kvantovou fyziku a vědecký výzkum.

## 🔭 Research portfolio

The flagship research programme (black holes, wormholes, white holes, gravitational
waves) publishes a generated research site:

- **Portal / notebooks:** https://dawe583.github.io/exotic-compact-objects/
- **Research site:** https://dawe583.github.io/exotic-compact-objects/premium/
- Source and build script: `research/projects/exotic-compact-objects/` (`scripts/build_premium_site.py`)

The site is rebuilt deterministically by `.opencode/loops/publish-site.sh` and is part
of the orchestrator run, so catalogue counts and figures cannot go stale.

## 🕸️ Knowledge graphs & Obsidian vault

- **Understand-Anything** (3 graphs in `.ua/`): code graph, domain flows, knowledge wiki. Run `/understand-dashboard` to explore.
- **graphify** (v0.9.95): full-workspace knowledge graph — `graphify-out/graph.html` (1295 nodes), `GRAPH_REPORT.md`, and an Obsidian export in `graphify-out/obsidian/` (1569 notes). Re-run: `graphify .` (full) or `graphify . --update` (incremental).
- **Obsidian vault**: the project root is an Obsidian vault (`.obsidian/`); entry point `Home.md`. Obsidian app at `~/Applications/Obsidian-1.14.5.AppImage`.
- **obsidian-skills** installed at `~/.opencode/skills/obsidian-skills` (6 skills).

## 📋 Přehled

Toto prostředí obsahuje:
- **Python Scientific Stack** s kompletním astrofyzikálním ekosystémem
- **Simulační nástroje** pro N-body, galaktickou dynamiku, kosmologii
- **Kvantové simulace** (QuTiP, Qiskit, Cirq, PennyLane)
- **Desktop planetarium software** (Stellarium, Celestia)
- **Astronomical image viewers** (DS9)
- **Symbolic computation** (Maxima, Julia)
- **Kosmologické nástroje** (CAMB, CLASS)
- **Gravitational wave inference** (Bilby)
- **Plasma physics** (PlasmaPy, PySAT)
- **Quantum computing** (Qiskit, Cirq, PennyLane)
- **Machine learning** (XGBoost, LightGBM, CatBoost)
- **Solar physics** (SunPy)
- **Gravitational lensing** (Lenstronomy)
- **Jupyter notebooks** s tutoriály a příklady
- **Přístup k online astronomickým databázím** (SIMBAD, Gaia, SDSS)

---

## 🚀 Rychlý Start

```bash
cd /home/dawe/Projects/astro-science
source .venv/bin/activate
jupyter lab
```

---

## 📦 Nainstalované Komponenty

### 1. Python Balíčky (~25-30GB)

#### Základní Scientific Stack
- numpy, scipy, sympy, pandas
- matplotlib, seaborn, plotly
- jupyter, jupyterlab, ipython

#### Vizualizace
- bokeh, holoviews, datashader, altair
- mayavi, pyvista (3D)
- scikit-image, scikit-video
- pythreejs, ipyvolume, k3d (3D web)
- trame (interaktivní 3D framework)
- glueviz, glue-core (multi-dimensional data)

#### Astrofyzika (Astropy Ecosystem)
- **astropy** - Hlavní knihovna
  - astropy.coordinates - souřadnice
  - astropy.units - fyzikální jednotky
  - astropy.time - čas a datumy
  - astropy.constants - fyzikální konstanty
  - astropy.cosmology - kosmologie
  - astropy.io.fits - FITS soubory
  - astropy.wcs - World Coordinate System
- **astroquery** - Online databáze (SIMBAD, Gaia, SDSS)
- **astroML** - Machine learning pro astronomii
- **photutils** - Fotometrie a detekce zdrojů
- **astroplan** - Plánování pozorování
- **specutils** - Analýza spekter
- **reproject** - Reprojekce obrázků

#### Simulace
- **rebound** - N-body gravitační simulace
- **gala** - Galaktická dynamika
- **yt** - Kosmologické simulace

#### Kvantová Fyzika
- **qutip** - Quantum Toolbox in Python
- **qiskit** - IBM quantum computing framework
- **qiskit-aer** - Quantum circuit simulator
- **cirq** - Google quantum computing framework
- **pennylane** - Quantum machine learning

#### Kosmologie
- **camb** - CMB power spectra, lensing
- **classy** - CMB, large-scale structure

#### CMB a Spherical Harmonics
- **healpy** - CMB mapy, spherical harmonics
- **shtools** - Wavelet transforms, power spectra

#### Statistical Inference
- **emcee** - MCMC sampler
- **corner** - Corner plots
- **dynesty** - Nested sampling
- **zeus** - GPU-accelerated MCMC
- **bilby** - Gravitational wave inference
- **pymc** - Probabilistic programming
- **arviz** - Bayesian model analysis

#### High-Energy Astrophysics
- **stingray** - X-ray timing/spectral analysis
- **gammapy** - Gamma-ray astronomy, Fermi-LAT
- **sherpa** - X-ray spectral analysis (NASA/CXC)

#### Gravitational Waves
- **bilby** - Gravitational wave parameter estimation

#### Atomic Simulation
- **ase** - Atomic Simulation Environment, DFT calculators
- **pymatgen** - Materials analysis, crystallography
- **phonopy** - Phonon calculations, lattice dynamics

#### Plasma Physics
- **pysat** - Space physics data analysis
- **plasmapy** - Plasma physics tools

#### Space Physics/Ephemerides
- **spiceypy** - NASA SPICE Toolkit, planetary ephemerides

#### Geospatial
- **geopandas** - Spatial data
- **pydeck** - Geospatial visualization
- **k3d** - 3D geospatial viz

#### Physical Units
- **pint** - Physical units library
- **quantities** - Unit-aware arrays

#### Machine Learning
- **xgboost** - Gradient boosting
- **lightgbm** - Light gradient boosting
- **catboost** - Categorical boosting

#### Solar Physics
- **sunpy** - Solar data analysis, space weather

#### Image Alignment
- **astroalign** - Astronomical image alignment

#### Gravitational Lensing
- **lenstronomy** - Gravitational lensing modeling

#### Bioinformatics
- **biopython** - Bioinformatics tools

#### Simulation
- **simpy** - Discrete event simulation

#### Data Analysis
- scikit-learn, networkx, xarray
- numba, h5py, zarr
- fitsio - Fast FITS I/O

---

### 2. Desktop Software (~850MB)

#### Planetarium
- **Stellarium 26.3** (AppImage)
  - Umístění: `~/tools/Stellarium-26.3-qt5-x86_64.AppImage`
  - Spuštění: `~/tools/Stellarium-26.3-qt5-x86_64.AppImage`
  - 600,000+ hvězd, realistické oblohy

- **Celestia** (AUR - vyžaduje sudo)
  - Install: `yay -S celestia`
  - 3D space simulation napříč vesmírem

#### Image Viewers
- **DS9/SAOImageDS9 8.8**
  - Umístění: `~/.local/bin/ds9`
  - Spuštění: `ds9`
  - FITS viewer, region manipulation, SAMP

#### Symbolic Computation
- **Maxima** (vyžaduje sudo)
  - Install: `yay -S maxima`
  - Computer algebra system

- **Julia 1.11.2**
  - Umístění: `~/tools/julia-1.11.2/`
  - Spuštění: `julia`
  - High-performance scientific computing

---

### 3. Jupyter Notebooks Tutorials

Klonované repozitáře:
- **astro-Jupyter** - Undergraduate astrophysics dema
- **mast_notebooks** - NASA MAST (JWST, TESS, Hubble)
- **gaia-jupyter-notebooks** - ESA Gaia tutorials
- **AstroInteractives** - Interactive astronomy demos

---

### 4. Přístup k Databázím

#### Online Databáze (přes astroquery)
- **SIMBAD** - Astronomical object database
- **Gaia** - 1.46 miliardy hvězd
- **SDSS** - Spectroscopic survey
- **Chandra, XMM, Hubble** - NASA data archivy

#### Web-based Tools
- **NASA Eyes** - https://science.nasa.gov/eyes/
  - Eyes on the Solar System
  - Eyes on Exoplanets
  - Eyes on Asteroids

---

## 📖 Dokumentace

- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Detailní setup instrukce
- [TOOLS_LIST.md](TOOLS_LIST.md) - Kompletní seznam nástrojů
- [GITHUB_TOOLS.md](GITHUB_TOOLS.md) - Curated GitHub repos (astrophysics + scientific stack, ≥4k stars where possible)
- [NEW_TOOLS_SUMMARY.md](NEW_TOOLS_SUMMARY.md) - Nové nástroje v2/v3
- [INSTALLATION_SUMMARY.md](INSTALLATION_SUMMARY.md) - Instalační shrnutí

---

## 🎯 Příklady Použití

### Astrofyzikální Data
```python
from astropy.coordinates import SkyCoord
from astropy import units as u
from astroquery.simbad import Simbad

# Query SIMBAD
result = Simbad.query_object('M31')

# Souřadnice
c = SkyCoord(ra=10.684*u.deg, dec=41.269*u.deg)
print(c.galactic)
```

### N-body Simulace
```python
import rebound
sim = rebound.Simulation()
sim.add(m=1.)
sim.add(m=1e-3, a=1., e=0.1)
sim.integrate(100.)
```

### Kvantová Simulace
```python
from qutip import *
H = sigmaz()
psi0 = basis(2, 0)
result = mesolve(H, psi0, np.linspace(0, 10, 100), [sigmaz()])
```

### Kosmologie (CAMB)
```python
import camb
from camb import model, initialpower

# Nastavení kosmologických parametrů
pars = camb.CAMBparams()
pars.set_cosmology(H0=67.5, ombh2=0.022, omch2=0.122)
pars.InitPower.set_params(ns=0.965, As=2e-9)

# Výpočet CMB power spectra
results = camb.get_results(pars)
powers = results.get_cmb_power_spectra(pars, CMB_unit='muK')
```

### Gravitational Wave Inference (Bilby)
```python
import bilby

# Nastavení priorů
priors = bilby.gw.prior.BBHPriorDict()
priors['mass_1'] = bilby.prior.Uniform(5, 50, 'mass_1')
priors['mass_2'] = bilby.prior.Uniform(5, 50, 'mass_2')

# Spuštění sampleru
result = bilby.run_sampler(
    likelihood=likelihood,
    priors=priors,
    sampler='dynesty',
    nlive=1000
)
```

### Plasma Physics (PlasmaPy)
```python
from plasmapy.formulary import gyrofrequency, thermal_speed
from astropy import units as u

# Gyrofrekvence iontů
B = 1 * u.T
ion = 'H+'
omega_ci = gyrofrequency(B, ion)

# Termální rychlost
T = 1e6 * u.K
v_th = thermal_speed(T, particle='e-')
```

### Quantum Computing (Qiskit)
```python
from qiskit import QuantumCircuit, Aer, execute

# Vytvoření kvantového obvodu
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# Simulace
backend = Aer.get_backend('qasm_simulator')
result = execute(qc, backend, shots=1000).result()
counts = result.get_counts()
```

---

## ⚙️ Instalace Dodatečných Nástrojů (vyžaduje sudo)

```bash
# Celestia
yay -S celestia

# Maxima
yay -S maxima

# SageMath (volitelné, velký balíček)
yay -S sagemath
```

---

## 📊 Správa Projektu

### Struktura
```
astro-science/
├── .venv/                 # Python virtual environment
├── notebooks/             # astro-Jupyter tutoriály
├── mast_notebooks/        # NASA MAST tutoriály
├── gaia-jupyter-notebooks/# Gaia tutoriály
├── AstroInteractives/     # Interactive demos
├── data/                  # Adresář pro data
├── requirements.txt       # Python dependencies
├── SETUP_GUIDE.md        # Detailní setup
├── TOOLS_LIST.md         # Kompletní seznam
├── NEW_TOOLS_SUMMARY.md  # Nové nástroje v2/v3
├── INSTALLATION_SUMMARY.md # Instalační shrnutí
└── README.md             # Tento soubor
```

---

## 🔗 Užitečné Odkazy

### Dokumentace
- Astropy: https://docs.astropy.org/
- REBOUND: https://rebound.hanno-rein.de/
- Gala: https://gala.adrian.pw/
- yt: https://yt-project.org/
- QuTiP: https://qutip.org/
- Julia Physics: https://juliaphysics.github.io/
- Qiskit: https://qiskit.org/
- Cirq: https://quantumai.google/cirq
- PennyLane: https://pennylane.ai/

### Online Data
- SIMBAD: https://simbad.harvard.edu/
- Gaia Archive: https://gea.esac.esa.int/archive/
- SDSS: https://skyserver.sdss.org/
- NASA Eyes: https://science.nasa.gov/eyes/

---

## 💡 Tipy

1. Pro práci s velkými daty použijte `dask` a `datashader`
2. Pro 3D vizualizaci použijte `mayavi`, `pyvista` nebo `k3d`
3. Pro N-body simulace použijte `rebound`
4. Pro kosmologické simulace použijte `yt`
5. Pro kvantové simulace použijte `qutip` nebo `qiskit`
6. Pro symbolickou matematiku použijte `sympy` nebo `Maxima`
7. Pro ML na vědeckých datech použijte `xgboost`, `lightgbm`, `catboost`
8. Pro CMB analýzu použijte `healpy` a `camb`
9. Pro gravitational waves použijte `bilby`
10. Pro plasma physics použijte `plasmapy`

---

## 📊 Statistiky

**Celkové využití disku:**
- Python balíčky: ~25-30GB
- Desktop software: ~850MB
- Jupyter notebooks: ~500MB
- **Celkem:** ~27-32GB (z limitu 100GB)

**Celkem nainstalovaných Python balíčků:** 150+

**Kategorie nástrojů:** 25+

---

## 🎉 Jste připraveni!

Začněte s Jupyter Lab:
```bash
cd /home/dawe/Projects/astro-science
source .venv/bin/activate
jupyter lab
```

Prozkoumejte notebooks v repozitářích a začněte s výzkumem!
