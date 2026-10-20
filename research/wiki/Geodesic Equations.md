# Geodesic Equations

The motion of test particles and light in a black-hole spacetime is governed by
the geodesic equation

$$\frac{d^2 x^\mu}{d\lambda^2} + \Gamma^\mu_{\nu\rho}\frac{dx^\nu}{d\lambda}\frac{dx^\rho}{d\lambda}=0,$$

where $\lambda$ is an affine parameter. For the Schwarzschild and Kerr metrics
this equation is integrable because enough conserved quantities exist.

## Conserved quantities and the effective potential

For [[Schwarzschild Metric]] the Lagrangian
$\mathcal L=\tfrac12 g_{\mu\nu}\dot x^\mu\dot x^\nu$ gives energy
$E=f(r)\dot t$ and angular momentum $L_z=r^2\sin^2\theta\,\dot\phi$. The
normalization condition yields a one-dimensional radial equation with the
effective potential

$$V_{\rm eff}(r) = f(r)\left(\epsilon+\frac{L^2}{r^2}\right), \qquad f(r)=1-\frac{2M}{r},$$

where $\epsilon=-1$ for timelike and $0$ for null geodesics. Circular orbits
satisfy $dV_{\rm eff}/dr=0$, giving $L^2=Mr^2/(r-3M)$; marginal stability gives
the ISCO $r=6M$. The same machinery yields the photon sphere $r=3M$ and the
pericenter advance $\Delta\phi=6\pi M/[a(1-e^2)]$.

## Kerr and the Carter constant

For [[Kerr Metric]] stationarity and axisymmetry give $E$ and $L_z$, while a
hidden symmetry (a rank-2 Killing tensor) provides the Carter constant

$$\mathcal Q = p_\theta^2 + (L_z\csc\theta - aE\sin\theta)^2 + \epsilon a^2\cos^2\theta.$$

The Hamilton–Jacobi equation then separates, giving

$$\rho^4\dot r^2 = R(r), \qquad \rho^4\dot\theta^2 = \Theta(\theta),$$

with quartic radial potential $R(r)$ and polar potential $\Theta(\theta)$.
Mino time $d\lambda=d\tau/\rho^2$ decouples the two motions entirely. Equatorial
ISCO radii are given by the Bardeen formula. These same null geodesics set the
shadow size used in [[Gravitational Wave Analysis]] and catalog
[[Gravitational-Wave Catalogs]] tests.

See also: [[Schwarzschild Metric]], [[Kerr Metric]], [[Christoffel Symbols]], [[Gravitational Wave Analysis]], [[Gravitational-Wave Catalogs]]

Categories: Gravity & Spacetime
