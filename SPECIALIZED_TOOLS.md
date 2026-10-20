# Specializované Nástroje pro Astrofyziku a Kosmologii

Dodatečně nainstalované specializované nástroje pro pokročilou astrofyziku a kosmologii.

---

## 📊 High-Energy Physics Data Analysis

### Uproot (5.7.7)
**Popis:** Čtení ROOT souborů v Pythonu bez C++

**Použití:**
```python
import uproot

# Čtení ROOT souborů z LHC
file = uproot.open("events.root")
tree = file["Events"]
data = tree.arrays(["pt", "eta", "phi", "energy"])

# Analýza
print(data)
```

**Příklady použití:**
- LHC data analysis
- Particle physics data
- Čtení ROOT formátu
- Analýza Monte Carlo events

---

### Awkward (2.14.0)
**Popis:** Složité nested pole pro HEP data

**Použití:**
```python
import awkward as ak

# Jagged arrays pro různé počty částic
events = ak.Array([
    [[1.0, 2.0], [3.0]],
    [[4.0, 5.0, 6.0]],
    [[7.0]]
])

# Filtry a operace
selected = events[events > 2.0]
```

**Příklady použití:**
- Komplexní HEP data
- Event-level data
- Jagged arrays
- Paralelní zpracování

---

### Iminuit (2.33.0)
**Popis:** Minimization a fitting (port MINUIT2)

**Použití:**
```python
from iminuit import Minuit

def f(x, y):
    return (x - 1)**2 + (y - 2)**2

m = Minuit(f, x=0, y=0)
m.migrad()
print(m.values)
```

**Příklady použití:**
- Fitting v particle physics
- Statistické analýzy
- Likelihood fitting
- Parameter estimation

---

### Particle (1.0.1)
**Popis:** Particle physics data z PDG database

**Použití:**
```python
from particle import Particle

# Informace o částicích
pion = Particle.from_pdgid(211)
print(f"Mass: {pion.mass}")
print(f"Charge: {pion.charge}")
print(f"Name: {pion.name}")

# Hledání částic
higgs = Particle.from_name("Higgs boson")
```

**Příklady použití:**
- Particle properties
- PDG database access
- Decay modes
- Cross sections

---

### PyHepMC (2.16.1)
**Popis:** Event records pro Monte Carlo events

**Použití:**
```python
import pyhepmc

# Čtení event data
with pyhepmc.Reader("events.hepmc") as f:
    for event in f:
        for particle in event.particles:
            print(particle.momentum)
```

**Příklady použití:**
- Monte Carlo events
- Event generation
- HepMC format
- Particle tracking

---

### HepUnits (2.4.7)
**Popis:** Fyzikální jednotky pro HEP

**Použití:**
```python
from hepunits import GeV, MeV, mm, ns

energy = 13 * GeV
distance = 100 * mm
time = 25 * ns
```

**Příklady použití:**
- Particle physics units
- Standardní konstanty
- Cross section units
- Energy scales

---

## 🌌 Cosmology Simulation

### SkyPy (0.5.5)
**Popis:** Python-based cosmological simulations

**Použití:**
```python
import skypy

# Kosmologická simulace
redshift = skypy.galaxies.redshift.redshift_distribution()
luminosity = skypy.galaxies.luminosity.luminosity_function()
```

**Příklady použití:**
- Cosmological simulations
- Galaxy formation
- Large-scale structure
- Mock galaxy catalogs

---

## 📡 Radio Astronomy

### Katdal (0.23)
**Popis:** MeerKAT data access pro radio interferometry

**Použití:**
```python
import katdal

# Přístup k MeerKAT data
data = katdal.open('meerkat_observation.h5')
print(data.shape)
print(data.visibilities)
```

**Příklady použití:**
- MeerKAT data processing
- Radio interferometry
- Visibility data
- Calibration

---

### Katpoint (0.10.3)
**Popis:** Radio astronomy pointing a coordinates

**Použití:**
```python
import katpoint

# Antenna pointing
antenna = katpoint.Antenna('name, 20:00:00, -30:00:00, 1000')
target = katpoint.Target('Jupiter')
az, el = antenna.pointing(target)
```

**Příklady použití:**
- Radio telescope pointing
- Coordinate systems
- Antenna positions
- Observation planning

---

## ⚡ Non-thermal Astrophysics

### Naima (0.10.4)
**Popis:** Non-thermal modeling pro gamma-ray astronomy

**Použití:**
```python
import naima
from naima.models import ExponentialCutoffPowerLaw

# Modelování ne-termálních procesů
model = ExponentialCutoffPowerLaw(amplitude=1e-12, index=2.0)
```

**Příklady použití:**
- Gamma-ray astronomy
- Particle acceleration
- Non-thermal emission
- Supernova remnants

---

## 🔬 Další Specializované Nástroje (Vyžadují Sudo/Build)

Tyto nástroje vyžadují kompilaci nebo root práva. Mohou být nainstalovány manuálně:

### Numerical Relativity
- **Einstein Toolkit** - Numerical relativity simulations
  - McLachlan (vacuum spacetime solver)
  - GRHydro (relativistic hydrodynamics)
  - IllinoisGRMHD (GRMHD)
  - https://www.einsteintoolkit.org/

- **GRChombo** - Numerical relativity s AMR
  - https://www.grchombo.org/

- **GRTeclyn** - GR simulations na AMReX
  - GPU support

### Cosmological N-body
- **GADGET-2/3** - Cosmological N-body/SPH simulations
  - https://wwwmpa.mpa-garching.mpg.de/gadget/
  - Large-scale structure
  - Galaxy formation

### Particle Physics
- **ROOT** - C++ framework pro HEP data analysis
  - https://root.cern.ch/
  - Data I/O, fitting, visualization
  - ~1GB+

- **Geant4** - Monte Carlo simulation
  - https://geant4.web.cern.ch/
  - Detector simulation
  - ~2GB+

### Radio Astronomy
- **CASA** - Common Astronomy Software Applications
  - https://casa.nrao.edu/
  - Radio interferometry data reduction
  - MeerKAT, ALMA processing

---

## 📊 Shrnutí

**Nainstalované Python balíčky:**
- High-Energy Physics: 6 balíčků
- Cosmology: 1 balíček
- Radio Astronomy: 2 balíčky
- Non-thermal: 1 balíček
- **Celkem:** 10 nových specializovaných balíčků

**Počet kategorií:** 29+

**Doporučené manuální instalace (vyžadují sudo/compilaci):**
- Einstein Toolkit (numerical relativity)
- GADGET-3 (cosmological N-body)
- ROOT (HEP data analysis)
- Geant4 (detector simulation)
- CASA (radio astronomy)

---

## 🎯 Jak Používat

**High-Energy Physics:**
```python
import uproot, awkward, iminuit, particle
# Čtení a analýza ROOT souborů
```

**Cosmology:**
```python
import skypy
# Kosmologické simulace
```

**Radio Astronomy:**
```python
import katdal, katpoint
# MeerKAT data processing
```

**Non-thermal:**
```python
import naima
# Gamma-ray modeling
```

Vše je připraveno k použití v Jupyter Lab!
