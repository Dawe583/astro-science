# Astrofyzikální Výzkumné Prostředí - Kompletní Setup Guide (v2)

## 🚀 Quick Start

### Aktivace Virtuálního Prostředí
```bash
cd /home/dawe/Projects/astro-science
source .venv/bin/activate
```

### Spuštění Jupyter Lab
```bash
jupyter lab
```

---

## 📦 Nainstalované Nástroje

### Python Balíčky (v .venv)

#### Základní Scientific Stack
- **numpy** - Numerické výpočty, lineární algebra
- **scipy** - Scientific computing, speciální funkce
- **sympy** - Symbolická matematika
- **pandas** - Data analysis
- **matplotlib** - Základní vizualizace
- **seaborn** - Statistické grafy

#### Vizualizace
- **bokeh** - Interaktivní web vizualizace
- **holoviews** - High-level vizualizace
- **datashader** - Vizualizace velkých datasetů
- **plotly** - Interaktivní grafy
- **altair** - Declarativní vizualizace
- **mayavi** - 3D scientific vizualizace
- **pyvista** - 3D mesh vizualizace
- **scikit-image** - Image processing
- **scikit-video** - Video processing
- **pythreejs** - 3D web vizualizace v prohlížeči
- **ipyvolume** - 3D volumetric data v Jupyter
- **k3d** - 3D interaktivní grafy
- **trame** - Python framework pro interaktivní 3D

### Kosmologie
- **camb** - Code for Anisotropies in the Microwave Background
  - CMB power spectra
  - Lensing
  - Matter power spectra
- **classy** - Cosmic Linear Anisotropy Solving System
  - CMB a large-scale structure
  - Relativistic corrections

### CMB a Spherical Harmonics
- **healpy** - Hierarchical Equal Area isoLatitude Pixelation
  - CMB mapy
  - Spherical harmonics
- **shtools** - Spherical Harmonic Tools
  - Wavelet transforms
  - Power spectrum analysis

### Statistical Inference
- **emcee** - MCMC sampler
- **corner** - Corner plots pro parameter estimation
- **dynesty** - Dynamic Nested Sampling
- **zeus** - GPU-accelerated MCMC
- **bilby** - Gravitational wave parameter estimation
- **pymc** - Probabilistic Programming in Python
- **arviz** - Exploratory analysis of Bayesian models

### High-Energy Astrophysics
- **stingray** - X-ray timing a spectral analysis
- **gammapy** - Gamma-ray astronomy analysis
  - Fermi-LAT data
  - Cherenkov telescopes

### Gravitational Waves
- **bilby** - Gravitational wave inference framework
  - Bayesian parameter estimation
  - Signal analysis

### Atomic Simulation
- **ase** - Atomic Simulation Environment
  - DFT calculators (VASP, Quantum ESPRESSO, atd.)
  - Structure manipulation
- **pymatgen** - Materials analysis
  - Crystallography
  - Phase diagrams

### Plasma Physics
- **pysat** - Python Satellite Analysis Toolkit
  - Space physics data
  - Ionosphere, magnetosphere
- **plasmapy** - Plasma physics in Python
  - Data analysis
  - Fitting tools

### Space Physics a Ephemerides
- **spiceypy** - NASA SPICE Toolkit Python wrapper
  - Planetary ephemerides
  - Spacecraft trajectory data
  - NASA mission data

### Geospatial Analysis
- **geopandas** - Spatial data manipulation
- **pydeck** - Large-scale geospatial vizualizace
- **k3d** - 3D geospatial vizualizace

#### Astrofyzika
- **astropy** - Hlavní knihovna pro astronomii
  - Souřadnice, jednotky, čas, konstanty
  - FITS soubory, WCS
  - Kosmologické výpočty
- **astroquery** - Přístup k online databázím (SIMBAD, Gaia, SDSS)
- **astroML** - Machine learning pro astronomii
- **photutils** - Fotometrie a detekce zdrojů
- **astroplan** - Plánování pozorování
- **specutils** - Analýza spekter
- **reproject** - Reprojekce obrázků

#### Simulace
- **rebound** - N-body gravitační simulace
- **gala** - Galaktická dynamika
- **yt** - Kosmologické simulace a vizualizace

#### Kvantová Fyzika
- **qutip** - Quantum Toolbox in Python

---

### Desktop Software

#### Planetarium
- **Stellarium** (AppImage)
  - Umístění: `~/tools/Stellarium-26.3-qt5-x86_64.AppImage`
  - Spuštění: `~/tools/Stellarium-26.3-qt5-x86_64.AppImage`
  - 600,000+ hvězd, realistické noční oblohy

- **Celestia** (AUR - vyžaduje sudo)
  - Install: `yay -S celestia` (vyžaduje sudo)
  - 3D space simulation

#### Image Viewers
- **DS9/SAOImageDS9**
  - Umístění: `~/.local/bin/ds9`
  - Spuštění: `ds9`
  - FITS viewer, region manipulation, SAMP

#### Symbolic Computation
- **Maxima** (vyžaduje sudo)
  - Install: `yay -S maxima` (vyžaduje sudo)
  - Computer algebra system

- **SageMath** (volitelné, vyžaduje větší instalaci)
  - Doporučeno: použít Docker nebo web verzi

#### Julia
- **Julia 1.11.2**
  - Umístění: `~/tools/julia-1.11.2/`
  - Spuštění: `julia` (v PATH přes symlink)
  - Balíčky nainstalujte přes Julia REPL: `using Pkg; Pkg.add("Package")`

---

## 📚 Jupyter Notebooks

Klonované repozitáře s tutoriály:

