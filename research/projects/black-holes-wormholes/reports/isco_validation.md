# Kerr ISCO: exact Bardeen–Press–Teukolsky formula vs. the notebook linear approximation

**Project:** `research/projects/black-holes-wormholes`
**Question:** How large is the error of the "simplified approximation" for the Kerr ISCO
used in `notebooks/02_geodesics_orbits.ipynb` (cell defining `isco_radius_kerr`), relative to
the exact Bardeen–Press–Teukolsky (BPT) result?
**Date:** 2026-10-20
**Status:** validated. The exact formula is implemented, cross-checked against the
marginal-stability quartic to machine precision, and the notebook error is quantified.

---

## 1. Question

The notebook computes the Kerr innermost stable circular orbit (ISCO) with a linear
"simplified approximation" instead of the exact BPT closed form. We quantify, in units of
$M \equiv GM/c^2$ and in percent, how wrong that approximation is for prograde orbits over
the astrophysically relevant spin range $a_* \in [0, 0.998]$ (Thorne 1974 maximal spin),
and whether a retrograde branch exists at all.

## 2. Hypothesis

The notebook's `r_isco = r_s (6 - 5a)` (with `r_s = 2GM/c^2`) is not merely a linearised
ISCO: because it uses the Schwarzschild radius $r_s = 2M$ rather than the gravitational
radius $M = GM/c^2$, it returns $12M$ at $a=0$ instead of $6M$ — a factor-of-two error even
before the spin dependence is considered. We expect the error to be largest at low spin
and to reach order-unity (tens of percent) for the intended chord.

## 3. Method

### 3.1 Exact formula (Bardeen–Press–Teukolsky 1972)

In geometric units $G = c = 1$, with radius measured in units of $M$ and dimensionless spin
$a_* = Jc/(GM^2) \in [0,1]$:

$$
r_{\rm ISCO}/M = 3 + Z_2 \;\mp\; \sqrt{(3-Z_1)(3+Z_1+2Z_2)}, \tag{1}
$$
$$
Z_1 = 1 + (1-a_*^2)^{1/3}\left[(1+a_*)^{1/3} + (1-a_*)^{1/3}\right], \tag{2}
$$
$$
Z_2 = \sqrt{3a_*^2 + Z_1^2}. \tag{3}
$$

The **upper sign is prograde** (co-rotating with the hole); the lower sign is retrograde.
This is the same formula stored in `research/wiki/Kerr Metric.md`.

### 3.2 Derivation sketch

1. Start from the Kerr metric in Boyer–Lindquist coordinates, restricted to the equatorial
   plane $\theta=\pi/2$:
   $$ds^2 = -\left(1-\frac{2M}{r}\right)dt^2 - \frac{4Ma}{r}\,dt\,d\phi
   + \frac{r^2}{\Delta}\,dr^2 + \left(r^2+a^2+\frac{2Ma^2}{r}\right)d\phi^2,$$
   with $\Delta = r^2 - 2Mr + a^2$.
2. The stationary, axisymmetric Killing vectors give two conserved quantities per unit
   rest mass, energy $E = -u_t$ and angular momentum $L = u_\phi$.
3. The radial motion obeys the Carter-type potential
   $$R(r) = \left[E(r^2+a^2) - aL\right]^2 - \Delta\left[r^2 + (L - aE)^2\right].$$
4. **Circular** equatorial orbits require $R = 0$ and $dR/dr = 0$; these two conditions fix
   $E(r,a)$ and $L(r,a)$.
5. **Marginal stability** (the ISCO) additionally requires $d^2R/dr^2 = 0$. Substituting the
   circular-orbit $E,L$ yields the quartic
   $$r^2 - 6r + 8a\sqrt{r} - 3a^2 = 0 \quad\text{(prograde)},$$
   with $a \to -a$ for the retrograde branch. BPT solved this quartic in closed form,
   giving equations (1)–(3).
6. Limits: $a_* = 0 \Rightarrow r_{\rm ISCO} = 6M$ (Schwarzschild);
   $a_* = 1$ prograde $\Rightarrow r_{\rm ISCO} = M$; $a_* = 1$ retrograde
   $\Rightarrow r_{\rm ISCO} = 9M$.

### 3.3 What the notebook actually computes

