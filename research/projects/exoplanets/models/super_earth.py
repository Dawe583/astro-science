"""Super-Earth habitability and atmospheric oxygen models.

All functions use SI units unless noted. Derived quantities are labeled
'model-derived' (not observed). Based on Kopparapu et al. 2013/2014,
Seager et al. 2013, Luger & Barnes 2015, Meadows et al. 2018.
"""

from __future__ import annotations

import numpy as np

# Constants
G = 6.67430e-11
M_SUN = 1.98847e30
R_SUN = 6.957e8
M_EARTH = 5.972e24
R_EARTH = 6.371e6
AU = 1.495978707e11
L_SUN = 3.828e26
K_B = 1.380649e-23
M_PROTON = 1.6726219e-27
SIGMA_SB = 5.670374419e-8
DAY = 86400.0


def hz_boundaries_kopparapu(L_star_W, T_eff_K):
    """Habitable zone boundaries (AU) per Kopparapu et al. 2013.

    Returns dict: recent_venus, runaway_greenhouse, moist_greenhouse,
    max_greenhouse, early_mars, (conservative inner=moist, outer=max).
    """
    coeffs = {
        "recent_venus": (1.776, 1.4335e-4, 3.3954e-9, -7.6364e-12, -1.1950e-15),
        "runaway_greenhouse": (1.107, 1.332e-4, 1.580e-8, -8.308e-12, -1.931e-15),
        "moist_greenhouse": (1.014, 8.18e-5, 1.93e-9, -4.34e-12, -6.68e-16),
        "max_greenhouse": (0.356, 6.171e-5, 1.698e-9, -3.198e-12, -5.575e-16),
        "early_mars": (0.320, 5.547e-5, 1.526e-9, -2.874e-12, -5.011e-16),
    }
    T = T_eff_K - 5780.0
    result = {}
    for name, (s0, a, b, c, d) in coeffs.items():
        seff = s0 + a * T + b * T**2 + c * T**3 + d * T**4
        result[name] = float(np.sqrt(L_star_W / L_SUN / seff))
    return result


def equilibrium_temp(T_star, R_star, a, albedo=0.3, greenhouse=0.0):
    """Equilibrium temperature (K) with optional greenhouse warming (K)."""
    teq = T_star * np.sqrt(R_star / (2 * a)) * (1 - albedo) ** 0.25
    return float(teq + greenhouse)


def greenhouse_warming(co2_bar, h2o_bar=0.0):
    """Approximate greenhouse warming (K) from CO2 and H2O partial pressures (bar).

    Simplified: delta_T ~ 10 * ln(1 + CO2) + 5 * ln(1 + H2O) (empirical fit).
    """
    return 10.0 * np.log1p(co2_bar) + 5.0 * np.log1p(h2o_bar)


def jeans_escape_param(M_kg, R_m, T_K, m_mol_kg):
    """Jeans escape parameter: lambda = GMm/(kT R) = v_esc^2 / v_th^2.

    lambda > ~3-5 means atmosphere retained over geological timescales.
    """
    v_esc = np.sqrt(2 * G * M_kg / R_m)
    v_th = np.sqrt(2 * K_B * T_K / m_mol_kg)
    return float((v_esc / v_th) ** 2)


def atmospheric_retention(M_earth, R_earth, T_eq, species="O2"):
    """Check if a species is retained over 4.5 Gyr.

    Species: O2, N2, H2O, H2, He, CO2, CH4
    Returns dict with Jeans parameter and retention flag.
    """
    mol_masses = {"O2": 32, "N2": 28, "H2O": 18, "H2": 2, "He": 4, "CO2": 44, "CH4": 16}
    mu = mol_masses.get(species, 28)
    m_mol = mu * M_PROTON
    lam = jeans_escape_param(M_earth * M_EARTH, R_earth * R_EARTH, T_eq, m_mol)
    # Retention criterion: lambda > 3 for geological timescale
    retained = lam > 3.0
    return {"species": species, "jeans_lambda": lam, "retained": retained}


