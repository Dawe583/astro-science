#!/usr/bin/env python3
"""Download astrophysical parameters (Teff, logg, [M/H], distance, A_G) for the
local volume from Gaia DR3 (join gaia_source x astrophysical_parameters).

Run: /home/dawe/Projects/astro-science/.venv/bin/python scripts/download_local_volume_aps.py
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

from astroquery.gaia import Gaia
import pandas as pd

PARALLAX_MIN = 1000.0 / 45.98

QUERY = f"""
SELECT TOP 100000
    ap.source_id, ap.teff_gspphot, ap.logg_gspphot, ap.mh_gspphot,
    ap.distance_gspphot, ap.azero_gspphot, ap.ag_gspphot,
    ap.spectraltype_esphs
FROM gaiadr3.astrophysical_parameters AS ap
JOIN gaiadr3.gaia_source AS g ON ap.source_id = g.source_id
WHERE g.parallax > {PARALLAX_MIN}
  AND g.parallax_over_error > 5
"""


def main():
    log.info("Querying Gaia DR3 astrophysical parameters for local volume ...")
    job = Gaia.launch_job_async(QUERY)
    res = job.get_results()
    df = res.to_pandas()
    log.info(f"Retrieved {len(df)} rows with APs")
    out = PROC / "local_volume_aps.csv"
    df.to_csv(out, index=False)
    log.info(f"Wrote {out}")
    # merge into main gaia catalog
    main_df = pd.read_csv(PROC / "local_volume_gaia.csv")
    merged = main_df.merge(df, on="source_id", how="left")
    merged.to_csv(PROC / "local_volume_gaia_full.csv", index=False)
    log.info(
        f"Merged catalog: {len(merged)} rows, Teff non-null: {merged['teff_gspphot'].notna().sum()}"
    )


if __name__ == "__main__":
    main()