`notebooks/02_geodesics_orbits.ipynb`, cell defining `isco_radius_kerr`:

```python
rs = 2 * const.G * mass / const.c**2      # Schwarzschild radius r_s = 2GM/c^2 = 2M
r_isco = rs * (6 - 5*a)                   # "Approximation"
```

In units of $M$ this is
$$
r_{\rm notebook}/M = 2\,(6 - 5a_*) = 12 - 10a_*. \tag{4}
$$

Two independent defects follow:

- **(i) Wrong prefactor.** The unit is $r_s = 2M$, not $M$. Even at $a_*=0$ the notebook
  returns $12M$ instead of the correct $6M$ — a **factor-of-two (100 %) error**.
- **(ii) Wrong spin dependence.** The intended linear chord between the correct endpoints
  $6M$ ($a=0$) and $1M$ ($a=1$) would be $r_{\rm chord}/M = 6 - 5a_*$. Equation (4) is that
  chord scaled by 2, so its deviation from the exact curve is amplified.

The notebook has **no retrograde branch at all**; only a prograde-looking line is plotted.
This is recorded as a gap.

### 3.4 Validation of the exact implementation

`scripts/kerr_isco_exact.py` implements (1)–(3) and validates it with:

- Analytic limits: $a_*=0 \to 6M$ (both branches); $a_*=1$ prograde $\to 1M$,
  retrograde $\to 9M$ (all to $<10^{-10}$).
- **Independent quartic check:** numerically solving $r^2 - 6r \pm 8a\sqrt{r} - 3a^2 = 0$
  with `scipy.optimize.brentq` reproduces the BPT value to $\sim 10^{-13}\,M$ for
  $a_* \in \{0, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99, 0.998, 1.0\}$. The script also evaluates the
  quartic residual of its own output: max scaled residual $1.6\times10^{-12}$ over a
  20 001-point grid.
- Monotonicity: prograde strictly decreasing, retrograde strictly increasing.
- Causality: $r_{\rm ISCO} \ge r_+ = 1+\sqrt{1-a_*^2}$ for all $a_*$ (equality at $a_*=1$
  prograde).
- Weak-spin cusp slope: $dr/da|_{0^+} = \mp 4\sqrt{2/3} = \mp 3.265986$, reproduced.

## 4. Results

### 4.1 Numeric table

Reference mass $M = 36\,M_\odot$ (the notebook's GW150914 mass), so
$r_g = GM/c^2 = 53.1585$ km. "Notebook" is equation (4); "chord" is the intended $6-5a_*$.

| $a_*$ | $r_{\rm pro}/M$ | $r_{\rm ret}/M$ | notebook $r/M$ | notebook $\Delta r$ [M] | notebook err [%] | chord $r/M$ | chord err [%] |
|------:|---------------:|---------------:|---------------:|------------------------:|-----------------:|-------------:|--------------:|
| 0.000 | 6.000000 | 6.000000 | 12.000 | +6.000 | **+100.000** | 6.000 | +0.000 |
| 0.500 | 4.233003 | 7.554585 | 7.000  | +2.767 | +65.367 | 3.500 | −17.316 |
| 0.900 | 2.320883 | 8.717352 | 3.000  | +0.679 | +29.261 | 1.500 | −35.369 |
| 0.998 | 1.236971 | 8.994374 | 2.020  | +0.783 | +63.302 | 1.010 | −18.349 |

In km (for $36\,M_\odot$): exact prograde $= 318.951,\ 225.020,\ 123.375,\ 65.756$ km at
$a_* = 0,\ 0.5,\ 0.9,\ 0.998$; the notebook returns
$637.902,\ 372.110,\ 159.476,\ 107.380$ km at the same spins.

The notebook's own demo spins $[0, 0.5, 0.9, 0.99]$ give notebook/exact ratios of
$2.000,\ 1.654,\ 1.293,\ 1.444$ — i.e. it is always an overestimate, worst at $a=0$.

### 4.2 Error quantification over $a_* \in [0, 0.998]$

Scanned on a 200 001-point grid:

| Approximation | max abs. error | location | max % error | location | value at $a_*=0.998$ |
|---|---:|---|---:|---|---:|
| Notebook $(12-10a)M$ | **6.000 M** | $a_*=0$ | **100.00 %** | $a_*=0$ | +63.30 % |
| Intended chord $(6-5a)M$ | 0.910 M | $a_*=0.772$ | 35.84 % | $a_*=0.930$ | −18.35 % |

**Takeaway:** the notebook's error is dominated by the factor-of-two prefactor (100 % at
$a_*=0$), not by the linearisation. Even the *intended* linear chord between the correct
endpoints $6M$ and $1M$ is wrong by up to **35.8 %** (peak near $a_* \approx 0.93$); the
exact curve is concave, so a straight chord cannot follow it.

