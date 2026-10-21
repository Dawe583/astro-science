#!/usr/bin/env python3
"""Download confirmed exoplanets from the NASA Exoplanet Archive."""

import urllib.request
from pathlib import Path

OUT = Path("data/raw/exoplanets_confirmed.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)

# NASA Exoplanet Archive TAP query — confirmed planets with key parameters
COLUMNS = [
    "pl_name", "hostname", "pl_letter", "discoverymethod", "disc_year",
    "pl_orbper", "pl_orbsmax", "pl_rade", "pl_radj", "pl_bmasse", "pl_bmassj",
    "pl_dens", "pl_eqt", "pl_insol", "pl_trandep", "pl_trandur", "pl_ratdor",
    "pl_ratror", "pl_imppar",
    "st_teff", "st_rad", "st_mass", "st_lum", "st_met", "st_logg",
    "st_age", "st_dens", "st_vsin", "st_rotp",
    "sy_dist", "sy_vmag", "sy_kmag", "sy_gaiamag",
    "ra", "dec", "pl_controv_flag",
]
cols = ",".join(COLUMNS)
query = "select %s from ps where default_flag=1" % cols
url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=%s&format=csv" % urllib.parse.quote(query) if False else None
import urllib.parse
url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=%s&format=csv" % urllib.parse.quote(query)

print("Downloading from NASA Exoplanet Archive...")
print("URL:", url[:120], "...")
urllib.request.urlretrieve(url, OUT)
print("Saved to", OUT)
# count rows
import csv
with open(OUT) as f:
    n = sum(1 for _ in f) - 1
print("Rows:", n)
