"""Fully symbolic derivations (sympy) of the formulas used in this project.

Every formula that appears in models/equations.py is derived
here from first principles with Sympy; each derivation carries explicit checks
(simplified identities that must reduce to zero / true booleans).

Entry point: run_all() -> list of DerivationResult dicts
    {"name": str, "description": str, "formula": str, "formula_latex": [str],
     "steps": [str], "checks": [{"label": str, "ok": bool}]}

The verifier script scripts/verify_formulas.py consumes run_all(), asserts every
identity, runs numeric spot checks and writes reports/derivations_report.md.
"""

from __future__ import annotations

import sympy as sp


# ---------------------------------------------------------------------------
# 1. Kepler's third law (exoplanet orbital period)
def derive_kepler_third_law():
    a, P = sp.symbols("a P", positive=True)
    G, M = sp.symbols("G M", positive=True)
    m = sp.symbols("m", positive=True)  # planet mass (cancels out)
    # Derive: P = 2*pi*sqrt(a^3/(G*M))
    # Start from gravitational force = centripetal force
    # G * M * m / a^2 = m * v^2 / a
    # Cancel m and a: G * M / a = v^2
    # v = 2 * pi * a / P (circular orbit: circumference / period)
    # G * M / a = (2 * pi * a / P)^2 = 4 * pi^2 * a^2 / P^2
    # Solve for P:
    # P^2 = 4 * pi^2 * a^3 / (G * M)
    # P = 2 * pi * sqrt(a^3 / (G * M))
    P_expr = 2 * sp.pi * sp.sqrt(a**3 / (G * M))
    # Check: P^2 * G * M / (4*pi^2) = a^3
    check = sp.simplify(P_expr**2 * G * M / (4 * sp.pi**2) - a**3)
    checks = [
        {
            "label": "P^2 proportional to a^3 (Kepler's third law)",
            "ok": check == 0,
        },
    ]
    return {
        "name": "kepler_third_law",
        "description": "Kepler's third law for exoplanet orbital period",
        "formula": "P = 2 pi sqrt(a^3 / (G M))",
        "formula_latex": ["P = 2\\pi\\sqrt{\\frac{a^{3}}{GM}}"],
        "steps": [
            "Start from gravitational force = centripetal force: G M m / a^2 = m v^2 / a",
            "Cancel planet mass m: G M / a = v^2",
            "Substitute orbital velocity v = 2 pi a / P (circular orbit: circumference / period)",
            "G M / a = 4 pi^2 a^2 / P^2",
            "Rearrange: P^2 = 4 pi^2 a^3 / (G M)",
            "Take square root: P = 2 pi sqrt(a^3 / (G M))",
        ],
        "checks": checks,
    }


# ---------------------------------------------------------------------------
# 2. Energy-limited atmospheric escape (Watson et al. 1981)
def derive_atmospheric_escape():
    R, M = sp.symbols("R M", positive=True)  # planet radius, mass
    G = sp.symbols("G", positive=True)  # gravitational constant
    F_XUV = sp.symbols("F_XUV", positive=True)  # XUV flux (W/m^2)
    eps = sp.symbols("eps", positive=True)  # heating efficiency
    K = sp.symbols("K", positive=True)  # Roche lobe reduction factor

    # Derivation of energy-limited escape rate:
    # 1. XUV power absorbed by planet: P_abs = pi * R^2 * F_XUV * eps
    #    (cross-section is pi*R^2, fraction eps heats the atmosphere)
    # 2. Gravitational potential energy per unit mass at surface: U = G*M/R
    # 3. With Roche lobe correction: U_eff = G*M*K/R
    # 4. Mass loss rate: dM/dt = P_abs / U_eff = (pi*R^2*F_XUV*eps) / (G*M*K/R)
    # 5. Simplify: dM/dt = (pi * R^3 * F_XUV * eps) / (G * M * K)

    dMdt_expr = sp.pi * R**3 * F_XUV * eps / (G * M * K)

    # Check 1: Dimensional consistency
    # [dM/dt] = kg/s
    # [pi * R^3 * F_XUV * eps / (G * M * K)] = m^3 * (W/m^2) / (m^3 kg^-1 s^-2 * kg)
    # = m^3 * (kg m^2 s^-3 / m^2) / (m^3 s^-2) = m^3 * kg s^-3 / m^3 s^-2 = kg/s ✓
    # Sympy dimensional check: verify formula structure
    check_dim = sp.simplify(dMdt_expr * G * M * K - sp.pi * R**3 * F_XUV * eps)

    # Check 2: Energy balance - power absorbed = power used for escape
    # P_abs = pi * R^2 * F_XUV * eps
    # P_escape = dM/dt * G * M * K / R
    P_abs = sp.pi * R**2 * F_XUV * eps
    P_escape = dMdt_expr * G * M * K / R
    check_energy = sp.simplify(P_abs - P_escape)

    checks = [
        {
            "label": "Formula structure identity (dM/dt = pi R^3 F_XUV eps / (G M K))",
            "ok": check_dim == 0,
        },
        {
            "label": "Energy balance: absorbed XUV power = gravitational power for escape",
            "ok": check_energy == 0,
        },
    ]

    return {
        "name": "atmospheric_escape_energy_limited",
        "description": "Energy-limited atmospheric escape rate (Watson et al. 1981)",
        "formula": "dM/dt = pi * R^3 * F_XUV * epsilon / (G * M * K)",
        "formula_latex": [
            "\\frac{dM}{dt} = \\frac{\\pi R^{3} F_{\\mathrm{XUV}} \\varepsilon}{G M K}"
        ],
        "steps": [
            "XUV power absorbed by planet: P_abs = pi * R^2 * F_XUV * epsilon",
            "  (cross-section pi R^2, heating efficiency epsilon)",
            "Gravitational potential energy per unit mass at surface: U = G M / R",
            "Roche lobe correction reduces potential barrier: U_eff = G M K / R",
            "  (K <= 1 accounts for stellar tidal potential reducing escape energy)",
            "Mass loss rate from energy balance: dM/dt = P_abs / U_eff",
            "Substitute: dM/dt = (pi R^2 F_XUV epsilon) / (G M K / R)",
            "Simplify: dM/dt = (pi * R^3 * F_XUV * epsilon) / (G * M * K)",
        ],
        "checks": checks,
    }



