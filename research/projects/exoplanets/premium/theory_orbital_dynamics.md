# Orbital Dynamics and Habitability

Self-contained derivations for exoplanet orbits, transit geometry, habitable
zones, tidal heating, and atmospheric escape. SI units with $G$, $c$, $k_B$
kept explicit.

## 1. Keplerian orbits

For a planet of mass $m_p$ orbiting a star of mass $M_*$ at semi-major axis
$a$, Kepler's third law gives

$$P^2 = \frac{4\pi^2}{G M_*} a^3,$$

so $a = (G M_* P^2 / 4\pi^2)^{1/3}$. The circular orbital velocity is
$v_{\rm orb} = \sqrt{G M_* / a}$.

## 2. Transit geometry

When a planet crosses the stellar disk, the fractional flux drop is

$$\delta = \left(\frac{R_p}{R_*}\right)^2,$$

and the transit duration (for impact parameter $b$) is

$$T = \frac{P}{\pi}\frac{R_*}{a}\sqrt{1-b^2}.$$

The impact parameter $b = (a/R_*)\cos i$ where $i$ is the orbital inclination.

## 3. Habitable zone

The conservative habitable zone (Kopparapu et al. 2013) is bounded by the
runaway greenhouse (inner) and maximum greenhouse (outer) limits:

$$d = \sqrt{L_*/L_\odot / S_{\rm eff}}\ {\rm AU},$$

where $S_{\rm eff}$ is a polynomial in $T_{\rm eff} - 5780\ {\rm K}$.
For the Sun: inner edge $\approx 0.95$ AU, outer edge $\approx 1.68$ AU.

## 4. Tidal heating

For an eccentric orbit, the tidal heating power is

$$\dot E = \frac{21}{2}\,k_2\,\frac{G M_*^2 R_p^5\, n\, e^2}{a^6 Q},$$

where $n = 2\pi/P$ is the mean motion, $k_2$ the Love number, and $Q$ the
tidal quality factor. This drives volcanism on Io and may sustain subsurface
oceans on Europa and Enceladus.

## 5. Atmospheric escape

The Jeans escape parameter is $\lambda = v_{\rm esc}^2/v_{\rm th}^2$ where
$v_{\rm esc} = \sqrt{2GM/R}$ and $v_{\rm th} = \sqrt{2k_BT/m}$. Escape is
significant when $\lambda \lesssim 10$–$15$. The energy-limited mass-loss rate
is

$$\dot M = \frac{\epsilon \pi R_p^3 F_{\rm XUV}}{G M_p K_{\rm tide}},$$

where $F_{\rm XUV}$ is the stellar XUV flux and $K_{\rm tide}$ a tidal
correction factor. This drives the radius valley (Fulton gap) at
$\sim 1.5$–$2.0\,R_\oplus$.

## 6. Mass-radius relation

For rocky planets, $R \propto M^{0.28}$ (Zeng et al. 2016). For volatile-rich
planets, $R \propto M^{0.5}$–$M^{0.7}$. The transition occurs around
$1.5$–$1.8\,R_\oplus$.

## 7. Scale height and transmission spectroscopy

The atmospheric scale height is $H = k_BT/(\mu m_p g)$. The transit depth
variation due to the atmosphere is

$$\Delta F/F = \frac{2 R_p H}{R_*^2}.$$

Molecular absorption features (H$_2$O, CO$_2$, CH$_4$, O$_3$) appear as
wavelength-dependent modulations of this depth.

## References

- Kopparapu et al. (2013), ApJ, 765, 131 — habitable zone boundaries
- Zeng et al. (2016), ApJ, 819, 127 — mass-radius relation
- Fulton et al. (2017), AJ, 154, 109 — radius valley
- Seager (2010), Exoplanet Atmospheres

## Data provenance

See `docs/DATA_PROVENANCE.md` (workspace root) for the real/derived/synthetic classification.
