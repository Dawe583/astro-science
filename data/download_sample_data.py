#!/usr/bin/env python
"""
Download sample astronomy datasets using astroquery
"""
import os
from astropy.coordinates import SkyCoord
from astropy import units as u
from astroquery.sdss import SDSS
from astroquery.gaia import Gaia
from astroquery.simbad import Simbad
from astropy.io import fits
import numpy as np

# Create directories
os.makedirs('fits', exist_ok=True)
os.makedirs('catalogs', exist_ok=True)
os.makedirs('cmb', exist_ok=True)

print("Downloading sample astronomy data...")

# 1. Download SDSS spectrum
print("\n1. Downloading SDSS spectrum sample...")
try:
    pos = SkyCoord(ra=150.1*u.deg, dec=2.2*u.deg, frame='icrs')
    xid = SDSS.query_xid(pos, spectro=True)
    if xid is not None and len(xid) > 0:
        spec = SDSS.get_spectra(xid[0])
        if spec is not None:
            spec.writeto('fits/sdss_sample_spectrum.fits', overwrite=True)
            print("   ✓ SDSS spectrum downloaded")
    else:
        print("   No SDSS spectrum found at position")
except Exception as e:
    print(f"   ✗ SDSS download failed: {e}")

# 2. Download Gaia catalog sample
print("\n2. Downloading Gaia catalog sample...")
try:
    Gaia.login()
    query = """
    SELECT TOP 1000
    source_id, ra, dec, parallax, pmra, pmdec, g_mag
    FROM gaiadr2.gaia_source
    WHERE parallax > 10
    ORDER BY random_index
    """
    job = Gaia.launch_job(query)
    r = job.get_results()
    r.write('catalogs/gaia_sample.fits', overwrite=True)
    print("   ✓ Gaia catalog downloaded (1000 stars)")
except Exception as e:
    print(f"   ✗ Gaia download failed: {e}")

# 3. Download SIMBAD data
print("\n3. Downloading SIMBAD data for M31...")
try:
    result_table = Simbad.query_object('M31')
    result_table.write('catalogs/m31_simbad.fits', overwrite=True)
    print("   ✓ SIMBAD data for M31 downloaded")
except Exception as e:
    print(f"   ✗ SIMBAD download failed: {e}")

# 4. Create synthetic CMB map using healpy
print("\n4. Creating synthetic CMB map...")
try:
    import healpy as hp
    # Create a simple CMB-like map
    nside = 64
    npix = hp.nside2npix(nside)
    cmb_map = np.random.normal(0, 100, npix)
    hp.write_map('cmb/synthetic_cmb_map.fits', cmb_map, overwrite=True)
    print("   ✓ Synthetic CMB map created")
except Exception as e:
    print(f"   ✗ CMB map creation failed: {e}")

# 5. Create sample galaxy catalog
print("\n5. Creating sample galaxy catalog...")
try:
    from astropy.table import Table
    n_galaxies = 1000
    ra = np.random.uniform(0, 360, n_galaxies)
    dec = np.random.uniform(-90, 90, n_galaxies)
    redshift = np.random.uniform(0.01, 0.5, n_galaxies)
    magnitude = np.random.uniform(15, 25, n_galaxies)
    
    table = Table()
    table['ra'] = ra * u.deg
    table['dec'] = dec * u.deg
    table['redshift'] = redshift
    table['magnitude'] = magnitude * u.mag
    table.write('catalogs/sample_galaxies.fits', overwrite=True)
    print("   ✓ Sample galaxy catalog created (1000 galaxies)")
except Exception as e:
    print(f"   ✗ Galaxy catalog creation failed: {e}")

print("\n✓ Sample data download complete!")
print("\nDownloaded files:")
print("  - fits/sdss_sample_spectrum.fits")
print("  - catalogs/gaia_sample.fits (1000 stars)")
print("  - catalogs/m31_simbad.fits")
print("  - cmb/synthetic_cmb_map.fits")
print("  - catalogs/sample_galaxies.fits (1000 galaxies)")
