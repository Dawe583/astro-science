# Astrofyzikální Vývojové Prostředí - Kompletní Seznam Nástrojů

## 📊 Shrnutí
- **Celková kapacita disku:** 884GB volného místa
- **Plánovaná instalace:** ~50-80GB (bez velkých datasetů)
- **Limit:** 100GB

---

## 1. Python Základní Balíčky (Core Scientific Stack)

### Numerické a Matematické Balíčky
- **numpy** - N-dimenzionální pole, lineární algebra, FFT
- **scipy** - Optimalizace, integrace, speciální funkce, statistika
- **sympy** - Symbolická matematika (algebra, kalkulus, diferenciální rovnice)
- **pandas** - Data analysis a manipulation
- **numba** - JIT kompilace pro rychlé výpočty

### Vizualizace
- **matplotlib** - Základní plotting, 2D/3D grafy
- **seaborn** - Statistické grafy, atraktivní styly
- **bokeh** - Interaktivní vizualizace v prohlížeči
- **holoviews** - High-level deklarativní vizualizace
- **datashader** - Vizualizace velkých datasetů
- **plotly** - Interaktivní grafy

### Jupyter a Development
- **jupyter** - Jupyter notebooks a lab
- **ipython** - Enhanced Python REPL
- **jupyterlab** - Moderní IDE pro Jupyter

---

## 2. Astropy Ecosystem (Astronomické Python Balíčky)

### Core Astropy
- **astropy** - Hlavní knihovna pro astronomii
  - astropy.coordinates - astronomické souřadnice
  - astropy.units - fyzikální jednotky
  - astropy.time - čas a datumy
  - astropy.constants - fyzikální konstanty
  - astropy.cosmology - kosmologické výpočty
  - astropy.table - datové tabulky
  - astropy.io.fits - FITS soubory
  - astropy.wcs - World Coordinate System
  - astropy.visualization - vizualizační nástroje

### Affiliated Packages
- **astroquery** - Přístup k online astronomickým databázím (SIMBAD, Gaia, SDSS, NASA)
- **photutils** - Detekce zdrojů a fotometrie
- **astroplan** - Plánování astronomických pozorování
- **specutils** - Analýza astronomických spekter
- **reproject** - Reprojekce astronomických obrázků
- **galpy** - Dynamika Galaxie
- **astroML** - Machine learning pro astronomii s datovými sety

---

## 3. Simulace a Dynamika

### N-body Simulace
- **rebound** - N-body integrátor pro gravitační simulace
  - Symplektické integrátory (WHFast, MERCURIUS)
  - Kolizní dynamika
  - Podpora planetárních systémů
  - 3D vizualizace

### Galaktická Dynamika
- **gala** - Galaktická a gravitační dynamika v Pythonu
  - Gravitační potenciály a síly
  - Integrace orbitů
  - Transformace souřadnic
  - Chaos indikátory

### Kosmologické Simulace
- **yt** - Analýza a vizualizace kosmologických simulací
  - Loading simulation data (Enzo, FLASH, Gadget, Arepo)
  - Slice, projection, volume rendering
  - Halo finding a analýza
  - Cosmology calculator
- **yt_astro_analysis** - Rozšíření pro astrofyzikální analýzu

---

## 4. Kvantová Fyzika a Teoretická Fyzika

### Kvantová Mechanika
- **qutip** - Quantum Toolbox in Python
  - Simulace kvantových systémů
  - Kvantová optika
  - Open quantum systems
  - Kvantové informační zpracování

### Další Kvantové Nástroje
- **quimb** - Tensor network methods
- **pennylane** - Quantum machine learning
- **cirq** - Quantum computing framework

### Condensed Matter
- **kwant** - Quantum transport
- **pybinding** - Tight-binding modely

---

## 5. Planetarium Software

### Desktop Planetarium
- **Stellarium** - Realistické planetarium pro počítač
  - 600,000+ hvězd v základním katalogu
  - 80,000+ deep-sky objektů
  - 3D sceneries
  - Telescope control
  - Větší katalogy (220M+ hvězd)

### 3D Space Simulation
- **Celestia** - Real-time 3D vizualizace vesmíru
  - 100,000+ hvězd
  - Galaxie, planety, měsíce, asteroidy
  - Seamless zoom napříč škálami
  - Expandable add-ons

### Web-based (No installation needed)
- **NASA Eyes** - NASA JPL vizualizační platforma
  - Eyes on the Solar System
  - Eyes on Exoplanets
  - Eyes on Asteroids
  - Real-time NASA mission tracking
  - URL: https://science.nasa.gov/eyes/

---

## 6. Astronomické Image Viewery

### FITS Viewers
- **DS9/SAOImageDS9** - Standardní FITS viewer
  - Podpora FITS obrázků a tabulek
  - Multiple frame buffers
  - Region manipulation
  - SAMP pro integraci s dalšími nástroji
  - Pokročilé scale algoritmy a colormaps

### Alternativy
- **FV** - FITS file browser/editor (součást HEASoft)
- **Aladin Desktop** - Interaktivní sky atlas

---

## 7. X-ray a High-Energy Astronomy

### HEASoft Suite
- **HEASoft** - Unified release pro high-energy astronomy
  - **FTOOLS** - Manipulace FITS souborů
  - **Xspec** - Spektrální analýza X-ray dat
  - **Xronos** - Timing analýza X-ray dat
  - **Ximage** - Imaging analýza X-ray dat
  - **Xselect** - Filtering event files
  - **XSTAR** - Photoionized gas calculations
  - **CFITSIO** - FITS I/O library
  - **HEASoftpy** - Python interface

### Podporované mise
- Chandra, XMM-Newton, Swift, NuSTAR, NICER, INTEGRAL, ROSAT, Suzaku

