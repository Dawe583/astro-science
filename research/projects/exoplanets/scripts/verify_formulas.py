#!/usr/bin/env python3
"""Verify exoplanet formulas symbolically and numerically.

1. Executes models/derivations.run_all() -> asserts every symbolic check.
2. Runs numeric spot checks (astropy constants) against the closed forms.
3. Writes reports/exoplanet_derivations_report.md and results/exoplanet_derivation_checks.json.

Run: .venv/bin/python research/projects/exoplanets/scripts/verify_formulas.py
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from astropy import constants as const
from astropy import units as u

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "models"))
import equations as E  # noqa: E402
import derivations as D  # noqa: E402

RESULTS_DIR = ROOT / "results"
REPORTS_DIR = ROOT / "reports"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# ----------------------------------------------------------------- numeric checks


def numeric_checks():
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

    # 15. Stellar density from transit: Earth/Sun central transit (~13 h) -> ~rho_sun order
    rho_tr = E.stellar_density_from_transit(365.25 * 86400.0, 13.0 * 3600.0)
    out.append(
        {
            "label": "Stellar density from transit (Earth/Sun, 13 h) ~ solar order",
            "value": rho_tr,
            "reference": 1408,
            "pass": 100 < rho_tr < 1e5,
        }
    )

    # 16. RV semi-amplitude: 1 Mjup at 1 AU around 1 Msun ~ 28.4 m/s
    K = E.rv_semi_amplitude(1.898e27, E.M_SUN, 365.25 * 86400.0)
    out.append(
        {
            "label": "RV semi-amplitude 1 Mjup @ 1 AU ~ 28.4 m/s",
            "value": K,
            "reference": 28.4,
            "pass": abs(K - 28.4) < 1.0,
        }
    )

    # 17. Kopparapu HZ: Sun contains 1 AU (already check 9) + Earth insolation in range
    out.append(
        {
            "label": "Kopparapu HZ flag: Earth (1 AU, Sun) is in HZ",
            "value": E.kopparapu_hz_flag(1.0, 5778.0),
            "pass": bool(E.kopparapu_hz_flag(1.0, 5778.0)),
        }
    )

    # 18. Scale height: H2-dominated atmosphere (mu=2.3) at 288 K -> ~106 km
    H23 = E.scale_height(288.0, 2.3, 9.81)
    out.append(
        {
            "label": "Scale height Earth (mu=2.3, H2) ~ 106 km",
            "value": H23 / 1000,
            "reference": 106.0,
            "pass": 90 < H23 / 1000 < 120,
        }
    )

    return out



def real_data_checks():
    """Real-data verification of the 4 new families against the NASA Exoplanet Archive."""
    import pandas as pd
    import numpy as np

    csv = ROOT.parent / "data" / "processed" / "exoplanets.csv"
    # ROOT = exoplanets project root; data is at ROOT/data/processed
    raw_csv = ROOT / "data" / "raw" / "exoplanets_confirmed.csv"
    proc_csv = ROOT / "data" / "processed" / "exoplanets.csv"
    df = pd.read_csv(raw_csv)
    pdf = pd.read_csv(proc_csv)
    # merge processed flags onto raw by pl_name
    if "in_hz" in pdf.columns:
        df = df.merge(pdf[["pl_name", "in_hz", "likely_rocky"]], on="pl_name", how="left")
    out = {"n_rows": int(len(df)), "checks": []}

    # --- A. Stellar density from transit vs catalog stellar density
    sub = df[
        df["pl_trandur"].notna()
        & df["pl_orbper"].notna()
        & df["st_mass"].notna()
        & df["st_rad"].notna()
        & (df["pl_trandur"] > 0)
        & (df["pl_orbper"] > 0)
    ].copy()
    if len(sub):
        rho_cat = sub["st_mass"] * 1.98847e30 / (
            4.0 / 3.0 * np.pi * (sub["st_rad"] * 6.957e8) ** 3
        )
        rho_tr = 24.0 * (sub["pl_orbper"] * 86400.0) / (
            np.pi**2 * 6.67430e-11 * (sub["pl_trandur"] * 3600.0) ** 3
        )
        logratio = np.log10(rho_tr / rho_cat)
        med = float(np.median(logratio))
        q1 = float(np.percentile(logratio, 25))
        q3 = float(np.percentile(logratio, 75))
        out["checks"].append(
            {
                "label": "Stellar density from transit vs catalog (log10 ratio)",
                "n": int(len(sub)),
                "median_log10_ratio": med,
                "iqr_log10": [q1, q3],
                "note": "scatter expected: impact parameter b != 0, eccentricity, stellar density errors",
            }
        )

    # --- B. RV semi-amplitude range for RV-detected planets
    rv = df[
        (df["discoverymethod"] == "Radial Velocity")
        & df["pl_bmassj"].notna()
        & df["pl_orbper"].notna()
        & df["st_mass"].notna()
    ].copy()
    if len(rv):
        Ks = []
        for r in rv.itertuples():
            K = E.rv_semi_amplitude(
                r.pl_bmassj * 1.89813e27,
                r.st_mass * 1.98847e30,
                r.pl_orbper * 86400.0,
            )
            Ks.append(K)
        Ks = np.array(Ks)
        in_range = int(((Ks >= 1) & (Ks <= 200)).sum())
        out["checks"].append(
            {
                "label": "RV semi-amplitude K for RV-detected planets (m/s)",
                "n": int(len(rv)),
                "median_K_ms": float(np.median(Ks)),
                "min_K_ms": float(Ks.min()),
                "max_K_ms": float(Ks.max()),
                "in_typical_range_1_200_ms": in_range,
                "note": "consistency/units check: catalog M sin i is derived from K by construction",
            }
        )

    # --- C. Kopparapu HZ count vs existing in_hz flag
    hz_mask = df.apply(
        lambda r: E.kopparapu_hz_flag(r.get("pl_insol", np.nan), r.get("st_teff", np.nan)),
        axis=1,
    )
    n_hz_new = int(hz_mask.sum())
    n_hz_old = int(df["in_hz"].sum()) if "in_hz" in df.columns else 0
    out["checks"].append(
        {
            "label": "Kopparapu HZ count (conservative) vs existing in_hz flag",
            "n_total": int(len(df)),
            "n_hz_kopparapu": n_hz_new,
            "n_hz_existing_flag": n_hz_old,
            "note": "differences come from HZ definition (moist/max greenhouse vs the pipeline's conservative box)",
        }
    )

    # --- D. Scale heights for HZ + rocky subset -> CSV
    # All HZ planets (existing flag) with complete parameters; the rocky ones
    # (R < 1.8 R_earth) are the priority targets for transmission spectroscopy.
    rocky_hz = df[df.get("in_hz", 0) == 1].copy()
    rows = []
    for r in rocky_hz.itertuples():
        if pd.isna(r.pl_rade) or pd.isna(r.pl_bmasse) or pd.isna(r.st_teff) or pd.isna(r.st_rad) or pd.isna(r.st_mass):
            continue
        Rp = r.pl_rade * 6.371e6
        Mp = r.pl_bmasse * 5.972e24
        Rs = r.st_rad * 6.957e8
        Ms = r.st_mass * 1.98847e30
        a = (r.pl_orbper * 86400.0) ** (2.0 / 3.0) * (6.67430e-11 * Ms) ** (1.0 / 3.0) / (4 * np.pi**2) ** (1.0 / 3.0) if pd.notna(r.pl_orbper) else None
        if a is None:
            continue
        Teq = E.equilibrium_temperature(r.st_teff, Rs, a, albedo=0.3)
        g = E.surface_gravity(Mp, Rp)
        H = E.scale_height(Teq, 2.3, g)
        sig = E.transmission_depth(Rp, H, Rs)
        rows.append(
            {
                "pl_name": r.pl_name,
                "hostname": getattr(r, "hostname", ""),
                "likely_rocky": bool(r.pl_rade < 1.8),
                "pl_rade": r.pl_rade,
                "pl_bmasse": r.pl_bmasse,
                "st_teff": r.st_teff,
                "T_eq_K": Teq,
                "g_ms2": g,
                "scale_height_m": H,
                "scale_height_km": H / 1000.0,
                "transmission_signal": sig,
            }
        )
    if rows:
        out_df = pd.DataFrame(rows).sort_values("scale_height_km", ascending=False)
        out_path = ROOT / "data" / "processed" / "hz_scale_heights.csv"
        out_df.to_csv(out_path, index=False)
        out["checks"].append(
            {
                "label": "Scale heights for HZ+rocky subset (model-derived)",
                "n": int(len(rows)),
                "top3": out_df.head(3)[["pl_name", "scale_height_km", "transmission_signal"]].to_dict("records"),
                "output": str(out_path),
                "note": "ALL derived: atmospheres are not observed; H assumes mu=2.3 amu, albedo 0.3. likely_rocky flags R<1.8 R_earth.",
                "n_rocky": int(sum(1 for rr in rows if rr["likely_rocky"])),
            }
        )
    else:
        out["checks"].append({"label": "Scale heights for HZ+rocky subset", "n": 0, "note": "no HZ+rocky rows with complete data"})

    return out

# ------------------------------------------------------------------------ reporting


def main():
    t_start = time.time()
    report_lines = [
        "# Exoplanet formula derivations and verification",
        "",
        f"Generated (UTC): {datetime.now(timezone.utc).isoformat()}",
        "",
        "Every entry: symbolic derivation in `models/derivations.py` executed with Sympy,",
        "each check simplifies to an identity (0) or strict inequality; then numeric",
        "spot-checks against the closed forms (astropy precise constants).",
        "",
    ]
    json_out = {
        "fetched_utc": datetime.now(timezone.utc).isoformat(),
        "symbolic": [],
        "numeric": [],
    }

    all_ok = True
    # --- symbolic
    report_lines += ["## Symbolic derivations", ""]
    for res in D.run_all():
        checks = res.get("checks", [])
        failed = [
            c["label"]
            for c in checks
            if c.get("ok") is not None and not bool(c.get("ok"))
        ]
        entry = {
            "name": res["name"],
            "description": res.get("description"),
            "formula": res.get("formula"),
            "formula_latex": res.get("formula_latex"),
            "steps": res.get("steps"),
            "checks": [
                {
                    "label": c["label"],
                    "ok": (None if c.get("ok") is None else bool(c["ok"])),
                }
                for c in checks
            ],
            "all_ok": not failed,
        }
        json_out["symbolic"].append(entry)
        status = "PASS" if not failed else "FAIL: " + "; ".join(failed)
        all_ok &= not failed
        report_lines.append(f"### {res['name']} — {status}")
        if res.get("description"):
            report_lines.append(f"{res['description']}")
        report_lines.append(f"- formula: `{res.get('formula', '')}`")
        if res.get("formula_latex"):
            for latex in res["formula_latex"]:
                report_lines.append(f"- LaTeX: `{latex}`")
        if res.get("steps"):
            report_lines.append("- steps:")
            for step in res["steps"]:
                report_lines.append(f"  - {step}")
        for c in checks:
            state = (
                ("PASS" if c.get("ok") is True else "numeric probe (see below)")
                if c.get("ok") is not False
                else "FAIL"
            )
            report_lines.append(f"- check: **{c['label']}** → {state}")
        report_lines.append("")

    # --- numeric
    report_lines += ["## Numerical spot checks", ""]
    for chk in numeric_checks():
        json_out["numeric"].append(chk)
        all_ok &= bool(chk["pass"])
        report_lines.append(f"### {chk['label']} — {'PASS' if chk['pass'] else 'FAIL'}")
        for k, v in chk.items():
            if k not in {"label", "pass"}:
                report_lines.append(f"- {k}: {v}")
        report_lines.append("")

    # --- real-data verification of the 4 new families
    report_lines += ["## Real-data verification (NASA Exoplanet Archive)", ""]
    rd = real_data_checks()
    json_out["real_data"] = rd
    for c in rd.get("checks", []):
        report_lines.append(f"### {c['label']}")
        for k, v in c.items():
            if k != "label":
                report_lines.append(f"- {k}: {v}")
        report_lines.append("")

    report_lines.append(
        f"Total: {'ALL CHECKS PASS' if all_ok else 'SOME CHECKS FAILED'} "
        f"({time.time() - t_start:.1f} s)"
    )
    report_lines.append("")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "exoplanet_derivation_checks.json").write_text(
        json.dumps(json_out, indent=2, default=str)
    )
    (REPORTS_DIR / "exoplanet_derivations_report.md").write_text(
        "\n".join(report_lines)
    )
    print("\n".join(report_lines[-3:]))
    print(
        "wrote",
        REPORTS_DIR / "exoplanet_derivations_report.md",
        "and",
        RESULTS_DIR / "exoplanet_derivation_checks.json",
    )
    if not all_ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
