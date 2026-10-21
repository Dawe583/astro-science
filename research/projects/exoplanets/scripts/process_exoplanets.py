#!/usr/bin/env python3
"""Process NASA Exoplanet Archive into a clean catalog."""

from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/exoplanets_confirmed.csv"
OUT = ROOT / "data/processed/exoplanets.csv"
OUT.parent.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RAW)
print("Raw rows:", len(df))

# Keep confirmed planets (default_flag already filtered in download)
# Compute derived quantities
df["pl_rade"] = pd.to_numeric(df["pl_rade"], errors="coerce")
df["pl_bmasse"] = pd.to_numeric(df["pl_bmasse"], errors="coerce")
df["pl_orbper"] = pd.to_numeric(df["pl_orbper"], errors="coerce")
df["st_teff"] = pd.to_numeric(df["st_teff"], errors="coerce")
df["st_lum"] = pd.to_numeric(df["st_lum"], errors="coerce")
df["st_mass"] = pd.to_numeric(df["st_mass"], errors="coerce")
df["sy_dist"] = pd.to_numeric(df["sy_dist"], errors="coerce")

# Habitable zone flag (conservative: between moist_greenhouse and max_greenhouse)
def in_hz(row):
    if pd.isna(row["st_lum"]) or pd.isna(row["pl_orbsmax"]):
        return False
    L = row["st_lum"]
    a = row["pl_orbsmax"]
    if not np.isfinite(L) or L <= 0:
        return False
    rv = np.sqrt(L / 1.776)
    mg = np.sqrt(L / 0.356)
    return bool(rv <= a <= mg)

df["in_hz"] = df.apply(in_hz, axis=1)

# Rocky planet flag (radius < 1.8 R_earth, likely rocky)
df["likely_rocky"] = df["pl_rade"] < 1.8

# Mass-radius density estimate (g/cm3) for planets with mass and radius
df["density_gcm3"] = df["pl_bmasse"] / (df["pl_rade"] ** 3) * 5.51  # relative to Earth

# Save
cols_keep = ["pl_name", "hostname", "discoverymethod", "disc_year", "pl_orbper",
             "pl_orbsmax", "pl_rade", "pl_bmasse", "pl_dens", "pl_eqt", "pl_insol",
             "st_teff", "st_rad", "st_mass", "st_lum", "st_met", "sy_dist",
             "ra", "dec", "in_hz", "likely_rocky", "density_gcm3"]
df[cols_keep].to_csv(OUT, index=False)
print("Processed rows:", len(df))
print("In HZ:", df["in_hz"].sum())
print("Likely rocky:", df["likely_rocky"].sum())
print("Saved to", OUT)