---

## 8. Symbolic Computation Systems

### SageMath
- **SageMath** - Open-source alternativa k Mathematica/Maple/MATLAB
  - Symbolická algebra
  - Kalkulus, diferenciální rovnice
  - Teorie čísel
  - Algebraická geometrie
  - Integrace s Pythonem

### Maxima
- **Maxima** - Computer algebra system (GPL)
  - Symbolická manipulace
  - Diferenciace, integrace
  - Taylor řady, Laplace transformace
  - Maticové operace
  - Plotting

---

## 9. Julia Programming Language

### Julia pro Physics
- **Julia** - High-performance programming language pro scientific computing
  - "As easy as Python, as fast as C/C++"
  - Native podpora pro paralelismus
  - GPU computing

### Physics Packages
- **Unitful.jl** - Physical quantities with units
- **UnitfulAstro.jl** - Astronomical units
- **PhysicalConstants.jl** - Fundamental constants
- **QuantumOptics.jl** - Quantum systems simulation
- **DifferentialEquations.jl** - ODE/PDE solvers
- **ModelingToolkit.jl** - Physical modeling
- **QuantumInformation.jl** - Quantum info theory
- **MonteCarlo.jl** - Monte Carlo simulations

### Astro Packages
- **JuliaAstro** - Astronomy ecosystem
- **Celeste.jl** - Astronomical source classification

---

## 10. Databáze a Katalogy (Přístup přes astroquery)

### Astro-databáze
- **SIMBAD** - Astronomical object database (bibliografie, identifikace)
- **Gaia** - 1.46+ miliardy hvězd (astrometrie, proper motion, parallax)
- **SDSS** - Spectroscopic survey (galaxie, quasary, hvězdy)
- **2MASS** - Infrared survey
- **AllWISE** - Mid-infrared survey
- **Chandra Source Catalog**
- **eROSITA** - X-ray survey
- **Hubble Source Catalog**
- **VizieR** - Astronomical catalogues

### Data Repositories
- **MAST** - Mikulski Archive for Space Telescopes (Hubble, JWST, TESS)
- **HEASARC** - High Energy Astrophysics Science Archive
- **IRSA** - Infrared Science Archive
- **NED** - NASA/IPAC Extragalactic Database

---

## 11. Jupyter Notebooks a Tutorials

### Astrofyzikální Dema
- **astro-Jupyter** - Undergraduate-level astrophysics demo codes
  - Radiation (blackbody, photons)
  - Gravity (orbits, binary stars, Lagrange points)
  - Relativity (SR, GR)
  - N-body simulations

### Učební Materiály
- **Python for Astronomers** - Free textbook + tutorials
- **Astronomy 330** - Scientific computing in astrophysics
- **MAST Notebooks** - JWST, TESS, Hubble tutorials
- **Gaia ESA Notebooks** - Gaia data tutorials
- **AstroInteractives** - Interactive astronomy demos

---

## 12. Astrofotografie (Volitelné)

### Image Processing
- **Siril** - Astrophotography image processing
- **AstroPixelProcessor** - Image calibration and processing
- **DeepSkyStacker** - Image stacking

---

## 13. Další Užitečné Nástroje

### Data Analysis
- **scikit-learn** - Machine learning
- **scikit-image** - Image processing
- **xarray** - Labeled multi-dimensional arrays
- **h5py** - HDF5 file format
- **zarr** - Compressed cloud-optimized storage

### Teoretické Nástroje
- **FEniCSx** - Finite element method
- **MDAnalysis** - Molecular dynamics
- **ASE** - Atomic Simulation Environment

### Visualization
- **mayavi** - 3D scientific visualization
- **pyvista** - 3D mesh analysis
- **paraview** - Large data visualization

---

## 📦 Instalační Priorita

### Fáze 1: Základní Python Stack (Nejdůležitější)
1. astropy, numpy, scipy, sympy, matplotlib, pandas
2. jupyter, ipython
3. astroquery, astroML

### Fáze 2: Specializované Astro Balíčky
4. rebound, gala, yt
5. qutip, specutils, photutils
6. bokeh, holoviews, datashader

### Fáze 3: Desktop Software
7. Stellarium
8. Celestia
9. DS9/SAOImage

### Fáze 4: High-energy Tools
10. HEASoft (pokud potřebujete X-ray data)

### Fáze 5: Symbolic Computation
11. SageMath
12. Maxima

### Fáze 6: Julia (Volitelné)
13. Julia + physics packages

### Fáze 7: Datasets a Tutorials
14. Clone Jupyter notebook repositories
15. Download sample datasets (Gaia, SDSS)

---

## 💾 Odhad Velikosti

- Python balíčky: ~5-10GB
- Stellarium: ~1-2GB
- Celestia: ~500MB-1GB
- DS9: ~100-200MB
- HEASoft: ~2-3GB
- SageMath: ~5-8GB
- Julia + packages: ~3-5GB
- Jupyter notebooks: ~500MB-1GB
- Sample datasets: ~5-10GB

**Celkem:** ~20-40GB (zanechává dost prostoru pro vlastní data)

---

## 🔗 Užitečné Odkazy

- Astropy: https://www.astropy.org/
- REBOUND: https://rebound.hanno-rein.de/
- Gala: https://gala.adrian.pw/
- yt: https://yt-project.org/
- QuTiP: https://qutip.org/
- Stellarium: https://stellarium.org/
- Celestia: https://www.celestiaproject.space/
- DS9: http://ds9.si.edu/
- HEASoft: https://heasarc.gsfc.nasa.gov/lheasoft/
- SageMath: https://www.sagemath.org/
- Maxima: https://maxima.sourceforge.io/
- Julia: https://julialang.org/
- NASA Eyes: https://science.nasa.gov/eyes/
