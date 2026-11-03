# Super-Earths and Oxygen Biosignatures

Companion to the exoplanet habitability analysis. This document derives the
quantities used to assess whether a rocky exoplanet can retain an atmosphere
and whether oxygen can be detected as a biosignature.

## 1. Habitable zone (Kopparapu et al. 2013)

The effective stellar flux for a planet at distance $d$ (AU) from a star of
luminosity $L$ and effective temperature $T_\star$ is

\begin{equation}
    S_{\rm eff} = \frac{L/L_\odot}{(d/{\rm AU})^2}.
\end{equation}

The HZ boundaries are defined by $S_{\rm eff} = S_{\rm eff}^\star(T_\star)$,
where $S_{\rm eff}^\star$ is a 4th-order polynomial in $(T_\star - 5780)$ K:

\begin{equation}
    S_{\rm eff}^\star = S_0 + a\,\Delta T + b\,\Delta T^2 + c\,\Delta T^3 + d\,\Delta T^4,
    \quad \Delta T = T_\star - 5780.
\end{equation}

Key boundaries: recent Venus (inner), runaway greenhouse, moist greenhouse
(conservative inner), max greenhouse (conservative outer), early Mars (outer).

## 2. Equilibrium temperature

\begin{equation}
    T_{\rm eq} = T_\star \sqrt{\frac{R_\star}{2a}}\,(1-A)^{1/4}
\end{equation}

where $A$ is the Bond albedo. Surface temperature includes greenhouse warming:
$T_{\rm surf} = T_{\rm eq} + \Delta T_{\rm GH}$.

## 3. Atmospheric retention (Jeans escape)

The Jeans escape parameter:

\begin{equation}
    \lambda = \frac{v_{\rm esc}^2}{v_{\rm th}^2}
    = \frac{GMm}{k_B T R}
\end{equation}

where $v_{\rm esc} = \sqrt{2GM/R}$ and $v_{\rm th} = \sqrt{2k_BT/m}$.
Atmosphere is retained over geological timescales when $\lambda > 3$–$5$.

For Super-Earths (M > 1 M⊕, R > 1 R⊕), $\lambda$ is large for heavy species
(O₂, N₂, CO₂) but small for H₂/He, explaining why rocky planets retain
heavy atmospheres but lose primordial hydrogen.

## 4. Oxygen biosignature

O₂ has strong absorption bands (A-band at 0.76 μm, B-band at 0.69 μm).
O₃ (ozone) has the Hartley band at 0.25 μm.

Transit depth variation due to atmosphere:

\begin{equation}
    \Delta \delta = \frac{2 R_p H}{R_\star^2}
\end{equation}

where $H = k_BT/(\mu m_p g)$ is the scale height. For an Earth-like planet
transiting an M-dwarf, $\Delta \delta \sim 10^{-4}$–$10^{-5}$, detectable
with JWST (5-σ requires $\sim$10-50 transits).

## 5. Energy-limited escape (water loss)

For planets in the HZ of M-dwarfs, XUV-driven escape can remove water:

\begin{equation}
    \frac{dM}{dt} = \frac{\pi R_p^3 F_{\rm XUV} \epsilon}{GM_p K}
\end{equation}

Water loss timescale: $\tau = M_{\rm water}/(dM/dt)$. If $\tau < 4.5$ Gyr,
the planet loses its water and becomes a Venus-like desert.

## 6. Tidal locking

HZ planets around M-dwarfs have short orbital periods and are often tidally
locked:

\begin{equation}
    \tau_{\rm lock} \sim 10^9\,{\rm yr} \times
    \left(\frac{a}{1\,{\rm AU}}\right)^6
    \left(\frac{M_\star}{M_\odot}\right)^{-2}
    \left(\frac{R_p}{R_\oplus}\right)^{-5}
\end{equation}

Tidally locked planets may have atmospheric collapse on the night side,
but 3D GCM models show that thick atmospheres can redistribute heat.

## 7. Summary of HZ candidates

From the NASA Exoplanet Archive (2026-11-04):
- **45 planets** with $R < 2.5\,R_\oplus$ and $T_{\rm eq} \in [180, 350]$ K
- **2,466 small planets** (R < 2.5 Re) total
- Top candidates: Kepler-1649 b/c, TOI-2095 b/c, LP 890-9 c, K2-3 d, TOI-715 b

All quantities are model-derived (theory), not observed. No oxygen detection
has been confirmed on any exoplanet to date (2026).