# Fisher Information Matrix

The Fisher information matrix (FIM) estimates parameter uncertainties for
gravitational-wave signals. In the high signal-to-noise limit the posterior is
approximately Gaussian with covariance equal to the inverse Fisher matrix.

## Inner product and definition

Detector noise is described by a one-sided power spectral density $S_n(f)$, and
the noise-weighted inner product is

$$(a|b) = 4\Re\int_{f_{\min}}^{f_{\max}}\frac{\tilde a(f)\tilde b^*(f)}{S_n(f)}\,df.$$

The signal-to-noise ratio is $\rho=\sqrt{(h|h)}$. For a signal
$h(\theta)$ with parameters $\theta^i$, the Fisher matrix is

$$\Gamma_{ij} = \left(\frac{\partial h}{\partial\theta^i}\middle|\frac{\partial h}{\partial\theta^j}\right),
\qquad \Sigma^{ij}=(\Gamma^{-1})^{ij},$$

with 1-$\sigma$ errors $\sigma_{\theta^i}=\sqrt{\Sigma^{ii}}$.

## Waveform derivatives and degeneracies

Writing $\tilde h=Ae^{i\Psi}$, the derivative splits into amplitude and phase
parts,

$$\frac{\partial\tilde h}{\partial\theta^i}=\left(\frac{\partial\ln A}{\partial\theta^i}+i\frac{\partial\Psi}{\partial\theta^i}\right)\tilde h.$$

The chirp mass dominates the phase, $\partial\Psi/\partial\mathcal M_c\propto f^{-8/3}$,
so it is measured best; the symmetric mass ratio and effective spin enter at
higher post-Newtonian orders and are strongly degenerate
($\rho_{\mathcal M_c\eta}\approx0.9$–$0.99$). Distance and inclination are
degenerate for a single detector but broken by a network. These forecasts feed
[[Gravitational Wave Analysis]] and are applied to the events in
[[Gravitational-Wave Catalogs]]; the underlying waveforms come from
[[Kerr Metric]] ringdown.

See also: [[Gravitational Wave Analysis]], [[Gravitational-Wave Catalogs]], [[Kerr Metric]]

Categories: Methods, Observations & Catalogs