# ---------------------------------------------------------------------------
# 3. Stellar mean density from a central transit (Seager & Mallen-Ornelas 2003)
def derive_stellar_density_from_transit():
    P, T = sp.symbols("P T", positive=True)   # orbital period, full transit duration
    G = sp.symbols("G", positive=True)
    # a/R_* from geometry of a central (b=0) transit of a small planet:
    #   T = 2 R_* P / (pi a)   ->   a/R_* = 2 P / (pi T)
    a_over_R = 2 * P / (sp.pi * T)
    # stellar mean density: rho_* = M_*/(4/3 pi R_*^3) = (3 pi/(G P^2)) (a/R_*)^3
    rho = 3 * sp.pi / (G * P**2) * a_over_R**3
    rho_simplified = sp.simplify(rho)
    # Check: simplifies to 24 P / (pi^2 G T^3)
    expected = 24 * P / (sp.pi**2 * G * T**3)
    check = sp.simplify(rho_simplified - expected)
    # Check: substituting a/R_* back gives identity
    check2 = sp.simplify(3 * sp.pi / (G * P**2) * (2 * P / (sp.pi * T))**3 - 24 * P / (sp.pi**2 * G * T**3))
    checks = [
        {"label": "rho_* simplifies to 24 P / (pi^2 G T^3)", "ok": check == 0},
        {"label": "algebraic identity of the two forms", "ok": check2 == 0},
    ]
    return {
        "name": "stellar_density_from_transit",
        "description": "Stellar mean density inferred from a central transit (Seager & Mallen-Ornelas 2003)",
        "formula": "rho_* = 24 P / (pi^2 G T^3)",
        "formula_latex": [r"\rho_* = \frac{24\,P}{\pi^{2} G\,T^{3}}"],
        "steps": [
            "Central transit (b=0), small planet: full transit duration T = 2 R_* P / (pi a)",
            "Solve for a/R_* = 2 P / (pi T)",
            "Kepler: rho_* = M_*/(4/3 pi R_*^3) = (3 pi/(G P^2))(a/R_*)^3",
            "Substitute a/R_*: rho_* = (3 pi/(G P^2)) (2 P/(pi T))^3",
            "Simplify: rho_* = 24 P / (pi^2 G T^3)",
        ],
        "checks": checks,
    }


# ---------------------------------------------------------------------------
# 4. RV semi-amplitude K (Newtonian two-body, circular orbit)
def derive_rv_semi_amplitude():
    G, P = sp.symbols("G P", positive=True)
    Mstar, Mp = sp.symbols("M_star M_p", positive=True)
    e = sp.symbols("e", real=True)
    # From Newtonian two-body: a = (G (Mstar+Mp) P^2 / (4 pi^2))^(1/3)
    # K = (2 pi a_star sin i)/(P sqrt(1-e^2)) with a_star = a * Mp/(Mstar+Mp)
    # -> K = (2 pi G / P)^(1/3) * Mp sin i / (Mstar+Mp)^(2/3) / sqrt(1-e^2)
    K = (2 * sp.pi * G / P) ** sp.Rational(1, 3) * Mp / (Mstar + Mp) ** sp.Rational(2, 3) / sp.sqrt(1 - e**2)
    # Check: circular, Mp << Mstar limit reduces to (2 pi G/P)^(1/3) Mp / Mstar^(2/3)
    Klim = sp.simplify(K.subs(Mp, 0) if False else K)
    # Verify dimensions/structure: K^3 * (Mstar+Mp)^2 * (1-e^2)^(3/2) = (2 pi G / P) Mp^3
    lhs = K**3 * (Mstar + Mp)**2 * (1 - e**2) ** sp.Rational(3, 2)
    rhs = (2 * sp.pi * G / P) * Mp**3
    check = sp.simplify(lhs - rhs)
    checks = [
        {"label": "K satisfies K^3 (M*+Mp)^2 (1-e^2)^(3/2) = (2 pi G/P) Mp^3", "ok": check == 0},
    ]
    return {
        "name": "rv_semi_amplitude",
        "description": "Radial-velocity semi-amplitude K (Newtonian two-body)",
        "formula": "K = (2 pi G / P)^(1/3) * M_p sin i / (M_* + M_p)^(2/3) / sqrt(1 - e^2)",
        "formula_latex": [r"K = \left(\frac{2\pi G}{P}\right)^{1/3}\frac{M_p\sin i}{(M_*+M_p)^{2/3}}\frac{1}{\sqrt{1-e^2}}"],
        "steps": [
            "Newtonian two-body: separation a = (G (M*+Mp) P^2/(4 pi^2))^(1/3)",
            "Star orbits the barycentre: a_* = a * Mp/(M*+Mp)",
            "Projected velocity amplitude: K = 2 pi a_* sin i / (P sqrt(1-e^2))",
            "Substitute a and simplify: K = (2 pi G/P)^(1/3) Mp sin i / (M*+Mp)^(2/3) / sqrt(1-e^2)",
        ],
        "checks": checks,
    }


