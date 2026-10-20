# Reissner-Nordström Metric

The Reissner–Nordström solution describes a static, spherically symmetric black
hole with mass $M$ and electric charge $Q$. It is the charged generalization of
the Schwarzschild metric.

## Einstein–Maxwell solution

Starting from the Einstein–Maxwell action and a static, spherically symmetric
ansatz $ds^2=-f(r)dt^2+f(r)^{-1}dr^2+r^2 d\Omega^2$ with $A_t=-Q/r$, the field
equations give

$$f(r) = 1 - \frac{2GM}{r} + \frac{GQ^2}{r^2}.$$

The horizons are the roots of $f(r)=0$:

$$r_\pm = GM \pm \sqrt{G^2M^2 - GQ^2},$$

with $r_+$ the event horizon and $r_-$ the Cauchy horizon. The three regimes are
subextremal ($GM^2>Q^2$), extremal ($GM^2=Q^2$, $r_+=r_-=GM$), and
superextremal ($GM^2<Q^2$, a naked singularity forbidden by cosmic censorship).
At extremality the near-horizon geometry is $AdS_2\times S^2$.

## Thermodynamics

The surface gravity and Hawking temperature are

$$\kappa = \frac{r_+-r_-}{2r_+^2}, \qquad
T_H = \frac{r_+-r_-}{4\pi r_+^2},$$

and the Bekenstein–Hawking entropy is $S=\pi r_+^2/G$. The first law and Smarr
formula are

$$dM = \frac{\kappa}{8\pi G}dA + \Phi_+ dQ, \qquad
M = 2T_H S + \Phi_+ Q,$$

with $\Phi_+=Q/r_+$. The heat capacity $C_Q$ diverges at $r_+^2=3GQ^2$
(Davies phase transition). A charged hole can also discharge by Schwinger pair
production, $dQ/dt \sim -(e^3Q/\pi^2 r_+^2)\exp(-\pi m_e^2 r_+^2/eQ)$.

## Rotating and charged black holes

Adding rotation yields [[Kerr-Newman Metric]]; the uncharged, non-rotating limit
is [[Schwarzschild Metric]]. Horizon structure and quantum emission connect to
[[Hawking Radiation]], and the connection components used in dynamics are in
[[Christoffel Symbols]].

See also: [[Kerr-Newman Metric]], [[Schwarzschild Metric]], [[Hawking Radiation]], [[Christoffel Symbols]]

Categories: Black Holes, Gravity & Spacetime
