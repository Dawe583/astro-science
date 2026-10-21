# Exoplanets

Exoplanets are planets orbiting stars other than the Sun. Over 5600 are
confirmed, spanning gas giants, mini-Neptunes, super-Earths, and rocky
terrestrial worlds.

## Detection methods

- **Transit** — flux drop $\delta=(R_p/R_*)^2$; dominant method (Kepler, TESS).
- **Radial velocity** — Doppler wobble gives minimum mass $M_p\sin i$.
- **Direct imaging** — spatially resolved planets at wide separations.
- **Microlensing** — mass and distance from Einstein radius.
- **Astrometry** — orbital inclination from Gaia.

## Orbital dynamics

Kepler's laws, orbital elements, resonances (Laplace), tidal locking and
heating, Hill stability, Roche limit.

## Habitability

Conservative habitable zone (Kopparapu et al. 2013): inner edge
$\sim 0.95$ AU, outer $\sim 1.68$ AU for Sun-like stars. Tidal locking,
atmospheric escape, and biosignatures (O$_2$, CH$_4$, H$_2$O) determine
actual habitability.

## Atmospheric characterization

Transmission and emission spectroscopy; molecular absorption features;
retrieval; JWST and Ariel.

## Demographics

Radius valley at $\sim 1.5$–$2.0\,R_\oplus$ (Fulton gap). Mass-radius
relation: rocky $R \propto M^{0.28}$, volatile $R \propto M^{0.5-0.7}$.
Occurrence rates depend on stellar metallicity and orbital period.

## See also

- [[Detection Methods]] — transit, RV, imaging, microlensing, astrometry
- [[Habitability]] — HZ, tidal locking, atmospheric escape, biosignatures
- [[Atmospheric Characterization]] — transmission/emission spectroscopy
- [[Gravitational Wave Analysis]] — (shared orbital dynamics)
- [[Kerr Metric]] — (compact objects)

## Source

- Data: `data/processed/exoplanets.csv` (6451 confirmed planets)
- Models: `models/equations.py`
- Notebook: `notebooks/01_exoplanet_catalog.ipynb`
- Theory: `premium/theory_orbital_dynamics.md`
