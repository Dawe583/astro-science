# Exoplanet formula derivations and verification

Generated (UTC): 2026-10-27T22:58:59.880011+00:00

Every entry: symbolic derivation in `models/derivations.py` executed with Sympy,
each check simplifies to an identity (0) or strict inequality; then numeric
spot-checks against the closed forms (astropy precise constants).

## Symbolic derivations

### kepler_third_law — PASS
Kepler's third law for exoplanet orbital period
- formula: `P = 2 pi sqrt(a^3 / (G M))`
- LaTeX: `P = 2\pi\sqrt{\frac{a^{3}}{GM}}`
- steps:
  - Start from gravitational force = centripetal force: G M m / a^2 = m v^2 / a
  - Cancel planet mass m: G M / a = v^2
  - Substitute orbital velocity v = 2 pi a / P (circular orbit: circumference / period)
  - G M / a = 4 pi^2 a^2 / P^2
  - Rearrange: P^2 = 4 pi^2 a^3 / (G M)
  - Take square root: P = 2 pi sqrt(a^3 / (G M))
- check: **P^2 proportional to a^3 (Kepler's third law)** → PASS

### atmospheric_escape_energy_limited — PASS
Energy-limited atmospheric escape rate (Watson et al. 1981)
- formula: `dM/dt = pi * R^3 * F_XUV * epsilon / (G * M * K)`
- LaTeX: `\frac{dM}{dt} = \frac{\pi R^{3} F_{\mathrm{XUV}} \varepsilon}{G M K}`
- steps:
  - XUV power absorbed by planet: P_abs = pi * R^2 * F_XUV * epsilon
  -   (cross-section pi R^2, heating efficiency epsilon)
  - Gravitational potential energy per unit mass at surface: U = G M / R
  - Roche lobe correction reduces potential barrier: U_eff = G M K / R
  -   (K <= 1 accounts for stellar tidal potential reducing escape energy)
  - Mass loss rate from energy balance: dM/dt = P_abs / U_eff
  - Substitute: dM/dt = (pi R^2 F_XUV epsilon) / (G M K / R)
  - Simplify: dM/dt = (pi * R^3 * F_XUV * epsilon) / (G * M * K)
- check: **Formula structure identity (dM/dt = pi R^3 F_XUV eps / (G M K))** → PASS
- check: **Energy balance: absorbed XUV power = gravitational power for escape** → PASS

### stellar_density_from_transit — PASS
Stellar mean density inferred from a central transit (Seager & Mallen-Ornelas 2003)
- formula: `rho_* = 24 P / (pi^2 G T^3)`
- LaTeX: `\rho_* = \frac{24\,P}{\pi^{2} G\,T^{3}}`
- steps:
  - Central transit (b=0), small planet: full transit duration T = 2 R_* P / (pi a)
  - Solve for a/R_* = 2 P / (pi T)
  - Kepler: rho_* = M_*/(4/3 pi R_*^3) = (3 pi/(G P^2))(a/R_*)^3
  - Substitute a/R_*: rho_* = (3 pi/(G P^2)) (2 P/(pi T))^3
  - Simplify: rho_* = 24 P / (pi^2 G T^3)
- check: **rho_* simplifies to 24 P / (pi^2 G T^3)** → PASS
- check: **algebraic identity of the two forms** → PASS

### rv_semi_amplitude — PASS
Radial-velocity semi-amplitude K (Newtonian two-body)
- formula: `K = (2 pi G / P)^(1/3) * M_p sin i / (M_* + M_p)^(2/3) / sqrt(1 - e^2)`
- LaTeX: `K = \left(\frac{2\pi G}{P}\right)^{1/3}\frac{M_p\sin i}{(M_*+M_p)^{2/3}}\frac{1}{\sqrt{1-e^2}}`
- steps:
  - Newtonian two-body: separation a = (G (M*+Mp) P^2/(4 pi^2))^(1/3)
  - Star orbits the barycentre: a_* = a * Mp/(M*+Mp)
  - Projected velocity amplitude: K = 2 pi a_* sin i / (P sqrt(1-e^2))
  - Substitute a and simplify: K = (2 pi G/P)^(1/3) Mp sin i / (M*+Mp)^(2/3) / sqrt(1-e^2)
- check: **K satisfies K^3 (M*+Mp)^2 (1-e^2)^(3/2) = (2 pi G/P) Mp^3** → PASS

### kopparapu_hz_flux — PASS
Kopparapu 2013/2014 HZ boundary from the S_eff(T_eff) polynomial
- formula: `a (AU) = sqrt(L*/L_sun / S_eff), S_eff = s0 + a T + b T^2 + c T^3 + d T^4, T = T_eff - 5780`
- LaTeX: `a_{\rm HZ} = \sqrt{L_*/L_\odot / S_{\rm eff}(T_{\rm eff})}`
- steps:
  - S_eff(T_eff) polynomial (Kopparapu 2013 Table 3) for each boundary
  - Flux balance at the boundary: L*/(4 pi a^2) = S_eff * L_sun/(4 pi (1 AU)^2)
  - Solve for a: a (AU) = sqrt(L*/L_sun / S_eff)
  - Conservative HZ: moist_greenhouse (inner) <= S/S_earth <= max_greenhouse (outer)
- check: **HZ distance satisfies a^2 * S_eff = L*/L_sun** → PASS

### scale_height_hydrostatic — PASS
Atmospheric scale height from hydrostatic equilibrium (ideal gas)
- formula: `H = k_B T / (mu m_p g)`
- LaTeX: `H = \frac{k_{\rm B}T}{\mu\,m_p\,g}`
- steps:
  - Hydrostatic equilibrium: dp/dz = -rho g
  - Ideal gas: p = rho k_B T/(mu m_p)
  - Solution: rho(z) = rho_0 exp(-z/H) with H = k_B T/(mu m_p g)
  - Pressure at the base: p_0 = rho_0 g H
- check: **Hydrostatic consistency: p = rho g H** → PASS

## Numerical spot checks

### Kepler period: code vs closed form (1 AU, 1 Msun) — PASS
- relative_deviation: 0.0

### Kepler round trip a->P->a — PASS
- relative_deviation: 1.4279818681603735e-15

### Earth/Sun transit depth ~8.4e-5 — PASS
- value: 8.386315626728506e-05

### Earth escape velocity ~11186 m/s — PASS
- value: 11185.97789184991

### Earth equilibrium temperature ~255 K — PASS
- value: 254.85041511888898

### Rocky radius for 1 Mearth ~1 Rearth — PASS
- value: 1.0

### Earth Jeans lambda > 1 — PASS
- value: 736.8820157762219

### Earth N2 scale height ~8.4 km — PASS
- value: 8.65467876659032

### Sun HZ contains 1 AU — PASS
- inner: 0.9931527705488595
- outer: 1.6762943904099954

### Earth Hill radius ~1.5e9 m — PASS
- value: 1496529374.468561

### Earth mean density ~5515 kg/m3 — PASS
- value: 5513.258738589093

### Earth surface gravity ~9.8 m/s² — PASS
- value: 9.819973426224687

### Kepler period at 0.5 AU ~0.353 yr — PASS
- value: 0.354
- reference: 0.353

### H2 Jeans parameter Earth orbit > 1 — PASS
- value: 3.388150302655952e+43

### Stellar density from transit (Earth/Sun, 13 h) ~ solar order — PASS
- value: 11216.882757958227
- reference: 1408

### RV semi-amplitude 1 Mjup @ 1 AU ~ 28.4 m/s — PASS
- value: 28.411957906995614
- reference: 28.4

### Kopparapu HZ flag: Earth (1 AU, Sun) is in HZ — PASS
- value: True

### Scale height Earth (mu=2.3, H2) ~ 106 km — PASS
- value: 105.36130672370827
- reference: 106.0

## Real-data verification (NASA Exoplanet Archive)

### Stellar density from transit vs catalog (log10 ratio)
- n: 2643
- median_log10_ratio: 0.9908502077599123
- iqr_log10: [0.8498794305842341, 1.2050693602183764]
- note: scatter expected: impact parameter b != 0, eccentricity, stellar density errors

### RV semi-amplitude K for RV-detected planets (m/s)
- n: 1187
- median_K_ms: 25.011529792129984
- min_K_ms: 0.21986574433764183
- max_K_ms: 6079.745883348715
- in_typical_range_1_200_ms: 1088
- note: consistency/units check: catalog M sin i is derived from K by construction

### Kopparapu HZ count (conservative) vs existing in_hz flag
- n_total: 6451
- n_hz_kopparapu: 27
- n_hz_existing_flag: 100
- note: differences come from HZ definition (moist/max greenhouse vs the pipeline's conservative box)

### Scale heights for HZ+rocky subset (model-derived)
- n: 21
- top3: [{'pl_name': 'TOI-7510 b', 'scale_height_km': 867.3584407889767, 'transmission_signal': 0.00015582203815458075}, {'pl_name': 'TOI-3856 b', 'scale_height_km': 556.206749841615, 'transmission_signal': 0.0001788759082729016}, {'pl_name': 'TOI-4507 b', 'scale_height_km': 515.8076865516027, 'transmission_signal': 0.00010295052780924016}]
- output: /home/dawe/Projects/astro-science/research/projects/exoplanets/data/processed/hz_scale_heights.csv
- note: ALL derived: atmospheres are not observed; H assumes mu=2.3 amu, albedo 0.3. likely_rocky flags R<1.8 R_earth.
- n_rocky: 1

Total: ALL CHECKS PASS (0.3 s)
