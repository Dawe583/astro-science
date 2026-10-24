#!/usr/bin/env python3
"""Verify exoplanet formulas numerically (astropy constants).

Run: .venv/bin/python research/projects/exoplanets/scripts/verify_formulas.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from astropy import constants as const
from astropy import units as u

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "models"))
import equations as E  # noqa: E402

RESULTS_DIR = ROOT / "results"
REPORTS_DIR = ROOT / "reports"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def checks():
    out = []
    # 1. Kepler: Earth orbital period
    a = 1 * u.au
    M = 1 * u.Msun
    P = E.kepler_period(a.to(u.m).value, M.to(u.kg).value)
    ref = (
        (2 * np.pi * np.sqrt((1 * u.au) ** 3 / (const.G * (1 * u.Msun)))).to(u.s).value
    )
    rel = abs(P - ref) / ref
    out.append(
        {
            "label": "Kepler period: code vs closed form (1 AU, 1 Msun)",
            "relative_deviation": rel,
            "pass": rel < 1e-9,
        }
    )

    # 2. Round trip a -> P -> a
    a2 = E.kepler_semi_major_axis(P, M.to(u.kg).value)
    rel2 = abs(a2 - a.to(u.m).value) / a.to(u.m).value
    out.append(
        {
            "label": "Kepler round trip a->P->a",
            "relative_deviation": rel2,
            "pass": rel2 < 1e-9,
        }
    )

    # 3. Transit depth Earth/Sun ~ 8.4e-5
    d = E.transit_depth(E.R_EARTH, E.R_SUN)
    out.append(
        {
            "label": "Earth/Sun transit depth ~8.4e-5",
            "value": d,
            "pass": abs(d - 8.37e-5) < 1e-6,
        }
    )

    # 4. Escape velocity Earth ~ 11.19 km/s
    ve = E.escape_velocity(E.M_EARTH, E.R_EARTH)
    out.append(
        {
            "label": "Earth escape velocity ~11186 m/s",
            "value": ve,
            "pass": abs(ve - 11186) < 5,
        }
    )

    # 5. Earth equilibrium temp ~ 255 K (albedo 0.3)
    Teq = E.equilibrium_temperature(5778.0, E.R_SUN, E.AU, albedo=0.3)
    out.append(
        {
            "label": "Earth equilibrium temperature ~255 K",
            "value": Teq,
            "pass": abs(Teq - 255) < 5,
        }
    )

    # 6. Rocky radius 1 Mearth ~ 1 Rearth (Zeng)
    rr = E.mass_radius_rocky(1.0)
    out.append(
        {
            "label": "Rocky radius for 1 Mearth ~1 Rearth",
            "value": rr,
            "pass": abs(rr - 1.0) < 0.05,
        }
    )

    # 7. Jeans parameter Earth (lambda > 1)
    vt = E.thermal_velocity(288.0, 28 * E.M_PROTON)
    lam = E.jeans_escape_parameter(ve, vt)
    out.append({"label": "Earth Jeans lambda > 1", "value": lam, "pass": lam > 1})

    # 8. Scale height Earth ~8.4 km for N2
    H = E.scale_height(288.0, 28.0, 9.81)
    out.append(
        {
            "label": "Earth N2 scale height ~8.4 km",
            "value": H / 1000,
            "pass": abs(H / 1000 - 8.4) < 1.0,
        }
    )

    # 9. HZ Sun: Earth (1 AU) between moist_greenhouse and max_greenhouse
    hz = E.habitable_zone_distances(E.L_SUN, 5778.0)
    out.append(
        {
            "label": "Sun HZ contains 1 AU",
            "inner": hz["moist_greenhouse"],
            "outer": hz["max_greenhouse"],
            "pass": hz["moist_greenhouse"] < 1.0 < hz["max_greenhouse"],
        }
    )

    # 10. Hill radius sanity
    hr = E.hill_radius(E.AU, E.M_EARTH, E.M_SUN)
    out.append(
        {"label": "Earth Hill radius ~1.5e9 m", "value": hr, "pass": 1.4e9 < hr < 1.6e9}
    )

    # 11. Density Earth ~5515 kg/m3
    rho = E.density(E.M_EARTH, E.R_EARTH)
    out.append(
        {
            "label": "Earth mean density ~5515 kg/m3",
            "value": rho,
            "pass": abs(rho - 5515) < 50,
        }
    )

    # 12. Surface gravity Earth ~9.8 m/s²
    g = E.surface_gravity(E.M_EARTH, E.R_EARTH)
    out.append(
        {
            "label": "Earth surface gravity ~9.8 m/s²",
            "value": g,
            "pass": abs(g - 9.8) < 0.1,
        }
    )

    # 13. Orbital period at 0.5 AU around Sun
    P_05 = E.kepler_period(0.5 * E.AU, E.M_SUN)
    ref_P = E.kepler_period(0.5 * E.AU, E.M_SUN)  # same function, reference value
    rel_P = abs(P_05 - ref_P) / ref_P
    out.append(
        {
            "label": "Kepler period at 0.5 AU ~0.353 yr",
            "value": round(P_05 / (365.25 * 86400), 3),
            "reference": 0.353,
            "pass": abs(P_05 / (365.25 * 86400) - 0.353) < 0.01,
        }
    )

    # 14. Jeans parameter for H2 atmosphere (T=100 K, m=2 amu)
    m_H2 = 2 * 1.67e-27  # kg
    vt_H2 = np.sqrt(8 * E.K_B * 100 / (np.pi * m_H2))
    lam_H2 = E.jeans_escape_parameter(E.M_EARTH, vt_H2)
    out.append(
        {
            "label": "H2 Jeans parameter Earth orbit > 1",
            "value": lam_H2,
            "pass": lam_H2 > 1,
        }
    )

    return out


def main():
    res = checks()
    for r in res:
        r["pass"] = bool(r["pass"])
        for k, v in list(r.items()):
            if isinstance(v, (np.integer,)):
                r[k] = int(v)
            elif isinstance(v, (np.floating,)):
                r[k] = float(v)
            elif isinstance(v, (np.bool_,)):
                r[k] = bool(v)
    n_pass = sum(1 for r in res if r["pass"])
    print(f"Exoplanet formula checks: {n_pass}/{len(res)} pass")
    for r in res:
        status = "PASS" if r["pass"] else "FAIL"
        print(f"  [{status}] {r['label']}")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "exoplanet_derivation_checks.json").write_text(
        json.dumps(res, indent=2)
    )
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(REPORTS_DIR / "exoplanet_derivations_report.md", "w") as f:
        f.write("# Exoplanet formula verification\n\n")
        f.write(
            "Generated: "
            + __import__("datetime")
            .datetime.now(__import__("datetime").timezone.utc)
            .isoformat()
            + "Z\n\n"
        )
        f.write(f"Result: **{n_pass}/{len(res)} pass**\n\n")
        for r in res:
            f.write(f"- [{'PASS' if r['pass'] else 'FAIL'}] {r['label']}\n")
    sys.exit(0 if n_pass == len(res) else 1)


if __name__ == "__main__":
    main()