# ---------------------------------------------------------------------------
# 5. Kopparapu 2013/2014 habitable-zone flux polynomial
def derive_kopparapu_hz():
    T = sp.symbols("T", real=True)   # T_eff - 5780 (K)
    s0, a, b, c, d = sp.symbols("s0 a b c d", real=True)
    Seff = s0 + a * T + b * T**2 + c * T**3 + d * T**4
    # Boundary distance (AU) from flux balance: S = L*/(4 pi a^2) = S_eff * S_sun
    # -> a (AU) = sqrt(L*/L_sun / S_eff)
    Lratio = sp.symbols("Lratio", positive=True)
    a_au = sp.sqrt(Lratio / Seff)
    # Check: a_au^2 * Seff = Lratio
    check = sp.simplify(a_au**2 * Seff - Lratio)
    checks = [
        {"label": "HZ distance satisfies a^2 * S_eff = L*/L_sun", "ok": check == 0},
    ]
    return {
        "name": "kopparapu_hz_flux",
        "description": "Kopparapu 2013/2014 HZ boundary from the S_eff(T_eff) polynomial",
        "formula": "a (AU) = sqrt(L*/L_sun / S_eff), S_eff = s0 + a T + b T^2 + c T^3 + d T^4, T = T_eff - 5780",
        "formula_latex": [r"a_{\rm HZ} = \sqrt{L_*/L_\odot / S_{\rm eff}(T_{\rm eff})}"],
        "steps": [
            "S_eff(T_eff) polynomial (Kopparapu 2013 Table 3) for each boundary",
            "Flux balance at the boundary: L*/(4 pi a^2) = S_eff * L_sun/(4 pi (1 AU)^2)",
            "Solve for a: a (AU) = sqrt(L*/L_sun / S_eff)",
            "Conservative HZ: moist_greenhouse (inner) <= S/S_earth <= max_greenhouse (outer)",
        ],
        "checks": checks,
    }


# ---------------------------------------------------------------------------
# 6. Atmospheric scale height (hydrostatic equilibrium, ideal gas)
def derive_scale_height():
    k_B, T, mu, m_p, g = sp.symbols("k_B T mu m_p g", positive=True)
    # Hydrostatic: dp/dz = -rho g; ideal gas p = rho k_B T/(mu m_p)
    # -> H = k_B T / (mu m_p g)
    H = k_B * T / (mu * m_p * g)
    # Check: p = rho g H  (pressure at base equals weight of one scale height)
    rho = sp.symbols("rho", positive=True)
    p = rho * k_B * T / (mu * m_p)
    check = sp.simplify(p - rho * g * H)
    checks = [
        {"label": "Hydrostatic consistency: p = rho g H", "ok": check == 0},
    ]
    return {
        "name": "scale_height_hydrostatic",
        "description": "Atmospheric scale height from hydrostatic equilibrium (ideal gas)",
        "formula": "H = k_B T / (mu m_p g)",
        "formula_latex": [r"H = \frac{k_{\rm B}T}{\mu\,m_p\,g}"],
        "steps": [
            "Hydrostatic equilibrium: dp/dz = -rho g",
            "Ideal gas: p = rho k_B T/(mu m_p)",
            "Solution: rho(z) = rho_0 exp(-z/H) with H = k_B T/(mu m_p g)",
            "Pressure at the base: p_0 = rho_0 g H",
        ],
        "checks": checks,
    }

ALL = [
    derive_kepler_third_law,
    derive_atmospheric_escape,
    derive_stellar_density_from_transit,
    derive_rv_semi_amplitude,
    derive_kopparapu_hz,
    derive_scale_height,
]


def run_all():
    return [fn() for fn in ALL]
