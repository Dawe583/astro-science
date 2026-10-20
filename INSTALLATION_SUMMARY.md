# Instalační Shrnutí - Astrofyzikální Výzkumné Prostředí

## ✅ Nainstalováno

### Python Balíčky (v .venv/)
**Základní Scientific Stack:**
- numpy 2.5.4
- scipy 1.18.1
- sympy 1.14.0
- pandas 3.0.6
- matplotlib 3.11.2
- seaborn 0.13.2

**Jupyter a Development:**
- jupyter 1.1.1
- jupyterlab 4.6.4
- ipython 9.17.1

**Vizualizace:**
- bokeh 3.9.2
- holoviews 1.23.2
- datashader 0.19.1
- plotly 7.1.0
- altair 6.3.0
- pygal 3.1.3
- wordcloud 1.9.6
- mayavi 4.9.0
- pyvista 0.49.1
- scikit-image 0.26.0
- scikit-video 1.1.11

**Astrofyzika (Astropy Ecosystem):**
- astropy 8.0.2
- astroquery 0.4.11
- astroML 1.0.2
- photutils 3.1.0
- astroplan 0.10.1
- specutils 2.4.0
- reproject 0.21.0

**Simulace:**
- rebound 5.2.2
- gala 1.12.0
- yt 4.4.3

**Kvantová Fyzika:**
- qutip 5.3.1

**Data Analysis:**
- scikit-learn 1.9.1
- networkx 3.7
- xarray 2026.9.0
- numba 0.68.0

**Kosmologie:**
- camb 2.0.5
- classy 3.4.1.0

**CMB a Spherical Harmonics:**
- healpy 1.20.1
- shtools 2.2.2

**Statistical Inference:**
- emcee 3.1.6
- corner 2.3.0
- dynesty 3.1.0
- zeus 0.16.0
- bilby 2.8.2
- pymc 6.3.2
- arviz 1.3.0

**High-Energy Astrophysics:**
- stingray 2.3.2
- gammapy 2.1

**Atomic Simulation:**
- ase 3.29.0
- pymatgen 2026.9.24

**Plasma Physics:**
- pysat 3.2.2
- plasmapy 2026.2.0

**Space Physics/Ephemerides:**
- spiceypy 8.3.0

**3D Vizualizace:**
- pythreejs 2.4.2
- ipyvolume 0.6.3
- trame 4.0.0
- k3d 3.2.0

**Geospatial:**
- geopandas 1.2.0
- pydeck 0.9.3

**Quantum Computing:**
- qiskit 2.6.0
- qiskit-aer 0.17.2
- cirq 1.7.0
- pennylane 0.45.1

**Physical Units:**
- pint 0.26.1
- quantities 0.16.4

**Phonons:**
- phonopy 4.8.3

**Distributed Computing:**
- pyro4 4.82

**Machine Learning:**
- xgboost 3.4.1
- lightgbm 4.7.0
- catboost 1.2.10

**Solar Physics:**
- sunpy 8.0.1

**Image Alignment:**
- astroalign 2.6.2

**Gravitational Lensing:**
- lenstronomy 1.14.2

**Data Visualization:**
- glueviz 1.4.0
- glue-core 1.27.0

**Bioinformatics:**
- biopython 1.88

**Simulation:**
- simpy 4.1.2

**X-ray Analysis:**
- sherpa 4.19.0
- fitsio 1.4.2

**High-Energy Physics Data Analysis:**
- uproot 5.7.7
- awkward 2.14.0
- iminuit 2.33.0
- particle 1.0.1
- pyhepmc 2.16.1
- hepunits 2.4.7

**Cosmology Simulation:**
- skypy 0.5.5

**Radio Astronomy:**
- katdal 0.23
- katpoint 0.10.3

**Non-thermal Astrophysics:**
- naima 0.10.4

---

### Desktop Software

**Planetarium:**
- ✅ Stellarium 26.3 (AppImage)
  - Umístění: `~/tools/Stellarium-26.3-qt5-x86_64.AppImage`
  - Velikost: 551MB

