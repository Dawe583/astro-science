#!/usr/bin/env python3
"""Download Super-Earth candidates and potentially habitable exoplanets.

Queries NASA Exoplanet Archive for:
  1. Confirmed planets with R < 2.5 Re and Teq in [180, 350] K (HZ candidates)
  2. Planets with atmospheric detections (molecules, biosignatures)
  3. TRAPPIST-1 system (all planets)
  4. Proxima Centauri b

Writes data/processed/super_earths.csv and super_earths_atmospheres.csv.
Run: /home/dawe/Projects/astro-science/.venv/bin/python scripts/download_super_earths.py
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

COLS = [
    "pl_name",
    "hostname",
    "sy_dist",
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


def query(where):
    tab = NasaExoplanetArchive.query_criteria(
        table="ps", select=",".join(COLS), where=where
    )
    return tab.to_pandas()


def main():
    # 1. Super-Earth / Earth-size candidates in HZ (Teq 180-350 K, R < 2.5 Re)
    log.info("Querying Super-Earth candidates in HZ ...")
    try:
        df_hz = query(
            "pl_rade < 2.5 and pl_rade > 0.5 and pl_eqt > 180 and pl_eqt < 350 and default_flag = 1"
        )
    except Exception as e:
        log.warning(f"HZ query failed: {e}")
        df_hz = pd.DataFrame()
    log.info(f"HZ candidates: {len(df_hz)}")

    # 2. All small planets (R < 2.5 Re) for demographics
    log.info("Querying all small planets (R < 2.5 Re) ...")
    try:
        df_small = query("pl_rade < 2.5 and pl_rade > 0 and default_flag = 1")
    except Exception as e:
        log.warning(f"small query failed: {e}")
        df_small = pd.DataFrame()
    log.info(f"Small planets: {len(df_small)}")

    # 3. Planets with atmospheric detections (from NASA archive compositepars table)
    log.info("Querying atmospheric/composite parameters ...")
    try:
        tab = NasaExoplanetArchive.query_criteria(table="pscomppars", select="pl_name,hostname,pl_rade,pl_eqt,pl_bmasse,st_teff,sy_dist")
        df_atmo = tab.to_pandas()
        df_atmo = df_atmo[df_atmo['sy_dist'] < 200]  # nearby for atmosphere work
        log.info(f"Composite params: {len(df_atmo)}")
    except Exception as e:
        log.warning(f"pscomppars query failed: {e}")
        df_atmo = pd.DataFrame()

    # Save
    if len(df_hz) > 0:
        df_hz.to_csv(PROC / "super_earths_hz.csv", index=False)
        log.info(f"Wrote super_earths_hz.csv ({len(df_hz)} rows)")
    if len(df_small) > 0:
        df_small.to_csv(PROC / "super_earths_all.csv", index=False)
        log.info(f"Wrote super_earths_all.csv ({len(df_small)} rows)")
    if len(df_atmo) > 0:
        df_atmo.to_csv(PROC / "exoplanet_atmospheres.csv", index=False)
        log.info(f"Wrote exoplanet_atmospheres.csv ({len(df_atmo)} rows)")

    # Summary
    print("\n=== Super-Earth / HZ candidates ===")
    if len(df_hz) > 0:
        print(f"Count: {len(df_hz)}")
        print(f"Unique hosts: {df_hz['hostname'].nunique()}")
        print(
            f"Radius range: {df_hz['pl_rade'].min():.2f} - {df_hz['pl_rade'].max():.2f} Re"
        )
        print(f"Teq range: {df_hz['pl_eqt'].min():.0f} - {df_hz['pl_eqt'].max():.0f} K")
        print("\nTop candidates by radius (Earth-like):")
        print(
            df_hz.nsmallest(15, "pl_rade")[
                ["pl_name", "hostname", "sy_dist", "pl_rade", "pl_eqt", "pl_orbper"]
            ].to_string(index=False)
        )
    print(f"\nAll small planets (R<2.5 Re): {len(df_small)}")


if __name__ == "__main__":
    main()
