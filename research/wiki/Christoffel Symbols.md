# Christoffel Symbols

Christoffel symbols encode the affine connection of a spacetime and are the
first step in computing geodesics, curvature, and tidal forces.

## Definition

Given a metric $g_{\mu\nu}$ with inverse $g^{\mu\nu}$,

$$\Gamma^\lambda_{\mu\nu} = \frac12 g^{\lambda\sigma}\left(\partial_\mu g_{\nu\sigma}+\partial_\nu g_{\mu\sigma}-\partial_\sigma g_{\mu\nu}\right).$$

They are symmetric in the lower indices, $\Gamma^\lambda_{\mu\nu}=\Gamma^\lambda_{\nu\mu}$.

## Schwarzschild

For [[Schwarzschild Metric]], with $A=e^{2\alpha}$ and $B=e^{2\beta}$, the
non-vanishing components include

$$\Gamma^t_{\ tr}=\alpha', \quad \Gamma^r_{\ tt}=\alpha'\frac{A}{B}, \quad
\Gamma^r_{\ rr}=\beta', \quad \Gamma^r_{\ \theta\theta}=-\frac{r}{B}, \quad
\Gamma^\theta_{\ r\theta}=\frac1r, \quad \Gamma^\phi_{\ r\phi}=\frac1r.$$

These are the building blocks for the vacuum field equations and for the tidal
acceleration.

## Kerr

For [[Kerr Metric]] the determinant is $\det g=-\rho^4\sin^2\theta$ and the
inverse metric has $g^{rr}=\Delta/\rho^2$, $g^{\theta\theta}=1/\rho^2$,
$g^{tt}=-[(r^2+a^2)^2-a^2\Delta\sin^2\theta]/(\rho^2\Delta)$, and
$g^{t\phi}=-2Mra/(\rho^2\Delta)$. There are 20 independent (48 with symmetry)
non-zero components. For example,

$$\Gamma^r_{\ tt} = \frac{M(r^2-a^2\cos^2\theta)\Delta}{\rho^6}, \qquad
\Gamma^r_{\theta\theta}=-\frac{r\Delta}{\rho^2}, \qquad
\Gamma^\theta_{\ r\theta}=\frac{r}{\rho^2}.$$

In the Schwarzschild limit $a\to0$ these reduce to the expressions above, and as
$M,a\to0$ they reduce to the spherical-coordinate symbols of flat space. The
symbols feed directly into [[Geodesic Equations]] and the
[[Raychaudhuri Equation]].

See also: [[Kerr Metric]], [[Schwarzschild Metric]], [[Geodesic Equations]], [[Raychaudhuri Equation]]

Categories: Gravity & Spacetime
