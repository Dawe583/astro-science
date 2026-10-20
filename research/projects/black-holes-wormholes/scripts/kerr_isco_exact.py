#!/usr/bin/env python3
"""
Exact Kerr ISCO radius and error budget of the linear approximation used in
notebook 02_geodesics_orbits.ipynb.

Physics
-------
Bardeen-Press-Teukolsky (1972) give the innermost stable circular orbit (ISCO)
in the equatorial plane of a Kerr black hole.  In geometric units G = c = 1,
with the radius expressed in units of M (so that r is dimensionless), and with
the dimensionless spin a = J/(M^2 c) in [0, 1):

    r_ISCO/M = 3 + Z2 -/+ sqrt((3 - Z1)(3 + Z1 + 2 Z2))          (1)
    Z1       = 1 + (1 - a^2)^(1/3) [(1 + a)^(1/3) + (1 - a)^(1/3)]  (2)
    Z2       = sqrt(3 a^2 + Z1^2)                                   (3)

Upper signs are prograde (co-rotating with the hole), lower signs retrograde.

The notebook instead evaluates

    r_notebook = r_s (6 - 5 a),   r_s = 2 G M / c^2 = 2 M           (4)

i.e. r_notebook/M = 12 - 10 a.  This has two independent problems:
  (i)  the prefactor is r_s instead of M (a factor 2), and
  (ii) the spin dependence is a straight line rather than the exact curve.
The "intended" linear chord between the correct endpoints 6M and 1M is
r_chord/M = 6 - 5a; we report both so that (i) and (ii) can be separated.

Units
-----
Internally everything is geometric (G = c = 1, lengths in M).  SI values are
obtained by multiplying by r_g = G M / c^2 and are reported in km.

References
----------
- Bardeen, Press & Teukolsky 1972, ApJ 178, 347 (ISCO formula).
- Bardeen 1970, ApJ 161, 103 (circular geodesics in Kerr).
- Misner, Thorne & Wheeler 1973, Gravitation, sec. 33.5.
- Thorne 1974, ApJ 191, 507 (maximal astrophysical spin a_* ~ 0.998).

Run from the project root:
    /home/dawe/Projects/astro-science/.venv/bin/python \
        research/projects/black-holes-wormholes/scripts/kerr_isco_exact.py

Outputs
-------
    results/isco_error_table.csv
    results/isco_exact_vs_approx.png
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np

from astropy import constants as const
from astropy import units as u

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "results"

A_MAX = 0.998  # Thorne (1974) maximal astrophysical spin
TABLE_SPINS = (0.0, 0.5, 0.9, 0.998)


# ---------------------------------------------------------------------------
# Exact Bardeen-Press-Teukolsky ISCO
# ---------------------------------------------------------------------------
def _check_spin(a: float) -> float:
    a = float(a)
    if not 0.0 <= a <= 1.0:
        raise ValueError(f"dimensionless spin must satisfy 0 <= a <= 1, got {a}")
    return a


def z1(a: float) -> float:
    """BPT auxiliary quantity Z1, equation (2)."""
    a = _check_spin(a)
    return 1.0 + (1.0 - a * a) ** (1.0 / 3.0) * (
        (1.0 + a) ** (1.0 / 3.0) + (1.0 - a) ** (1.0 / 3.0)
    )


def z2(a: float) -> float:
    """BPT auxiliary quantity Z2, equation (3)."""
    a = _check_spin(a)
    return np.sqrt(3.0 * a * a + z1(a) ** 2)


def isco_radius_over_M(a: float, prograde: bool = True) -> float:
    """Exact Kerr ISCO radius in units of M = GM/c^2 (BPT 1972).

    Parameters
    ----------
    a : float
        Dimensionless spin a_* in [0, 1].
    prograde : bool
        True for the prograde (co-rotating) branch, False for retrograde.

    Returns
    -------
    float
        r_ISCO / M, dimensionless.
    """
    a = _check_spin(a)
    zz1, zz2 = z1(a), z2(a)
    sign = -1.0 if prograde else +1.0
    return 3.0 + zz2 + sign * np.sqrt((3.0 - zz1) * (3.0 + zz1 + 2.0 * zz2))


def isco_radius_over_M_array(a, prograde: bool = True):
    """Vectorised exact ISCO, r_ISCO/M for an array of spins in [0, 1]."""
    a = np.asarray(a, dtype=float)
    if np.any((a < 0.0) | (a > 1.0)):
        raise ValueError("all spins must satisfy 0 <= a <= 1")
    zz1 = 1.0 + np.cbrt(1.0 - a * a) * (np.cbrt(1.0 + a) + np.cbrt(1.0 - a))
    zz2 = np.sqrt(3.0 * a * a + zz1 * zz1)
    sign = -1.0 if prograde else 1.0
    return 3.0 + zz2 + sign * np.sqrt((3.0 - zz1) * (3.0 + zz1 + 2.0 * zz2))


def isco_radius_si(mass, a: float, prograde: bool = True):
    """Exact ISCO radius as an astropy Quantity in km.

    Parameters
    ----------
    mass : astropy.units.Quantity
        Black-hole mass (any mass unit).
    a : float
        Dimensionless spin in [0, 1].
    prograde : bool
        Branch selector.

    Returns
    -------
    astropy.units.Quantity
        r_ISCO in km.
    """
    r_g = (const.G * mass / const.c**2).to(u.km)
    return (isco_radius_over_M(a, prograde) * r_g).to(u.km)


def horizon_radius_over_M(a: float) -> float:
    """Outer Kerr horizon r_+/M = 1 + sqrt(1 - a^2)."""
    a = _check_spin(a)
    return 1.0 + np.sqrt(1.0 - a * a)


# ---------------------------------------------------------------------------
# What the notebook actually computes
# ---------------------------------------------------------------------------
def notebook_isco_radius_over_M(a: float) -> float:
    """Reproduce notebooks/02_geodesics_orbits.ipynb, cell 9, exactly.

    The cell does ``rs = 2*G*M/c**2`` and ``r_isco = rs*(6 - 5*a)``, hence
    r/M = 2*(6 - 5a) = 12 - 10a.  This is *not* the intended 6 - 5a chord.
    """
    a = _check_spin(a)
    return 2.0 * (6.0 - 5.0 * a)


def notebook_isco_radius_si(mass, a: float):
    """Notebook ISCO as an astropy Quantity in km (reproduction of cell 9)."""
    r_s = (2.0 * const.G * mass / const.c**2).to(u.km)
    return (r_s * (6.0 - 5.0 * a)).to(u.km)


def chord_isco_radius_over_M(a: float) -> float:
    """Intended linear interpolation between 6M (a=0) and 1M (a=1): 6 - 5a."""
    a = _check_spin(a)
    return 6.0 - 5.0 * a


def percent_error(approx, exact):
    """Signed percent error 100*(approx - exact)/exact."""
    return 100.0 * (np.asarray(approx) - np.asarray(exact)) / np.asarray(exact)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
def validate(verbose: bool = True) -> dict:
    """Analytic limits, quartic residual, monotonicity, horizon, cusp slope."""
    checks = {}

    checks["a=0 prograde = 6"] = abs(isco_radius_over_M(0.0, True) - 6.0)
    checks["a=0 retrograde = 6"] = abs(isco_radius_over_M(0.0, False) - 6.0)
    checks["a=1 prograde = 1"] = abs(isco_radius_over_M(1.0, True) - 1.0)
    checks["a=1 retrograde = 9"] = abs(isco_radius_over_M(1.0, False) - 9.0)
    for name, err in checks.items():
        if err > 1e-10:
            raise AssertionError(f"validation failed: {name} (off by {err:.3e})")

    a = np.linspace(0.0, 1.0, 20001)
    r_pro = isco_radius_over_M_array(a, True)
    r_ret = isco_radius_over_M_array(a, False)

    # ISCO must lie on or outside the event horizon.  At a=1 the prograde ISCO
    # and the horizon coincide (r=1), so the boundary is non-strict there.
    r_h = 1.0 + np.sqrt(1.0 - a * a)
    if not np.all(r_pro >= r_h - 1e-12):
        raise AssertionError("prograde ISCO crosses the horizon")
    if not np.all(r_ret > r_h):
        raise AssertionError("retrograde ISCO crosses the horizon")

    # Monotonicity: prograde decreases, retrograde increases with spin.
    if not np.all(np.diff(r_pro) < 0.0):
        raise AssertionError("prograde ISCO is not strictly decreasing")
    if not np.all(np.diff(r_ret) > 0.0):
        raise AssertionError("retrograde ISCO is not strictly increasing")

    # Marginal-stability quartic: r^2 - 6r + 8 a sqrt(r) - 3a^2 = 0
    # (a -> -a for the retrograde branch).
    resid_pro = r_pro**2 - 6.0 * r_pro + 8.0 * a * np.sqrt(r_pro) - 3.0 * a * a
    resid_ret = r_ret**2 - 6.0 * r_ret - 8.0 * a * np.sqrt(r_ret) - 3.0 * a * a
    scale = np.maximum(r_pro**2, 1.0)
    max_resid = max(
        np.max(np.abs(resid_pro) / scale),
        np.max(np.abs(resid_ret) / np.maximum(r_ret**2, 1.0)),
    )
    if max_resid > 1e-10:
        raise AssertionError(f"BPT quartic residual too large: {max_resid:.3e}")

    # Weak-spin cusp: r = 6 - 4 sqrt(2/3) |a| + O(a^2), so the one-sided
    # derivative at a=0 is -4 sqrt(2/3) = -3.265986... (prograde).
    # h=1e-4 keeps the O(h) truncation near 4e-5 while avoiding the
    # catastrophic cancellation in (3 - Z1) ~ a^2 at much smaller h.
    h = 1e-4
    slope_pro = (isco_radius_over_M(h, True) - 6.0) / h
    slope_ret = (isco_radius_over_M(h, False) - 6.0) / h
    expected = -4.0 * np.sqrt(2.0 / 3.0)
    if abs(slope_pro - expected) > 1e-3:
        raise AssertionError(f"prograde cusp slope {slope_pro:.8f} != {expected:.8f}")
    if abs(slope_ret + expected) > 1e-3:
        raise AssertionError(
            f"retrograde cusp slope {slope_ret:.8f} != {-expected:.8f}"
        )

    if verbose:
        print("Validation")
        print("-" * 72)
        print("  a=0  : prograde = 6.000000 M, retrograde = 6.000000 M")
        print("  a=1  : prograde = 1.000000 M, retrograde = 9.000000 M")
        print(f"  BPT quartic max scaled residual (grid 0..1) : {max_resid:.3e}")
        print("  monotonic: prograde decreasing, retrograde increasing  [ok]")
        print("  ISCO > r_+ for all a in [0, 1]                        [ok]")
        print(
            f"  cusp slope dr/da at a=0+ : prograde {slope_pro:+.6f}, "
            f"retrograde {slope_ret:+.6f}  (= -/+4 sqrt(2/3))"
        )
        print()

    return {
        "max_quartic_residual": max_resid,
        "slope_prograde_a0": slope_pro,
        "slope_retrograde_a0": slope_ret,
    }


# ---------------------------------------------------------------------------
# Error budget
# ---------------------------------------------------------------------------
def error_budget(a_max: float = A_MAX, n: int = 200001) -> dict:
    """Scan [0, a_max] and locate the worst-case errors of both approximations."""
    a = np.linspace(0.0, a_max, n)
    exact = isco_radius_over_M_array(a, True)

    nb = 12.0 - 10.0 * a
    chord = 6.0 - 5.0 * a

    nb_abs = nb - exact
    nb_pct = percent_error(nb, exact)
    ch_abs = chord - exact
    ch_pct = percent_error(chord, exact)

    i_nb_pct = int(np.argmax(np.abs(nb_pct)))
    i_nb_abs = int(np.argmax(np.abs(nb_abs)))
    i_ch_pct = int(np.argmax(np.abs(ch_pct)))
    i_ch_abs = int(np.argmax(np.abs(ch_abs)))

    return {
        "a": a,
        "exact": exact,
        "notebook": nb,
        "chord": chord,
        "notebook_abs_error_M": nb_abs,
        "notebook_pct_error": nb_pct,
        "chord_abs_error_M": ch_abs,
        "chord_pct_error": ch_pct,
        "notebook_max_pct": (a[i_nb_pct], nb_pct[i_nb_pct]),
        "notebook_max_abs_M": (a[i_nb_abs], nb_abs[i_nb_abs]),
        "chord_max_pct": (a[i_ch_pct], ch_pct[i_ch_pct]),
        "chord_max_abs_M": (a[i_ch_abs], ch_abs[i_ch_abs]),
        "notebook_at_a_max": (float(nb[-1]), float(nb_pct[-1])),
        "chord_at_a_max": (float(chord[-1]), float(ch_pct[-1])),
    }


def print_table(mass_msun: float = 36.0) -> None:
    """Print the requested table at a = 0, 0.5, 0.9, 0.998 (M units and km)."""
    mass = mass_msun * u.Msun
    r_g_km = (const.G * mass / const.c**2).to(u.km).value
    hdr = (
        f"{'a*':>6} {'r_exact,pro':>11} {'r_exact,ret':>11} "
        f"{'r_nb':>7} {'d_nb':>7} {'err_nb':>8} "
        f"{'r_chord':>8} {'err_chord':>9} {'r_exact,pro':>11} {'r_nb':>10}"
    )
    print(f"ISCO table (M = {mass_msun:g} Msun, r_g = GM/c^2 = {r_g_km:.3f} km)")
    print(hdr)
    print(
        f"{'':>6} {'[M]':>11} {'[M]':>11} {'[M]':>7} {'[M]':>7} {'[%]':>8} "
        f"{'[M]':>8} {'[%]':>9} {'[km]':>11} {'[km]':>10}"
    )
    print("-" * len(hdr))
    rows = []
    for a in TABLE_SPINS:
        r_pro = isco_radius_over_M(a, True)
        r_ret = isco_radius_over_M(a, False)
        r_nb = notebook_isco_radius_over_M(a)
        r_ch = chord_isco_radius_over_M(a)
        rows.append(
            {
                "a_star": a,
                "r_isco_prograde_M": r_pro,
                "r_isco_retrograde_M": r_ret,
                "r_horizon_M": horizon_radius_over_M(a),
                "notebook_r_M": r_nb,
                "notebook_abs_error_M": r_nb - r_pro,
                "notebook_pct_error": 100.0 * (r_nb - r_pro) / r_pro,
                "linear_chord_r_M": r_ch,
                "linear_chord_abs_error_M": r_ch - r_pro,
                "linear_chord_pct_error": 100.0 * (r_ch - r_pro) / r_pro,
                "r_isco_prograde_km": r_pro * r_g_km,
                "notebook_r_km": r_nb * r_g_km,
                "r_isco_retrograde_km": r_ret * r_g_km,
            }
        )
        print(
            f"{a:6.3f} {r_pro:11.6f} {r_ret:11.6f} {r_nb:7.3f} "
            f"{r_nb - r_pro:+7.3f} {100.0 * (r_nb - r_pro) / r_pro:+8.3f} "
            f"{r_ch:8.3f} {100.0 * (r_ch - r_pro) / r_pro:+9.3f} "
            f"{r_pro * r_g_km:11.3f} {r_nb * r_g_km:10.3f}"
        )
    print()
    return rows


# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
def make_figure(budget: dict, output_png: Path) -> None:
    """Two-panel figure: ISCO radii and percent error vs exact prograde."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    a = budget["a"]
    fig, (ax, axerr) = plt.subplots(
        2,
        1,
        figsize=(10.0, 9.0),
        sharex=True,
        gridspec_kw={"height_ratios": [3, 2], "hspace": 0.08},
    )

    ax.plot(a, budget["exact"], color="black", lw=2.4, label="Exact BPT, prograde")
    ax.plot(
        a,
        isco_radius_over_M_array(a, False),
        color="#1b7837",
        lw=2.0,
        ls="-",
        label="Exact BPT, retrograde",
    )
    ax.plot(
        a,
        budget["notebook"],
        color="#c0392b",
        lw=2.2,
        ls="--",
        label="Notebook: $r_s(6-5a)$ = $(12-10a)\\,M$",
    )
    ax.plot(
        a,
        budget["chord"],
        color="#e08214",
        lw=1.8,
        ls=":",
        label="Intended linear chord: $(6-5a)\\,M$",
    )

    # Thorne limit.
    ax.axvline(A_MAX, color="0.5", lw=1.0, ls="-.", label=r"$a_*=0.998$ (Thorne limit)")

    # Annotate exact prograde at the astrophysical limit.
    r_lim = isco_radius_over_M(A_MAX, True)
    ax.plot([A_MAX], [r_lim], "o", color="black", ms=6, zorder=5)
    ax.annotate(
        f"exact prograde at $a_*=0.998$:\n$r={r_lim:.3f}\\,M$",
        xy=(A_MAX, r_lim),
        xytext=(0.68, 6.0),
        arrowprops=dict(arrowstyle="->", lw=1.0),
        fontsize=9,
    )

    a_nb, e_nb = budget["notebook_max_pct"]
    a_ch, e_ch = budget["chord_max_pct"]
    ax.annotate(
        f"notebook is 2x exact at $a_*=0$\n($12M$ instead of $6M$)",
        xy=(0.02, 11.8),
        xytext=(0.17, 11.15),
        arrowprops=dict(arrowstyle="->", lw=1.0, color="#c0392b"),
        color="#c0392b",
        fontsize=9,
    )
    ax.text(
        0.60,
        8.55,
        "exact retrograde\n(no notebook branch)",
        color="#1b7837",
        fontsize=9,
        ha="left",
        va="bottom",
    )

    ax.set_ylabel(r"$r_{\rm ISCO}/M$   [$M=GM/c^2$]")
    ax.set_ylim(0.0, 13.2)
    ax.set_xlim(0.0, 1.0)
    ax.grid(alpha=0.25)
    ax.legend(loc="upper right", fontsize=9, framealpha=0.95)
    ax.set_title(
        "Kerr ISCO: exact Bardeen-Press-Teukolsky vs notebook linear approximation\n"
        r"geometric units $G=c=1$; spin $a_*=Jc/(GM^2)$",
        fontsize=11,
    )

    axerr.axhline(0.0, color="0.3", lw=0.8)
    axerr.plot(
        a,
        budget["notebook_pct_error"],
        color="#c0392b",
        lw=2.0,
        ls="--",
        label="Notebook $(12-10a)M$",
    )
    axerr.plot(
        a,
        budget["chord_pct_error"],
        color="#e08214",
        lw=1.8,
        ls=":",
        label="Linear chord $(6-5a)M$",
    )
    axerr.fill_between(
        a, 0.0, budget["notebook_pct_error"], color="#c0392b", alpha=0.08
    )

    axerr.plot([a_nb], [e_nb], "o", color="#c0392b", ms=5)
    axerr.annotate(
        f"max $|\\epsilon|$ = {abs(e_nb):.1f}%\nat $a_*={a_nb:.3f}$",
        xy=(a_nb, e_nb),
        xytext=(a_nb + 0.10, e_nb - 34),
        arrowprops=dict(arrowstyle="->", lw=1.0, color="#c0392b"),
        color="#c0392b",
        fontsize=9,
    )
    axerr.plot([a_ch], [e_ch], "o", color="#e08214", ms=5)
    axerr.annotate(
        f"max $|\\epsilon|$ = {abs(e_ch):.1f}%\nat $a_*={a_ch:.3f}$",
        xy=(a_ch, e_ch),
        xytext=(a_ch - 0.26, e_ch + 12),
        arrowprops=dict(arrowstyle="->", lw=1.0, color="#e08214"),
        color="#9a5b00",
        fontsize=9,
    )

    axerr.set_xlabel(r"Dimensionless spin $a_*=Jc/(GM^2)$")
    axerr.set_ylabel(r"Percent error vs exact prograde  [%]")
    axerr.set_xlim(0.0, 1.0)
    axerr.grid(alpha=0.25)
    axerr.legend(loc="lower left", fontsize=9, framealpha=0.95)

    fig.savefig(output_png, dpi=300, bbox_inches="tight")
    plt.close(fig)


