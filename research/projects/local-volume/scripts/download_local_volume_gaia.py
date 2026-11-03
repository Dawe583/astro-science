#!/usr/bin/env python3
"""Download the local volume (d < 150 ly ~ 46 pc) stellar catalog from Gaia DR3.

Queries Gaia DR3 for all sources with parallax > 21.75 mas (d < 46 pc),
with astrometry, photometry and (where available) astrophysical parameters
and radial velocities. Writes a CSV + parquet to data/processed/.

Run: /home/dawe/Projects/astro-science/.venv/bin/python scripts/download_local_volume_gaia.py
"""

import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"
RAW.mkdir(parents=True, exist_ok=True)
PROC.mkdir(parents=True, exist_ok=True)

from astroquery.gaia import Gaia
import pandas as pd

# 150 ly = 45.98 pc -> parallax > 21.75 mas
PARALLAX_MIN_MAS = 1000.0 / 45.98  # mas

QUERY = f"""
SELECT TOP 100000
    source_id, ra, dec, parallax, parallax_error, parallax_over_error,
    pmra, pmra_error, pmdec, pmdec_error,
    radial_velocity, radial_velocity_error,
    phot_g_mean_mag, bp_rp, phot_bp_mean_mag, phot_rp_mean_mag,
    ruwe, astrometric_excess_noise, non_single_star
FROM gaiadr3.gaia_source
WHERE parallax > {PARALLAX_MIN_MAS}
  AND parallax_over_error > 5
ORDER BY parallax DESC
"""


def main():
    log.info("Querying Gaia DR3 for local volume (d < 150 ly) ...")
    job = Gaia.launch_job_async(QUERY)
    res = job.get_results()
    df = res.to_pandas()
    log.info(f"Retrieved {len(df)} sources")

    # Derived quantities
    df["distance_pc"] = 1000.0 / df["parallax"]
    df["distance_ly"] = df["distance_pc"] * 3.26156
    import numpy as np

    df["abs_mag_g"] = df["phot_g_mean_mag"] + 5 * np.log10(df["parallax"] / 1000.0)

    out_csv = PROC / "local_volume_gaia.csv"
    df.to_csv(out_csv, index=False)
    log.info(f"Wrote {out_csv} ({len(df)} rows)")

    # Summary
    print(f"\nLocal volume (d < 150 ly) Gaia DR3 catalog")
    print(f"  sources: {len(df)}")
    print(
        f"  distance range: {df['distance_ly'].min():.2f} - {df['distance_ly'].max():.2f} ly"
    )
    print(f"  with RV: {df['radial_velocity'].notna().sum()}")
    print(f"  non-single-star: {df['non_single_star'].notna().sum()}")


if __name__ == "__main__":
    main()