def oxygen_biosignature_strength(N_O2_cm2, N_O3_cm2=None):
    """Approximate O2/O3 absorption depth (dimensionless) for transmission spectroscopy.

    O2 A-band at 0.76 um: cross-section ~ 1e-23 cm^2
    O3 Hartley band at 0.25 um: cross-section ~ 1e-17 cm^2
    Returns estimated transit depth variation.
    """
    sigma_O2 = 1e-23  # cm^2
    depth_O2 = N_O2_cm2 * sigma_O2
    result = {"O2_depth": float(depth_O2)}
    if N_O3_cm2 is not None:
        sigma_O3 = 1e-17
        result["O3_depth"] = float(N_O3_cm2 * sigma_O3)
    return result


def rayleigh_scattering_slope(R_p_m, H_m, R_star_m):
    """Rayleigh scattering slope in transit depth vs wavelength (dimensionless).

    alpha = 4 * H / R_p (for Rayleigh, transit depth ~ lambda^-4)
    """
    return 4.0 * H_m / R_p_m


def surface_temp_with_greenhouse(T_eq, co2_bar, h2o_bar=0.0):
    """Surface temperature (K) = Teq + greenhouse warming."""
    return T_eq + greenhouse_warming(co2_bar, h2o_bar)


def water_loss_timescale(M_earth, R_earth, F_XUV, epsilon=0.15):
    """Energy-limited water loss timescale (Gyr) for a planet.

    Assumes Earth-like water inventory (1.4e21 kg). Uses energy-limited escape.
    """
    water_inventory = 1.4e21  # kg (Earth ocean mass)
    R_m = R_earth * R_EARTH
    M_kg = M_earth * M_EARTH
    rate = (np.pi * R_m**3 * F_XUV * epsilon) / (G * M_kg * 1.0)
    if rate <= 0:
        return float("inf")
    return water_inventory / rate / 1e9 / 3.15576e7  # Gyr


def tidal_locking_timescale(a_m, M_star_kg, M_p_kg, R_p_m, k2=0.3, Q=100):
    """Tidal locking timescale (Gyr) for a planet.

    tau = (a^6 * Q * omega) / (3 * k2 * G * M_star^2 * R_p^5) * ...
    Simplified: tau ~ 1 Gyr * (a/AU)^6 * (M_star/Msun)^-2 * (R_p/Re)^-5
    """
    tau_yr = 1e9 * (a_m / AU) ** 6 * (M_SUN / M_star_kg) ** 2 * (R_EARTH / R_p_m) ** 5
    return tau_yr / 1e9  # Gyr


def biosignature_detectability(SNR, depth, n_transits):
    """Approximate biosignature detectability.

    Detectable if SNR * sqrt(n_transits) * depth > 5 (5-sigma).
    """
    return SNR * np.sqrt(n_transits) * depth > 5.0


if __name__ == "__main__":
    # Sanity checks
    hz = hz_boundaries_kopparapu(L_SUN, 5778)
    print("Sun HZ (AU):", {k: round(v, 3) for k, v in hz.items()})
    print("Earth Teq:", round(equilibrium_temp(5778, R_SUN, AU), 1), "K")
    print(
        "Earth surface temp (greenhouse):",
        round(surface_temp_with_greenhouse(255, 0.0004, 0.01), 1),
        "K",
    )
    print("O2 retention (Earth):", atmospheric_retention(1.0, 1.0, 288, "O2"))
    print("H2 retention (Earth):", atmospheric_retention(1.0, 1.0, 288, "H2"))
    print("O2 biosignature depth:", oxygen_biosignature_strength(1e21))
    print(
        "Water loss (Earth, F_XUV=0.001):",
        round(water_loss_timescale(1.0, 1.0, 0.001), 1),
        "Gyr",
    )
    print(
        "Tidal lock (Earth):",
        round(tidal_locking_timescale(AU, M_SUN, M_EARTH, R_EARTH), 1),
        "Gyr",
    )