def write_csv(rows, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mass-msun",
        type=float,
        default=36.0,
        help="reference black-hole mass in solar masses (default 36)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="directory for CSV and PNG outputs",
    )
    parser.add_argument("--no-plot", action="store_true", help="skip figure generation")
    args = parser.parse_args()

    print("=" * 72)
    print("Kerr ISCO: exact BPT formula vs notebook linear approximation")
    print("=" * 72)
    print()

    stats = validate(verbose=True)
    rows = print_table(args.mass_msun)

    budget = error_budget()
    a_nb, e_nb = budget["notebook_max_pct"]
    a_nbi, e_nbi = budget["notebook_max_abs_M"]
    a_ch, e_ch = budget["chord_max_pct"]
    a_chi, e_chi = budget["chord_max_abs_M"]

    print(f"Worst-case errors on a* in [0, {A_MAX}]")
    print("-" * 72)
    print(f"  Notebook (12-10a)M : max |pct| = {abs(e_nb):8.2f}%  at a* = {a_nb:.4f}")
    print(f"                       max |abs| = {abs(e_nbi):8.3f} M at a* = {a_nbi:.4f}")
    print(f"  Linear chord (6-5a)M: max |pct| = {abs(e_ch):8.2f}%  at a* = {a_ch:.4f}")
    print(f"                       max |abs| = {abs(e_chi):8.3f} M at a* = {a_chi:.4f}")
    print(
        f"  Notebook at a*=0.998: {budget['notebook_at_a_max'][0]:.3f} M "
        f"({budget['notebook_at_a_max'][1]:+.2f}% vs exact)"
    )
    print(
        f"  Chord    at a*=0.998: {budget['chord_at_a_max'][0]:.3f} M "
        f"({budget['chord_at_a_max'][1]:+.2f}% vs exact)"
    )
    print()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.output_dir / "isco_error_table.csv"
    write_csv(rows, csv_path)
    print(f"Wrote {csv_path}")

    if not args.no_plot:
        png_path = args.output_dir / "isco_exact_vs_approx.png"
        make_figure(budget, png_path)
        print(f"Wrote {png_path}")

    print()
    print("Note: the notebook has no retrograde branch at all; the exact")
    print("retrograde ISCO is reported here for completeness (6M at a*=0,")
    print("9M at a*=1, increasing with spin).")
    print(
        f"Validation: max scaled BPT quartic residual = "
        f"{stats['max_quartic_residual']:.2e}"
    )


if __name__ == "__main__":
    main()
