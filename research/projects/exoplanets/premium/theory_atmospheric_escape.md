# Atmospheric Escape from Exoplanets

**A Self-Contained Derivation**

SI units with $G$, $k_B$, $m_p$ explicit. Distances outward positive. Model-dependent
scalings are marked.

---

## 1. Jeans escape

The escape velocity from a planet of mass $M_p$ and radius $R_p$ is

$$v_{\rm esc} = \sqrt{\frac{2 G M_p}{R_p}}.$$

The most probable thermal speed of a species of mass $m$ at temperature $T$ is

$$v_{\rm th} = \sqrt{\frac{2 k_B T}{m}}.$$

The Jeans escape parameter is

$$\lambda = \frac{v_{\rm esc}^2}{v_{\rm th}^2}
          = \frac{G M_p m}{k_B T R_p}.$$

Escape is significant when $\lambda \lesssim 10$–$15$. The Jeans escape flux
(molecules m$^{-2}$ s$^{-1}$) is $\Phi_J \propto n v_{\rm th}(1+\lambda)e^{-\lambda}/(2\sqrt{\pi})$.

## 2. Energy-limited mass loss

For XUV-heated upper atmospheres, the mass-loss rate is

$$\dot M = \frac{\epsilon\,\pi R_p^3 F_{\rm XUV}}{G M_p K_{\rm tide}},$$

where $\epsilon$ is the heating efficiency ($\sim 0.1$–$0.3$), $F_{\rm XUV}$ the
stellar XUV flux at the planet, and $K_{\rm tide}$ the tidal correction. The
tidal factor (Erkaev et al. 2007) accounts for the reduced potential well near
the Roche lobe:

$$K_{\rm tide} = 1 - \frac{3}{2\xi} + \frac{1}{2\xi^3},\qquad
\xi = \frac{R_{\rm Roche}}{R_p}\approx\frac{R_{\rm Hill}}{R_p}.$$

Smaller $K_{\rm tide}$ (more tidal assistance) occurs for close-in planets.

## 3. Hydrodynamic escape (blow-off)

When XUV heating is strong relative to gravity, the atmosphere enters a
hydrodynamic regime: a bulk outflow with a sonic point, described by
Parker-wind-like solutions. The transition from Jeans to hydrodynamic escape
occurs for small $\lambda$ and high XUV fluxes. Blow-off can strip H/He
envelopes from mini-Neptunes, producing super-Earths.

## 4. XUV flux evolution

Stellar XUV luminosity decays with age. Empirical scalings (model-dependent):

$$L_{\rm XUV}/L_{\rm bol} \propto t^{-1.0\text{ to }-1.4}\quad (t\gtrsim 100\ {\rm Myr}),$$

with saturation at $L_{\rm X}/L_{\rm bol}\sim 10^{-3}$ for young stars. Thus
escape is most vigorous in the first $\sim 100$ Myr, and integrated mass loss
depends on the early XUV history (often unknown for individual stars).

## 5. Radius valley connection

The observed radius valley (Fulton gap) at $\sim 1.5$–$2.0\,R_\oplus$ is
explained by atmospheric loss:

- **Photoevaporation**: XUV-driven escape strips H/He from planets below a
  mass threshold, leaving rocky cores.
- **Core-powered mass loss**: luminosity of the cooling core drives escape.

Both predict a valley; discriminating them uses radius–period dependence and
stellar age. Photoevaporation predicts stronger radius dependence on orbital
period.

## 6. Scale height and transmission spectroscopy

The (isothermal) scale height is

$$H = \frac{k_B T}{\mu m_p g},$$

with mean molecular weight $\mu$ and surface gravity $g=GM_p/R_p^2$. The
transit-depth variation due to the atmosphere is

$$\frac{\Delta F}{F} = \frac{2 R_p H}{R_*^2}.$$

Molecular absorption (H$_2$O, CO$_2$, CH$_4$, O$_3$) modulates this depth
with wavelength, enabling transmission spectroscopy.

## References

- Jeans (1925), The Dynamical Theory of Gases
- Watson et al. (1981), Icarus, 48, 150 — energy-limited escape
- Erkaev et al. (2007), A&A, 472, 329 — tidal correction $K_{\rm tide}$
- Lammer et al. (2003), SSRv, 109, 3 — hydrodynamic escape
- Jackson et al. (2012), ApJ, 745, 54 — XUV evolution
- Fulton et al. (2017), AJ, 154, 109 — radius valley
- Owen & Wu (2017), ApJ, 847, 29 — photoevaporation
- Ginzburg et al. (2018), MNRAS, 476, 759 — core-powered mass loss
- `models/equations.py` — `escape_velocity`, `thermal_velocity`, `scale_height`