### 4.3 Figure

`results/isco_exact_vs_approx.png` (300 dpi): top panel — exact prograde (black), exact
retrograde (green), notebook line (red dashed), intended chord (orange dotted), Thorne
limit $a_*=0.998$; bottom panel — signed percent error of both approximations vs. exact
prograde, with the two maxima annotated.

## 5. Limitations and assumptions

- **GR / Kerr only.** The result assumes the Kerr vacuum solution and general relativity;
  no charge, no cosmological constant, no modified gravity.
- **Equatorial, circular, geodesic orbits.** The ISCO is defined for the equatorial plane;
  inclined or eccentric orbits have different stability boundaries.
- **Test-particle (geodesic) limit.** Self-gravity of the orbiting body is neglected.
- **Thin-disk interpretation.** In accretion theory the ISCO sets the inner edge of a thin
  disk; real disks can truncate inside/outside it, and magnetohydrodynamic effects can move
  the effective inner edge. This is an assumption of the *application*, not of the formula.
- **Prograde vs. retrograde.** The notebook has no retrograde branch; the exact retrograde
  ISCO rises from $6M$ to $9M$ and is reported here for completeness.
- **Astrophysical spin ceiling.** $a_* \le 0.998$ (Thorne 1974) is the maximal spin expected
  from thin-disk accretion; the formulas remain valid up to $a_*=1$.
- No observational data are used; this is an analytic/numeric validation against a
  published closed-form result (BPT 1972), cross-checked via the marginal-stability quartic.

## 6. Reproduction

From the workspace root (`/home/dawe/Projects/astro-science`):

```bash
.venv/bin/python research/projects/black-holes-wormholes/scripts/kerr_isco_exact.py
```

Environment: `.venv` Python 3.14, `numpy`, `astropy`, `matplotlib` (all present).
The script is standalone and writes both outputs into `results/`.

## 7. File paths

| Artifact | Path |
|---|---|
| Script (exact formula + validation + error budget + figure) | `research/projects/black-holes-wormholes/scripts/kerr_isco_exact.py` |
| Numeric table (CSV) | `research/projects/black-holes-wormholes/results/isco_error_table.csv` |
| Figure (PNG, 300 dpi) | `research/projects/black-holes-wormholes/results/isco_exact_vs_approx.png` |
| This report | `research/projects/black-holes-wormholes/reports/isco_validation.md` |
| Reference formula (wiki) | `research/wiki/Kerr Metric.md` |
| Target notebook (read-only this run) | `research/projects/black-holes-wormholes/notebooks/02_geodesics_orbits.ipynb` |

**Notebook correction (applied by the parent, not in this run):** replace the approximation
with the exact BPT formula (equations 1–3), add the retrograde branch, and fix the unit from
$r_s=2M$ to $M=GM/c^2$.

---

## Post-fix confirmation (2026-10-20)

The notebook correction described above was applied and the notebook re-executed
successfully (`nbconvert --execute`, 265 KB output, no errors):

- Schwarzschild ISCO cell: `r_isco = 3 * r_s = 6 GM/c^2` (was `6 * r_s = 12 GM/c^2`).
- Kerr ISCO cell: exact BPT formula with prograde **and** retrograde branches; the old
  chord `r_s*(6-5a)` is gone.
- Printed check for a 36 Msun black hole: `a=0 -> 318.95 km` (6 GM/c^2);
  `a=0.50 -> prograde 225.02 km, retrograde 401.59 km`; `a=0.90 -> 123.37 / 463.40 km`;
  `a=0.99 -> 77.32 / 476.93 km` — all consistent with the error table above.

The CSV's `notebook_*` columns remain the pre-fix values, which is the point of the
comparison; `linear_chord_*` columns describe the intended chord after the unit fix.
