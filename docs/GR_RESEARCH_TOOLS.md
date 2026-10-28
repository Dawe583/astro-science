# General Relativity & Gravitational Wave Research Tools

## Overview

This document lists all tools installed for real astrophysics/GR research.
All tools are in the project's `.venv` (Python 3.14) or system packages.

## Installed Tools

### Core Scientific Computing (already in .venv)
| Package | Version | Purpose |
|---|---|---|
| numpy | 2.3.5 | Numerical arrays |
| scipy | 1.16.3 | Scientific computing |
| astropy | 5.x | Units, constants, cosmology |
| matplotlib | 3.x | Plotting |
| sympy | 1.x | Symbolic math |
| pandas | 2.x | Data frames |
| h5py | 3.x | HDF5 files (GWOSC strain) |
| jupyter | 1.x | Notebooks |

### Gravitational Wave Analysis
| Package | Version | Purpose |
|---|---|---|
| bilby | 2.8.2 | Bayesian inference for GW parameters |
| pycbc | 2.11.0 | GW search, waveform generation, matched filtering |
| lalsuite | 7.26.16 | LIGO algorithm library (C/Python) |
| ligo.skymap | 2.5.4 | Sky localization for GW events |
| gwosc | 0.8.3 | GWOSC data access (catalogs, strain) |
| ligo-gracedb | 2.16.1 | GraceDB API client |

### Numerical Relativity
| Package | Version | Purpose |
|---|---|---|
| einsteinpy | 0.4.0 | Einstein field equations, geodesics, metrics |

### Symbolic / Tensor Algebra
| Tool | Source | Purpose |
|---|---|---|
| SymPy | .venv | Symbolic math, tensor basics |
| SageMath | system (python3) | Manifolds, differential geometry, GR |

### Not Available (requires heavy setup)
| Tool | Why not | Alternative |
|---|---|---|
| Einstein Toolkit (Cactus) | Requires MPI, HDF5, C/Fortran build | einsteinpy (Python) |
| Mathematica + xAct | Commercial, not installed | SymPy + SageMath |
| Cadabra2 | Complex C++ build | SymPy tensor module |
| LISA tools | Not yet packaged | bilby + custom waveforms |

## Quick Start: Gravitational Wave Analysis

```python
# 1. Download GWOSC data
from gwosc.datasets import find_datasets
events = find_datasets(type="events", detector="H1")
print(f"Found {len(events)} events")

# 2. Load strain data
from gwosc.api import fetch_event_json
event = fetch_event_json("GW150914")
print(event)

# 3. Generate waveform with PyCBC
from pycbc.waveform import get_td_waveform
hp, hc = get_td_waveform(approximant="IMRPhenomD",
                          mass1=36, mass2=29,
                          spin1z=0, spin2z=0,
                          delta_t=1.0/4096, f_lower=20)

# 4. Bayesian inference with Bilby
import bilby
# See bilby tutorials: https://lscsoft.docs.ligo.org/bilby/
```

## Quick Start: Numerical Relativity

```python
# EinsteinPy: geodesics in Schwarzschild
from einsteinpy.geodesic import Geodesic
from einsteinpy.metric import Schwarzschild
import numpy as np

# Schwarzschild metric, M=1
metric = Schwarzschild(M=1.0)
# Timelike geodesic
geo = Geodesic(metric=metric, position=[10, np.pi/2, 0],
                momentum=[0, 0, 0.1], timelike=True)
geo.trajectory  # integrate
```

## Quick Start: Symbolic GR with SageMath

```python
# SageMath manifold (run with system python3)
from sage.all import *
M = Manifold(4, 'M', latex_name=r'\mathcal{M}')
# Define metric, Christoffel, Riemann, etc.
# See: https://doc.sagemath.org/html/en/reference/manifolds/
```

## Quick Start: LIGO Sky Localization

```python
import ligo.skymap
# Plot skymap from a GW event
# See: https://lscsoft.docs.ligo.org/ligo.skymap/
```

## Data Sources (all real)

| Source | URL | Access |
|---|---|---|
| GWOSC | https://gwosc.org | Free, no auth |
| HEASARC | https://heasarc.gsfc.nasa.gov | Free, TAP |
| VizieR | https://vizier.cds.unistra.fr | Free (sometimes unreachable) |
| NASA Exoplanet Archive | https://exoplanetarchive.ipac.caltech.edu | Free, TAP |
| BlackCAT | https://github.com/BlackCAT (via VizieR) | Free |
| LIGO Open Data | https://www.gw-openscience.org | Free |

## What's NOT installed (and why)

| Tool | Reason | How to get |
|---|---|---|
| Einstein Toolkit (Cactus) | Heavy C/Fortran build, needs MPI+HDF5 | Build from source (days) |
| Mathematica | Commercial ($$$) | Use SymPy/SageMath instead |
| Cadabra2 | Complex C++ build | Use SymPy tensor module |
| LISA analysis tools | Not yet packaged for Python 3.14 | Wait for release |

## Next Steps for Real Research

1. **Learn Bilby**: Run the tutorials at https://lscsoft.docs.ligo.org/bilby/
2. **Learn PyCBC**: Generate waveforms, do matched filtering
3. **Download GWOSC strain**: Already have HDF5 files for GW170817, GW190814, GW190521
4. **Run a parameter estimation**: Use Bilby on GW150914
5. **Compare with GR**: Test if the data is consistent with GR predictions
6. **Publish**: If you find an anomaly, write a paper and submit to arXiv

## Honest Assessment

These tools give you the **capability** to do real GW analysis, but making a
**discovery** requires:
- Deep understanding of GR, statistics, and signal processing
- Months of learning the tools and data
- Access to LIGO collaboration for peer review
- Original insight that hasn't been explored before

The tools are necessary but not sufficient. The "discovery" comes from the
researcher, not the software.
