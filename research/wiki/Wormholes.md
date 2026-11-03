# Wormholes

A wormhole is a topological shortcut connecting two regions of spacetime. The
modern theory of traversable wormholes begins with Morris and Thorne (1988),
and it shows that such objects require exotic matter violating the null energy
condition (NEC).

## Morris–Thorne metric

The general static, spherically symmetric traversable metric is

$$ds^2 = -e^{2\Phi(r)}c^2 dt^2 + \frac{dr^2}{1-b(r)/r} + r^2 d\Omega^2,$$

where $\Phi(r)$ is the redshift function and $b(r)$ the shape function. The
throat is the minimum of the areal radius, where $b(r_0)=r_0$. Asymptotic
flatness requires $\Phi\to0$ and $b/r\to0$ as $r\to\infty$.

## Flare-out and exotic matter

Embedding the equatorial slice in $\mathbb R^3$ gives
$dz/dr=\pm\sqrt{r/b(r)-1}$, and the throat must flare outward:

$$\frac{d^2 r}{dz^2}>0 \quad\Longrightarrow\quad b'(r_0)<1.$$

The Einstein equations give an anisotropic fluid with
$\rho c^2 = (c^4/8\pi G)\,b'/r^2$. At the throat with $\Phi(r_0)=0$,

$$\rho c^2 + p_r\big|_{r_0} = \frac{c^4}{8\pi G}\frac{b'(r_0)-1}{r_0^2}<0,$$

so the NEC is violated and all stronger energy conditions fail. The violation
is enormous: for $r_0=1$ m and $b'(r_0)=0$, $|\rho c^2+p_r|\approx4.8\times10^{42}$ J/m$^3$.

## Research result (2026-10-28)

For the simplest shape function $b(r)=b_0^2/r$ with throat $r_0=b_0=1$ km:
- Flare-out: $b'(r_0)=-1<1$ ✓
- NEC violation at throat: $\rho+p_r \approx -0.0796$ (geometric units) ✓
- Exotic matter integral: $I = \int_{r_0}^{\infty}(\rho+p_r)\,4\pi r^2/\sqrt{1-b/r}\,dr \approx -9021$
  (negative → exotic matter required)

Figure: `figures/wormhole_flare_out.png` (shape function, NEC violation,
exotic matter integrand, embedding diagram).

## Traversability, thin shells, and time travel

Traversability requires no horizon ($\Phi$ finite) and tolerable tidal forces.
Visser's thin-shell construction concentrates the exotic matter on a
codimension-1 shell, minimizing the total amount. Quantum inequalities
constrain how long exotic matter can persist, suggesting Planck-scale throats
for known fields. A moving mouth can produce closed timelike curves, but
Hawking's chronology protection conjecture argues that vacuum polarization
destroys the wormhole first.

## Observational signatures

Wormholes differ from black holes ([[Schwarzschild Metric]]) in shadow size,
lensing (roughly half the Schwarzschild deflection), absence of an event
horizon, and gravitational-wave echoes. Echoes connect to
[[Gravitational Wave Analysis]], and the exotic-matter requirement connects to
[[Quantum Gravity]]. A wormhole is not a white hole ([[White Holes]]), though
both are time-related curiosities.

See also: [[Schwarzschild Metric]], [[White Holes]], [[Raychaudhuri Equation]], [[Gravitational Wave Analysis]], [[Quantum Gravity]]

## Traversal physics (2026-11-03)

Phase F research thread: traversal proper time, tidal constraints, exotic-matter
budget, and quantum-inequality position. Full derivation in
`premium/theory_wormhole_traversal.md`; report in `reports/wormhole_traversal.md`.

- Traversal time (Ellis, $L=10b_0$): $\Delta\tau \approx 6.64\times10^{-7}\,b_0/{\rm m}$ s at $0.1c$.
- Tidal safety requires $b_0 \gtrsim 10^7$–$10^8$ m for a 2 m traveler.
- Exotic budget: $M_{\rm eq}/M_\odot = 1.063775\times10^{-3}\,b_0/{\rm m}$ (Ellis).
- QI ceiling $b_{0,{\rm QI}}\approx 0.49\,l_P$; ANEC integral $-5/(64b_0)<0$.
- EHT anchors: Sgr A* / M87* shadow predictions 17.8 / 13.2 μas (predictions, not detections).

Categories: Wormholes
