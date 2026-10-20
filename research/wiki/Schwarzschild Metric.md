# Schwarzschild Metric

The Schwarzschild metric is the unique spherically symmetric vacuum solution of
Einstein's field equations (Birkhoff's theorem). It describes the exterior
spacetime of any non-rotating, uncharged mass and is the simplest black-hole
geometry.

## Metric and horizon

The most general static, spherically symmetric line element can be written
$ds^2 = -e^{2\alpha(r)}c^2 dt^2 + e^{2\beta(r)}dr^2 + r^2 d\Omega^2$. Imposing
$R_{\mu\nu}=0$ and asymptotic flatness gives $\alpha = -\beta$ and

$$ds^2 = -\left(1 - \frac{2GM}{rc^2}\right)c^2 dt^2 + \left(1 - \frac{2GM}{rc^2}\right)^{-1}dr^2 + r^2 d\Omega^2$$

with Schwarzschild radius

$$R_s = \frac{2GM}{c^2}.$$

For the Sun, $R_s \approx 2.95$ km.

## Singularity and curvature

At $r=R_s$ the metric is degenerate, but this is a coordinate singularity: the
Kretschmann scalar

$$K = R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma} = \frac{48 G^2 M^2}{c^4 r^6}$$

is finite there. At $r=0$, $K\to\infty$, which is a true curvature singularity.
Kruskal–Szekeres coordinates remove the horizon coordinate singularity and
reveal four regions, including the black-hole interior and the white-hole
region of [[White Holes]].

## Orbits and key radii

Conserved energy $E=(1-R_s/r)c^2 \dot t$ and angular momentum $L=r^2\dot\phi$
give the effective potential

$$V_{\rm eff}(r) = c^2\left(1-\frac{R_s}{r}\right)\left(1+\frac{L^2}{c^2 r^2}\right).$$

Circular photon orbits (the photon sphere) sit at $r_{\rm ph}=3GM/c^2=1.5R_s$,
and the innermost stable circular orbit (ISCO) at $r_{\rm ISCO}=6GM/c^2=3R_s$.
Tidal acceleration across a body of size $\ell$ is
$a_{\rm tidal}=2GM\ell/r^3$, which for a solar-mass hole at the horizon is
$\sim 2\times10^8 g$.

## Where to go next

The charged generalization is [[Reissner-Nordström Metric]]; adding rotation
gives [[Kerr Metric]] and, with both, [[Kerr-Newman Metric]]. Orbital motion is
treated in [[Geodesic Equations]], and quantum emission in
[[Hawking Radiation]].

See also: [[Kerr Metric]], [[Geodesic Equations]], [[Hawking Radiation]],
[[White Holes]], [[Gravitational Wave Analysis]]

Categories: Black Holes, Gravity & Spacetime
