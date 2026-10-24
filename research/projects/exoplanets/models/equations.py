"""Exoplanet physical models and equations.

All functions use SI units unless noted. Constants are explicit.
"""

from __future__ import annotations

import numpy as np

# Constants
G = 6.67430e-11       # m^3 kg^-1 s^-2
M_SUN = 1.98847e30     # kg
R_SUN = 6.957e8        # m
M_EARTH = 5.972e24     # kg
R_EARTH = 6.371e6      # m
AU = 1.495978707e11    # m
L_SUN = 3.828e26       # W
K_B = 1.380649e-23     # J/K
M_PROTON = 1.6726219e-27  # kg
SIGMA_SB = 5.670374419e-8  # W m^-2 K^-4
DAY = 86400.0          # s


def kepler_period(a_m: float, M_star_kg: float) -> float:
    """Orbital period (s) for semi-major axis a (m) and stellar mass (kg)."""
    return 2 * np.pi * np.sqrt(a_m**3 / (G * M_star_kg))


def kepler_semi_major_axis(P_s: float, M_star_kg: float) -> float:
    """Semi-major axis (m) from period (s) and stellar mass (kg)."""
    return ((G * M_star_kg * P_s**2) / (4 * np.pi**2)) ** (1.0 / 3.0)


def transit_depth(R_p_m: float, R_star_m: float) -> float:
    """Transit depth (dimensionless) = (R_p/R_*)^2."""
    return (R_p_m / R_star_m) ** 2


def transit_duration(P_s: float, R_star_m: float, a_m: float, b: float = 0.0) -> float:
    """Transit duration (s) for impact parameter b."""
    return (P_s / np.pi) * (R_star_m / a_m) * np.sqrt(1 - b**2)


def habitable_zone_distances(L_star_W: float, T_eff_K: float) -> dict:
    """Conservative and optimistic HZ boundaries (AU) per Kopparapu et al. 2013.

    Returns dict with keys: recent_venus, runaway_greenhouse, moist_greenhouse,
    max_greenhouse, early_mars (in AU).
    """
    # S_eff coefficients (Kopparapu 2013, Table 3, for Earth-like planet)
    # S_eff = S0 + a*T + b*T^2 + c*T^3 + d*T^4, T = T_eff - 5780
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
        dist_au = np.sqrt(L_star_W / L_SUN / seff)
        result[name] = float(dist_au)
    return result


def tidal_heating_power(M_p_kg: float, R_p_m: float, a_m: float, e: float,
                        k2: float = 0.3, Q: float = 100.0, M_star_kg: float = M_SUN) -> float:
    """Tidal heating power (W) for a planet in eccentric orbit.

    Simplified formula: P = (21/2) * k2 * G * M_star^2 * R_p^5 * n * e^2 / (a^6 * Q)
    where n = 2*pi/P is the mean motion.
    """
    n = 2 * np.pi / (2 * np.pi * np.sqrt(a_m**3 / (G * M_star_kg)))  # mean motion
    P = (21.0 / 2.0) * k2 * G * M_star_kg**2 * R_p_m**5 * n * e**2 / (a_m**6 * Q)
    return float(P)


def jeans_escape_parameter(v_esc_ms: float, v_th_ms: float) -> float:
    """Jeans escape parameter lambda = v_esc^2 / v_th^2."""
    return (v_esc_ms / v_th_ms) ** 2


def thermal_velocity(T_K: float, m_kg: float) -> float:
    """Most probable thermal speed (m/s) for mass m at temperature T."""
    return np.sqrt(2 * K_B * T_K / m_kg)


def escape_velocity(M_kg: float, R_m: float) -> float:
    """Escape velocity (m/s)."""
    return np.sqrt(2 * G * M_kg / R_m)


def scale_height(T_K: float, mu: float, g_ms2: float) -> float:
    """Atmospheric scale height (m). mu = mean molecular weight (dimensionless)."""
    return K_B * T_K / (mu * M_PROTON * g_ms2)


def transmission_depth(R_p_m: float, H_m: float, R_star_m: float) -> float:
    """Transit depth variation due to atmosphere (dimensionless)."""
    return 2 * R_p_m * H_m / R_star_m**2


def mass_radius_rocky(M_earth: float) -> float:
    """Rocky planet radius (Earth radii) from mass (Earth masses). Zeng et al. 2016."""
    return float(M_earth ** 0.28)


def equilibrium_temperature(T_star_K: float, R_star_m: float, a_m: float,
                           albedo: float = 0.3) -> float:
    """Equilibrium temperature (K) for a planet at distance a from star."""
    return T_star_K * np.sqrt(R_star_m / (2 * a_m)) * (1 - albedo) ** 0.25


def roche_limit(M_star_kg: float, rho_planet_kgm3: float) -> float:
    """Roche limit (m) for a planet of density rho around star of mass M."""
    return 2.44 * (M_star_kg / (4.0 / 3.0 * np.pi * rho_planet_kgm3)) ** (1.0 / 3.0)


def hill_radius(a_m: float, M_p_kg: float, M_star_kg: float) -> float:
    """Hill radius (m)."""
    return a_m * (M_p_kg / (3 * M_star_kg)) ** (1.0 / 3.0)


def orbital_velocity(a_m: float, M_star_kg: float) -> float:
    """Circular orbital velocity (m/s)."""
    return np.sqrt(G * M_star_kg / a_m)


def density(M_kg: float, R_m: float) -> float:
    """Mean density (kg/m^3)."""
    return M_kg / (4.0 / 3.0 * np.pi * R_m**3)

def surface_gravity(M_kg: float, R_m: float) -> float:
    """Surface gravity (m s^-2) from mass and radius: g = G*M/R^2."""
    return G * M_kg / R_m**2


if __name__ == "__main__":
    # Quick sanity checks
    print("Earth transit depth (Sun): %.2e" % transit_depth(R_EARTH, R_SUN))
    print("Earth equilibrium temp: %.1f K" % equilibrium_temperature(5778, R_SUN, AU))
    print("HZ (Sun):", {k: round(v, 3) for k, v in habitable_zone_distances(L_SUN, 5778).items()})
    print("Rocky radius for 5 Mearth: %.2f Rearth" % mass_radius_rocky(5))
    print("Scale height (Earth, 288K, mu=29): %.1f km" % (scale_height(288, 29, 9.81) / 1000))
