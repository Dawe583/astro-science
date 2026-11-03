#!/usr/bin/env python3
"""Download confirmed exoplanets within 150 ly (46 pc) from the NASA Exoplanet Archive.

Uses the IPAC/NExScI TAP service (ps table). Writes data/processed/local_volume_exoplanets.csv.
Run: /home/dawe/Projects/astro-science/.venv/bin/python scripts/download_local_volume_exoplanets.py
"""

import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
PROC.mkdir(parents=True, exist_ok=True)

from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive
import pandas as pd

# 150 ly = 45.98 pc
DIST_PC = 45.98


def main():
    log.info("Querying NASA Exoplanet Archive for planets within 150 ly ...")
    # ps table has one row per planet; sy_dist is host-star distance in pc
    cols = [
        "pl_name",
        "hostname",
        "sy_dist",
        "sy_disterr1",
        "sy_pnum",
        "pl_orbper",
        "pl_orbsmax",
        "pl_rade",
        "pl_radj",
        "pl_bmasse",
        "pl_bmassj",
        "pl_eqt",
        "pl_insol",
        "pl_dens",
        "discoverymethod",
        "disc_year",
        "st_teff",
        "st_rad",
        "st_mass",
        "st_met",
        "st_spectype",
        "ra",
        "dec",
        "sy_vmag",
        "sy_kmag",
    ]
    query = f"sy_dist < {DIST_PC} and default_flag = 1"
    try:
        tab = NasaExoplanetArchive.query_criteria(
            table="ps", select=",".join(cols), where=query
        )
        df = tab.to_pandas()
    except Exception as e:
        log.warning(f"query_criteria failed: {e}; trying full table filter")
        tab = NasaExoplanetArchive.query_criteria(table="ps", select=",".join(cols))
        df = tab.to_pandas()
        df = df[df["sy_dist"] < DIST_PC]

    log.info(f"Retrieved {len(df)} planets")
    df["distance_ly"] = df["sy_dist"] * 3.26156
    out = PROC / "local_volume_exoplanets.csv"
    df.to_csv(out, index=False)
    log.info(f"Wrote {out}")

    print(f"\nLocal volume exoplanets (d < 150 ly)")
    print(f"  planets: {len(df)}")
    print(f"  unique hosts: {df['hostname'].nunique()}")
    print(f"  methods: {df['discoverymethod'].value_counts().to_dict()}")
    print(f"  distance range: {df['sy_dist'].min():.2f} - {df['sy_dist'].max():.2f} pc")


if __name__ == "__main__":
    main()