- ⏳ Celestia (AUR - vyžaduje sudo)
  - Poznámka: Nainstalujte manuálně: `yay -S celestia`

**Image Viewers:**
- ✅ DS9/SAOImageDS9 8.8
  - Umístění: `~/.local/bin/ds9`
  - Velikost: 20MB

**Symbolic Computation:**
- ⏳ Maxima (vyžaduje sudo)
  - Poznámka: Nainstalujte manuálně: `yay -S maxima`

- ✅ Julia 1.11.2
  - Umístění: `~/tools/julia-1.11.2/`
  - Velikost: 273MB

---

### Jupyter Notebooks Repozitáře

- ✅ astro-Jupyter - Undergraduate astrophysics dema
- ✅ mast_notebooks - NASA MAST (JWST, TESS, Hubble)
- ✅ gaia-jupyter-notebooks - ESA Gaia tutorials
- ✅ AstroInteractives - Interactive astronomy demos

---

### Projektové Soubory

- ✅ requirements.txt - Python dependencies
- ✅ SETUP_GUIDE.md - Detailní setup instrukce
- ✅ TOOLS_LIST.md - Kompletní seznam nástrojů
- ✅ README.md - Přehled projektu
- ✅ start.sh - Startovací skript
- ✅ data/ - Adresář pro data

---

## 📊 Diskové Využití

**Odhad:**
- Python balíčky: ~25-30GB (rozšířené)
- Stellarium: 551MB
- DS9: 20MB
- Julia: 273MB
- Jupyter notebooks: ~500MB
- **Celkem:** ~27-32GB (z limitu 100GB)

**Volné místo:** 884GB (z 931GB celkem)
**Limit:** 100GB (přirozeně dodržen)

---

## 🚀 Jak Začít

### Rychlý Start
```bash
cd /home/dawe/Projects/astro-science
./start.sh lab
```

Nebo manuálně:
```bash
cd /home/dawe/Projects/astro-science
source .venv/bin/activate
jupyter lab
```

### Spuštění Desktop Aplikací

**Stellarium:**
```bash
~/tools/Stellarium-26.3-qt5-x86_64.AppImage
```

**DS9:**
```bash
ds9
```

**Julia:**
```bash
julia
```

---

## ⚠️ Manuální Instalace (vyžaduje sudo)

Následující nástroje nebyly nainstalovány, protože vyžadují sudo/yay:

```bash
# Celestia
yay -S celestia

# Maxima
yay -S maxima

# SageMath (volitelné, velký balíček)
yay -S sagemath
```

---

## 📚 Online Nástroje (Bez Instalace)

- **NASA Eyes:** https://science.nasa.gov/eyes/
- **SIMBAD:** https://simbad.harvard.edu/
- **Gaia Archive:** https://gea.esac.esa.int/archive/
- **SDSS SkyServer:** https://skyserver.sdss.org/

---

## ✅ Kontrolní Seznam

- [x] Python virtual environment vytvořen
- [x] Základní scientific stack nainstalován
- [x] Astrofyzikální balíčky nainstalovány
- [x] Vizualizační nástroje nainstalovány
- [x] Simulační nástroje nainstalovány
- [x] Kvantové fyzikální nástroje nainstalovány
- [x] Stellarium stažen a připraven
- [x] DS9 nainstalován
- [x] Julia nainstalována
- [x] Jupyter notebook repozitáře naklonovány
- [x] Dokumentace vytvořena
- [x] Startovací skript vytvořen
- [ ] Celestia (vyžaduje sudo)
- [ ] Maxima (vyžaduje sudo)
- [ ] SageMath (volitelné, vyžaduje sudo)

---

## 🎉 Jste Připraveni!

Všechny hlavní nástroje jsou nainstalovány a připraveny k použití. Začněte s:

```bash
cd /home/dawe/Projects/astro-science
./start.sh lab
```

A prozkoumejte dokumentaci v SETUP_GUIDE.md a tutoriály v naklonovaných repozitářích.
