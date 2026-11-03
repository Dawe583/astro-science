# Local Volume (d < 150 ly) — Data Inventory

Generated 2026-11-03.

## Contents

| File | Rows | Description |
|---|---|---|
| `data/processed/local_volume_gaia.csv` | 38,847 | Gaia DR3 sources within 150 ly (parallax > 21.75 mas, parallax/error > 5) |
| `data/processed/local_volume_gaia_full.csv` | 38,847 | Above + astrophysical params (Teff, logg, [M/H], distance, A_G) for 12,265 sources |
| `data/processed/local_volume_aps.csv` | 12,265 | Astrophysical parameters subset |
| `data/processed/local_volume_exoplanets.csv` | 877 | Confirmed exoplanets within 150 ly (NASA Exoplanet Archive) |

## Key findings

- **38,847 stars** within 150 ly of the Sun (Gaia DR3)
- **21,757 with radial velocities** (56%)
- **12,265 with Teff** from GSP-Phot
- **877 confirmed exoplanets** around 560 host stars within 150 ly
- **No confirmed stellar-mass black holes** within 150 ly (nearest: Gaia BH1 at ~480 pc)
- **No known neutron stars/pulsars** within 150 ly (nearest: RX J1856 at ~120 pc = 390 ly)
- **No quasars or galaxies** within 150 ly (all extragalactic; nearest galaxy Canis Major Dwarf at ~25 kly)
- **Brown dwarfs and white dwarfs** are present in the Gaia catalog (late-type, cool sources)

## Distance distribution
- Range: 4.25 - 149.97 ly
- Median: ~80 ly

## Data budget
- Gaia CSV: ~15 MB
- Exoplanets CSV: ~0.5 MB
- Total local volume data: < 100 MB (well within 35 GB limit)

## Reproduce
    .venv/bin/python scripts/download_local_volume_gaia.py
    .venv/bin/python scripts/download_local_volume_aps.py
    .venv/bin/python scripts/download_local_volume_exoplanets.py
PY