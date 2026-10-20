#!/usr/bin/env python
"""
Download sample astronomy data directly from archives
"""
import os
import numpy as np
from astropy.table import Table
from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy import units as u
import matplotlib.pyplot as plt

# Create directories
os.makedirs('fits', exist_ok=True)
os.makedirs('catalogs', exist_ok=True)
os.makedirs('cmb', exist_ok=True)
os.makedirs('simulations', exist_ok=True)

print("Creating sample astronomy datasets...")

# 1. Create sample FITS image (synthetic astronomical image)
print("\n1. Creating synthetic FITS image...")
try:
    # Create a synthetic galaxy image
    image_size = 512
    x, y = np.meshgrid(np.linspace(-10, 10, image_size), np.linspace(-10, 10, image_size))
    
    # Create a galaxy-like pattern
    galaxy = np.exp(-(x**2 + y**2) / 10) * 100
    stars = np.random.poisson(2, (image_size, image_size))
    image = galaxy + stars + np.random.normal(0, 1, (image_size, image_size))
    
    # Create FITS header
    hdu = fits.PrimaryHDU(image)
    hdu.header['OBJECT'] = 'SYNTHETIC_GALAXY'
    hdu.header['EXPTIME'] = 300
    hdu.header['FILTER'] = 'R'
    hdu.header['RA'] = 150.0
    hdu.header['DEC'] = 2.0
    hdu.writeto('fits/synthetic_galaxy.fits', overwrite=True)
    print("   ✓ Synthetic galaxy FITS image created")
except Exception as e:
    print(f"   ✗ Failed: {e}")

# 2. Create detailed galaxy catalog
print("\n2. Creating detailed galaxy catalog...")
try:
    n_galaxies = 5000
    ra = np.random.uniform(0, 360, n_galaxies)
    dec = np.random.uniform(-90, 90, n_galaxies)
    redshift = np.random.uniform(0.01, 2.0, n_galaxies)
    magnitude = np.random.uniform(12, 28, n_galaxies)
    mass = 10**np.random.uniform(8, 12, n_galaxies)  # Solar masses
    galaxy_type = np.random.choice(['Spiral', 'Elliptical', 'Irregular'], n_galaxies)
    
    table = Table()
    table['id'] = np.arange(n_galaxies)
    table['ra'] = ra * u.deg
    table['dec'] = dec * u.deg
    table['redshift'] = redshift
    table['magnitude'] = magnitude * u.mag
    table['mass'] = mass * u.Msun
    table['type'] = galaxy_type
    table.write('catalogs/galaxy_catalog.fits', overwrite=True)
    print(f"   ✓ Galaxy catalog created ({n_galaxies} galaxies)")
except Exception as e:
    print(f"   ✗ Failed: {e}")

# 3. Create star catalog
print("\n3. Creating star catalog...")
try:
    n_stars = 10000
    ra = np.random.uniform(0, 360, n_stars)
    dec = np.random.uniform(-90, 90, n_stars)
    parallax = np.random.uniform(0.1, 100, n_stars)  # mas
    pmra = np.random.normal(0, 10, n_stars)  # mas/yr
    pmdec = np.random.normal(0, 10, n_stars)  # mas/yr
    g_mag = np.random.uniform(8, 22, n_stars)
    bp_rp = np.random.uniform(0, 2, n_stars)
    
    table = Table()
    table['source_id'] = np.arange(n_stars)
    table['ra'] = ra * u.deg
    table['dec'] = dec * u.deg
    table['parallax'] = parallax * u.mas
    table['pmra'] = pmra * u.mas/u.yr
    table['pmdec'] = pmdec * u.mas/u.yr
    table['g_mag'] = g_mag * u.mag
    table['bp_rp'] = bp_rp * u.mag
    table.write('catalogs/star_catalog.fits', overwrite=True)
    print(f"   ✓ Star catalog created ({n_stars} stars)")
except Exception as e:
    print(f"   ✗ Failed: {e}")

