# Kerr Metric

The Kerr metric is the unique stationary, axisymmetric vacuum solution of
Einstein's equations: a rotating black hole of mass $M$ and angular momentum
$J=acM$. It is the geometry that real astrophysical black holes are expected
to approximate.

## Line element

In Boyer–Lindquist coordinates $(t,r,\theta,\phi)$, with

$$\rho^2 = r^2 + \frac{a^2}{c^2}\cos^2\theta, \qquad
\Delta = r^2 - \frac{2GMr}{c^2} + \frac{a^2}{c^2},$$

the line element is

$$ds^2 = -\left(1-\frac{2GMr}{\rho^2 c^2}\right)c^2 dt^2
-\frac{4GMar\sin^2\theta}{\rho^2 c}\,dt\,d\phi
+\frac{\rho^2}{\Delta}dr^2 + \rho^2 d\theta^2
+\left(r^2+\frac{a^2}{c^2}+\frac{2GMa^2 r\sin^2\theta}{\rho^2 c^4}\right)\sin^2\theta\,d\phi^2.$$

The dimensionless spin is $a_* = ac^2/(GM)=Jc/(GM^2)\in[0,1]$.

## Horizons and ergosphere

The horizons are the roots of $\Delta=0$:

$$r_\pm = \frac{GM}{c^2}\left(1\pm\sqrt{1-a_*^2}\right),$$

where $r_+$ is the event horizon and $r_-$ the inner (Cauchy) horizon. For
$a_*>1$ no horizon exists, which cosmic censorship forbids. The ergosphere
lies between $r_+$ and the static limit $r_{\rm erg}(\theta)$, where $g_{tt}=0$:

$$r_{\rm erg}(\theta) = \frac{GM}{c^2}+\sqrt{\left(\frac{GM}{c^2}\right)^2-\frac{a^2}{c^2}\cos^2\theta}.$$

Inside, no observer can remain static; frame dragging forces co-rotation.

## ISCO and energy extraction

The Bardeen–Press–Teukolsky ISCO is

$$r_{\rm ISCO} = \frac{GM}{c^2}\left[3+Z_2\mp\sqrt{(3-Z_1)(3+Z_1+2Z_2)}\right],$$

with $Z_1 = 1+(1-a_*^2)^{1/3}[(1+a_*)^{1/3}+(1-a_*)^{1/3}]$ and
$Z_2=\sqrt{3a_*^2+Z_1^2}$. The upper sign is prograde. For $a_*=0$ this gives
$6GM/c^2$; for $a_*=1$ prograde, $GM/c^2$.

> **Approximation warning.** A straight-line chord between $6M$ and $1M$ (the common
> $6-5a$ form) is wrong by up to ~36% near $a_*\approx0.93$, because the exact curve is
> concave; and quoting the ISCO in units of the Schwarzschild radius $r_s=2M$ instead of
> $M=GM/c^2$ doubles the result. Use the exact BPT form for quantitative work.
> (Verified numerically; see `research/projects/black-holes-wormholes/reports/isco_validation.md`.) Rotational energy can be extracted
through the Penrose process and through superradiance, $\omega < m\Omega_H$
with $\Omega_H = a_*c^3/[2GM(1+\sqrt{1-a_*^2})]$.

See also: [[Schwarzschild Metric]], [[Kerr-Newman Metric]], [[Geodesic Equations]], [[Christoffel Symbols]], [[Hawking Radiation]], [[Raychaudhuri Equation]]

Categories: Black Holes, Gravity & Spacetime