1. **astro-Jupyter** - Undergraduate astrophysics dema
   - `./notebooks/`
   - Témata: radiation, gravity, relativity, N-body

2. **mast_notebooks** - NASA MAST tutorials
   - `./mast_notebooks/`
   - JWST, TESS, Hubble data

3. **gaia-jupyter-notebooks** - ESA Gaia tutorials
   - `./gaia-jupyter-notebooks/`
   - Gaia data access a analýza

4. **AstroInteractives** - Interactive astronomy demos
   - `./AstroInteractives/`
   - Exoplanet systems, Doppler shift, atd.

---

## 🔍 Přístup k Astronomickým Databázím

### Astroquery Examples

```python
from astroquery.simbad import Simbad
from astroquery.gaia import Gaia
from astroquery.sdss import SDSS

# SIMBAD
result_table = Simbad.query_object('M31')

# Gaia
Gaia.login()
Gaia.launch_job("SELECT TOP 10 * FROM gaiadr2.gaia_source")
r = Gaia.load_results()

# SDSS
from astroquery.sdss import SDSS
pos = coords.SkyCoord('0h8m05.63s +14d50m23.3s', frame='icrs')
xid = SDSS.query_xid(pos, spectro=True)
```

### Online Databáze (bez stahování)

- **SIMBAD**: https://simbad.harvard.edu/ - Astronomical object database
- **Gaia Archive**: https://gea.esac.esa.int/archive/ - 1.46B hvězd
- **SDSS SkyServer**: https://skyserver.sdss.org/ - Spectroscopic survey
- **NASA Eyes**: https://science.nasa.gov/eyes/ - Web-based 3D visualization
- **VizieR**: https://vizier.cds.unistra.fr/ - Astronomical catalogues
- **HEASARC**: https://heasarc.gsfc.nasa.gov/ - High-energy data

---

## 🎯 Příklady Použití

### 1. N-body Simulace s REBOUND
```python
import rebound
sim = rebound.Simulation()
sim.add(m=1.)  # Central star
sim.add(m=1e-3, a=1., e=0.1)  # Jupiter-like planet
sim.integrate(100.)
for p in sim.particles:
    print(p.x, p.y, p.z)
```

### 2. Galaktická Dynamika s Gala
```python
import gala.potential as gp
import gala.dynamics as gd
mw = gp.MilkyWay2022()
w0 = gd.PhaseSpacePosition(pos=[8, 0, 0], vel=[0, 220, 0])
orbit = mw.integrate_orbit(w0, dt=1, t1=0, t2=1000)
orbit.plot()
```

### 3. Kvantová Simulace s QuTiP
```python
from qutip import *
H = sigmaz()  # Hamiltonian
psi0 = basis(2, 0)  # Initial state
times = np.linspace(0, 10, 100)
result = mesolve(H, psi0, times, [sigmaz()])
result.plot()
```

### 4. Astrofyzikální Data s Astropy
```python
from astropy.coordinates import SkyCoord
from astropy import units as u
c = SkyCoord(ra=10.684*u.deg, dec=41.269*u.deg, frame='icrs')
print(c.galactic)  # Convert to galactic coordinates
```

---

## 🛠️ Konfigurace

### PATH Setup
Do `~/.bashrc` nebo `~/.zshrc` přidejte:
```bash
export PATH="$HOME/.local/bin:$PATH"
export PATH="$HOME/tools/julia-1.11.2/bin:$PATH"
```

### Julia Physics Packages
V Julia REPL:
```julia
using Pkg
Pkg.add("Unitful")
Pkg.add("PhysicalConstants")
Pkg.add("DifferentialEquations")
Pkg.add("QuantumOptics")
```

---

## 📊 Správa Dat

### Data Directory
- Umístění: `/home/dawe/Projects/astro-science/data/`
- Použijte pro vlastní datasets

### Stahování Datasets
Většina dat se stahuje dynamicky přes astroquery. Pro lokální data:
```python
from astroML.datasets import fetch_...
```

---

## 🌐 NASA Eyes (Web-based)

Bez instalace - použijte prohlížeč:
- URL: https://science.nasa.gov/eyes/
- Eyes on the Solar System
- Eyes on Exoplanets
- Eyes on Asteroids

---

## ⚠️ Poznámky

### Vyžadující Sudo
Následující nástroje vyžadují sudo/yay:
- **Celestia**: `yay -S celestia`
- **Maxima**: `yay -S maxima`
- **SageMath**: `yay -S sagemath` (velký balíček)

Tyto nainstalujte manuálně podle potřeby.

### Performance Tips
- Pro velké simulace použijte REBOUND v C verzi
- Pro 3D vizualizaci použijte Mayavi nebo PyVista
- Pro kosmologické simulace použijte yt

---

## 📖 Další Zdroje

### Dokumentace
- Astropy: https://docs.astropy.org/
- REBOUND: https://rebound.hanno-rein.de/
- Gala: https://gala.adrian.pw/
- yt: https://yt-project.org/
- QuTiP: https://qutip.org/
- Julia Physics: https://juliaphysics.github.io/

### Kurzy
- Python for Astronomers: https://prappleizer.github.io/
- AstroML: https://www.astroml.org/
- Gaia Tutorials: https://github.com/esa/gaia-jupyter-notebooks

---

## 🎉 Jste připraveni!

Všechny nástroje jsou připraveny k použití. Začněte s:
```bash
cd /home/dawe/Projects/astro-science
source .venv/bin/activate
jupyter lab
```

A prozkoumejte notebooks v `./notebooks/`, `./mast_notebooks/`, atd.
