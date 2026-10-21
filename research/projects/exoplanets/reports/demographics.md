# Exoplanet Demographics Report

Generated from data/processed/exoplanets.csv (6451 confirmed planets, NASA Exoplanet Archive).

## Sample

- Total confirmed planets: 6451
- Discovery methods: Transit (4785), RV (1204), Microlensing (292), Imaging (98), TTV (29), ETV (17), others (26)
- Median planet radius: 2.47 R_earth
- Median planet mass: 170 M_earth (where measured)
- Median stellar Teff: 5544 K
- Median distance: 349 pc

## Radius valley (Fulton gap)

The radius distribution shows a gap at ~1.5-2.0 R_earth, separating rocky super-Earths from gas-rich mini-Neptunes. This is attributed to photoevaporation and core-powered mass loss.

## Mass-radius relation

Rocky planets follow R ~ M^0.28 (Zeng et al. 2016). Gas-rich planets have R ~ M^0.5-0.7. The transition occurs at ~1.5-1.8 R_earth.

## Habitable zone

100 planets fall in the conservative habitable zone (Kopparapu 2013). Most are around M dwarfs (small stars, close-in HZ).

## Demographics by method

Transit dominates (74%), followed by RV (19%). Microlensing (4.5%) finds cold planets at large separations. Direct imaging (1.5%) finds young, wide-separation giants.

## Reproduce

    python notebooks/01_exoplanet_catalog.ipynb
    python models/equations.py
