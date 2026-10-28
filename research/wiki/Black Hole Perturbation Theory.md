# Black Hole Perturbation Theory

Linearized perturbations around a black-hole background separate into
decoupled master equations. For [[Schwarzschild Metric]] and [[Kerr Metric]]
backgrounds, gravitational, electromagnetic and scalar perturbations reduce to
single scalar wave equations that govern ringdown, superradiance and
self-force. The full derivation lives in the premium page
`premium/theory_bh_perturbation.md`.

## Schwarzschild: Regge-Wheeler and Zerilli

Perturbations split under parity into **axial (odd)** and **polar (even)**
sectors. Each obeys a Schrödinger-like equation

$$\frac{d^2\psi}{dr_*^2} + (\omega^2 - V_\ell(r))\psi = 0,$$

with tortoise coordinate $dr_*/dr = 1/f(r)$, $f(r)=1-2M/r$. The axial
**Regge-Wheeler** potential and the polar **Zerilli** potential are different
but share the same quasi-normal mode spectrum — this is **isospectrality**:
axial and polar modes of the same $(\ell,m)$ have identical frequencies for
Schwarzschild.

## Kerr: Teukolsky formalism

In the Newman-Penrose formalism, perturbations of spin weight $s$ (scalar
$s=0$, neutrino $s=\pm 1/2$, electromagnetic $s=\pm 1$, gravitational
$s=\pm 2$) obey the **Teukolsky master equation**, which separates in
Boyer-Lindquist coordinates. The angular part gives spin-weighted spheroidal
harmonics ${}_sS_{\ell m}(\theta;a\omega)$; the radial part is a confluent
Heun equation. For $a=0$ it reduces to the Regge-Wheeler/Zerilli equations.

## Quasi-normal modes

Imposing outgoing waves at infinity and ingoing waves at the horizon yields a
discrete spectrum $\omega_{\ell m n} = \omega_R - i\,\omega_I$ (complex
frequency, positive imaginary part = damping). The fundamental mode
$(\ell,m,n)=(2,2,0)$ has $M\omega \approx 0.3737 - 0.0890\,i$ for
Schwarzschild. The **ringdown** observed in [[Gravitational Wave Analysis]] is
a superposition of these modes; their frequencies and damping times encode the
final mass and spin (black-hole spectroscopy, no-hair tests).

## Superradiance

A bosonic wave scattering off a rotating hole is amplified when
$\omega < m\Omega_H$ (the superradiant condition), extracting rotational
energy. Repeated reflection in a cavity (or a massive boson cloud) can trigger
a **black-hole bomb** instability, producing a gravitational-wave signal.

## Self-force

For extreme mass-ratio inspirals the smaller body's own field back-reacts on
its motion. The first-order self-force (MiSaTaQuWa) splits into a conservative
part (shifts the ISCO) and a dissipative part (radiation reaction). The
regularization of the singular self-field uses mode-sum or puncture schemes.

## Black-hole spectroscopy

The no-hair theorem predicts that the entire QNM spectrum is fixed by mass
and spin. Measuring two or more modes tests this; overtones (e.g. the
$n=1$ (2,2) mode) improve the test. Parametrized ringdown frameworks allow
model-independent deviations.

## Cross-links

- Background metrics: [[Schwarzschild Metric]], [[Kerr Metric]]
- Observations: [[Gravitational Wave Analysis]], [[Gravitational-Wave Catalogs]]
- Energy extraction: [[Remnant Energetics]], [[Black Hole Accretion]]
- Premium derivation: `premium/theory_bh_perturbation.md`

Categories: Black Holes, Gravity & Spacetime