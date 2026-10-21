# Habitability of Exoplanets

**A Self-Contained Derivation**

All equations in SI units with $G$, $k_B$, $m_p$ kept explicit. Sign convention: outward positive for fluxes and distances; $T_{\rm eff}$ in K. Model-dependent statements are marked.

---

## 1. Habitable zone (Kopparapu et al. 2013)

The effective stellar flux $S_{\rm eff}$ at a planet is scaled to the solar
constant. The orbital distance of a boundary is

$$d = \sqrt{\frac{L_*/L_\odot}{S_{\rm eff}}}\ {\rm AU},$$

with $S_{\rm eff}$ a polynomial in $T = T_{\rm eff} - 5780\ {\rm K}$:

$$S_{\rm eff}(T) = S_0 + a\,T + b\,T^2 + c\,T^3 + d\,T^4.$$

Boundaries (inner to outer): recent Venus, runaway greenhouse, moist
greenhouse, maximum greenhouse, early Mars. The conservative HZ uses runaway
greenhouse (inner) and maximum greenhouse (outer); for the Sun these are
$\approx 0.95$ and $\approx 1.68$ AU.

## 2. Tidal locking and spin-orbit resonances

A planet is tidally locked when its rotation period equals its orbital period
(1:1 resonance, e.g. the Moon). Tidal torques scale as
$\tau_{\rm tide}\sim (k_2/Q)\,G M_*^2 R_p^5/a^6$ and drive the spin toward
synchronization on a timescale that decreases strongly with $a$. Mercury sits in
a 3:2 spin-orbit resonance ($P_{\rm rot}/P_{\rm orb}=3/2$) because of its
eccentricity and triaxiality; higher-order resonances are possible for
eccentric orbits. Tidal locking redistributes heat and can sustain a
substellar hot spot, affecting climate and atmospheric circulation.

## 3. Atmospheric escape

The Jeans escape parameter is $\lambda = v_{\rm esc}^2/v_{\rm th}^2$, with
$v_{\rm esc}=\sqrt{2GM_p/R_p}$ and $v_{\rm th}=\sqrt{2k_BT/m}$. Escape is
significant when $\lambda \lesssim 10$–$15$. The energy-limited mass-loss rate
is

$$\dot M = \frac{\epsilon\,\pi R_p^3 F_{\rm XUV}}{G M_p K_{\rm tide}},$$

with efficiency $\epsilon\sim 0.1$–$0.3$ and tidal correction $K_{\rm tide}$
(see `theory_atmospheric_escape.md`). Hydrodynamic (blow-off) escape occurs
when heating drives a bulk outflow; it dominates for highly irradiated,
low-gravity planets and can remove entire H/He envelopes.

## 4. Biosignatures and false positives

Candidate biosignatures: O$_2$, CH$_4$, H$_2$O, CO$_2$, O$_3$. Disequilibrium
pairs (O$_2$+CH$_4$) are stronger indicators than single gases. False
positives: abiotic O$_2$ from CO$_2$ photolysis and H escape; CH$_4$ from
serpentinization or volcanism; O$_3$ tracking abiotic O$_2$. Context (stellar
UV, planet mass, redox state) is required to interpret any detection.

## 5. Greenhouse limits

- **Runaway greenhouse**: absorbed stellar flux exceeds the maximum outgoing
  longwave radiation the atmosphere can emit; oceans evaporate and water is
  lost. Defines the inner (conservative) HZ edge.
- **Moist greenhouse**: upper atmosphere becomes water-rich, enabling
  photodissociation and H escape; occurs at slightly lower flux than runaway.
- **Maximum greenhouse**: outer edge where CO$_2$ condensation limits
  greenhouse warming; beyond it the planet freezes.

## 6. Kopparapu coefficients

| Boundary | $S_0$ | $a$ | $b$ | $c$ | $d$ |
|---|---|---|---|---|---|
| Recent Venus | 1.776 | $1.4335\times10^{-4}$ | $3.3954\times10^{-9}$ | $-7.6364\times10^{-12}$ | $-1.1950\times10^{-15}$ |
| Runaway greenhouse | 1.107 | $1.332\times10^{-4}$ | $1.580\times10^{-8}$ | $-8.308\times10^{-12}$ | $-1.931\times10^{-15}$ |
| Moist greenhouse | 1.014 | $8.18\times10^{-5}$ | $1.93\times10^{-9}$ | $-4.34\times10^{-12}$ | $-6.68\times10^{-16}$ |
| Maximum greenhouse | 0.356 | $6.171\times10^{-5}$ | $1.698\times10^{-9}$ | $-3.198\times10^{-12}$ | $-5.575\times10^{-16}$ |
| Early Mars | 0.320 | $5.547\times10^{-5}$ | $1.526\times10^{-9}$ | $-2.874\times10^{-12}$ | $-5.011\times10^{-16}$ |

$T = T_{\rm eff}-5780\ {\rm K}$; $d=\sqrt{L_*/L_\odot/S_{\rm eff}}$ AU.

## References

- Kopparapu et al. (2013), ApJ, 765, 131 — HZ boundaries
- Kasting et al. (1993), Icarus, 101, 108 — runaway greenhouse
- Seager (2010), Exoplanet Atmospheres
- Wordsworth & Pierrehumbert (2013), ApJ, 778, 154 — moist greenhouse
- Meadows et al. (2018), Astrobiology, 18, 630 — biosignatures
- Fulton et al. (2017), AJ, 154, 109 — radius valley
- `models/equations.py` — `habitable_zone_distances`, `jeans_escape_parameter`