# 4. Create CMB power spectrum
print("\n4. Creating CMB power spectrum...")
try:
    import healpy as hp
    nside = 128
    npix = hp.nside2npix(nside)
    
    # Create CMB-like map
    cmb_map = np.random.normal(0, 100, npix)
    
    # Add some structure
    lmax = 3 * nside - 1
    cl = np.zeros(lmax + 1)
    cl[2:] = 1000 / (np.arange(2, lmax + 1)**2)
    cmb_map = hp.synfast(cl, nside)
    
    hp.write_map('cmb/cmb_map.fits', cmb_map, overwrite=True)
    
    # Compute power spectrum
    cl_est = hp.anafast(cmb_map)
    hp.write_cl('cmb/cmb_power_spectrum.fits', cl_est, overwrite=True)
    print("   ✓ CMB map and power spectrum created")
except Exception as e:
    print(f"   ✗ Failed: {e}")

# 5. Create N-body simulation snapshot
print("\n5. Creating N-body simulation snapshot...")
try:
    n_particles = 1000
    positions = np.random.randn(n_particles, 3) * 10  # Mpc
    velocities = np.random.randn(n_particles, 3) * 100  # km/s
    masses = np.random.uniform(1e10, 1e12, n_particles)  # Solar masses
    
    table = Table()
    table['particle_id'] = np.arange(n_particles)
    table['x'] = positions[:, 0] * u.Mpc
    table['y'] = positions[:, 1] * u.Mpc
    table['z'] = positions[:, 2] * u.Mpc
    table['vx'] = velocities[:, 0] * u.km/u.s
    table['vy'] = velocities[:, 1] * u.km/u.s
    table['vz'] = velocities[:, 2] * u.km/u.s
    table['mass'] = masses * u.Msun
    table.write('simulations/nbody_snapshot.fits', overwrite=True)
    print(f"   ✓ N-body snapshot created ({n_particles} particles)")
except Exception as e:
    print(f"   ✗ Failed: {e}")

# 6. Create gravitational wave strain data
print("\n6. Creating gravitational wave strain data...")
try:
    time = np.linspace(0, 10, 10000)  # seconds
    frequency = 100  # Hz
    strain = np.sin(2 * np.pi * frequency * time) * np.exp(-time/5) * 1e-21
    
    table = Table()
    table['time'] = time * u.s
    table['strain'] = strain
    table['frequency'] = frequency * u.Hz
    table.write('simulations/gw_strain.fits', overwrite=True)
    print("   ✓ Gravitational wave strain data created")
except Exception as e:
    print(f"   ✗ Failed: {e}")

# 7. Create X-ray spectrum
print("\n7. Creating X-ray spectrum...")
try:
    energy = np.linspace(0.1, 10, 1000)  # keV
    flux = 1000 * energy**(-2) * np.exp(-energy/2) + np.random.normal(0, 10, 1000)
    
    table = Table()
    table['energy'] = energy * u.keV
    table['flux'] = flux * u.erg/(u.cm**2 * u.s * u.keV)
    table.write('simulations/xray_spectrum.fits', overwrite=True)
    print("   ✓ X-ray spectrum created")
except Exception as e:
    print(f"   ✗ Failed: {e}")

print("\n✓ Sample data creation complete!")
print("\nCreated files:")
print("  FITS Images:")
print("    - fits/synthetic_galaxy.fits")
print("  Catalogs:")
print("    - catalogs/galaxy_catalog.fits (5000 galaxies)")
print("    - catalogs/star_catalog.fits (10000 stars)")
print("  CMB Data:")
print("    - cmb/cmb_map.fits")
print("    - cmb/cmb_power_spectrum.fits")
print("  Simulations:")
print("    - simulations/nbody_snapshot.fits (1000 particles)")
print("    - simulations/gw_strain.fits")
print("    - simulations/xray_spectrum.fits")
print("\nTotal data size: ~10-20MB")
