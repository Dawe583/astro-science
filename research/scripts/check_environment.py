from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
import sys

packages = ["numpy", "scipy", "astropy", "astroquery", "photutils", "astroplan", "specutils", "reproject", "matplotlib", "pandas", "jupyterlab", "rebound", "gala", "yt", "camb", "classy", "healpy", "pyshtools", "emcee", "bilby", "gammapy", "stingray", "spiceypy"]
print(f"Python {sys.version.split()[0]} | executable: {sys.executable}")
missing = []
for package in packages:
    try:
        print(f"{package}: {version(package)}")
    except PackageNotFoundError:
        missing.append(package)
print("Missing:", ", ".join(missing) if missing else "none")
raise SystemExit(bool(missing))
