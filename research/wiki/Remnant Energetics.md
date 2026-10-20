# Remnant Energetics

How much rotational energy survives a binary black-hole merger, and what
radiative efficiency does the remnant spin imply? This page records the
population-level answer for the GWTC catalogue and the assumptions behind it.

## Definitions

For a Kerr black hole of mass $M$ and dimensionless spin
$a_* = Jc/(GM^2)$, the prograde innermost stable circular orbit is given by the
Bardeen–Press–Teukolsky solution:

$$r_{\rm ISCO} = \frac{GM}{c^2}\left[3 + Z_2 - \sqrt{(3-Z_1)(3+Z_1+2Z_2)}\right],$$

with

$$Z_1 = 1 + (1-a_*^2)^{1/3}\left[(1+a_*)^{1/3}+(1-a_*)^{1/3}\right],
\qquad Z_2 = \sqrt{3a_*^2+Z_1^2}.$$

The specific orbital energy at the ISCO defines the thin-disc efficiency

$$\eta = 1 - E_{\rm ISCO}(a_*),$$

which rises from $\eta = 0.0572$ for Schwarzschild to
$\eta = 1-1/\sqrt{3} = 0.4226$ as $a_* \to 1$. The value $0.4226$ is a hard
upper bound for a Kerr horizon.

The irreducible mass follows from Christodoulou's relation,

$$\frac{M_{\rm irr}}{M} = \sqrt{\frac{1+\sqrt{1-a_*^2}}{2}},$$

so the rotational reservoir is $E_{\rm rot} = (M-M_{\rm irr})c^2$.

## Population estimate

The catalogue supplies component masses and the effective inspiral spin
$\chi_{\rm eff}$, but not the final spin. We estimate it with the aligned-spin
fit of Rezzolla et al. (2008), setting $\chi_1=\chi_2=\chi_{\rm eff}$:

$$a_f = \frac{(1+q^2)\chi_{\rm eff} + q\,\ell}{(1+q)^2},
\qquad \ell = 2\sqrt{3} + t_2\eta + t_3\eta^2,$$

where $q=m_1/m_2 \ge 1$, $\eta=q/(1+q)^2$, $t_2=-3.517$ and $t_3=2.576$.

For 270 GWTC events with complete masses and spins:

| quantity | value |
|---|---|
| median inferred spin | $a_* = 0.690$ |
| 90th percentile spin | $0.774$ |
| maximum spin | $0.930$ |
| median efficiency | $\eta = 0.102$ |
| 10–90% efficiency range | $0.092$–$0.116$ |
| fraction with $a_*>0.9$ | 1.1% |
| median rotational energy | $3.9\,M_\odot c^2$ |
| total rotational reservoir | $\approx 1140\,M_\odot c^2$ |
| mean Schwarzschild/Kerr ISCO ratio | $1.76$ |

## Interpretation

1. The population is **modestly spinning**. The median efficiency is about
   twice the Schwarzschild value but far below the Kerr bound; the data do not
   support a population of routinely near-extremal remnants.
2. Using the Schwarzschild ISCO $6GM/c^2$ for every remnant **overestimates**
   the true radius by 1.76× on average and by up to 2.85× for the fastest
   remnants. Any accretion or ringdown calculation that assumes $a_*=0$ is
   therefore biased.
3. The rotational reservoir is **large compared with the gravitational-wave
   output**: the median remnant retains several $M_\odot c^2$ of rotational
   energy, so spin-down channels have substantial energy available.
4. No event **requires** $\eta>0.4226$ under the adopted spin fit. This is a
   null result: it is consistent with Kerr, not evidence for it.

## Caveats

The final spin is a point estimate from $\chi_{\rm eff}$, not a posterior
sample; individual spins and precession are ignored. The efficiency is the
thin-disc value at the prograde ISCO, not an observed bolometric efficiency.
Conclusions are population-level.

## See also

- [Kerr Metric](Kerr%20Metric.md) — ISCO, ergosphere, energy extraction.
- [Black Hole Accretion](Black%20Hole%20Accretion.md) — thin-disc efficiency.
- [Hawking Radiation](Hawking%20Radiation.md) — the other channel that taps
  the remnant mass.
- [Gravitational-Wave Catalogs](Gravitational-Wave%20Catalogs.md) — the input
  catalogue.

## Source

- Script: `research/projects/exotic-compact-objects/scripts/remnant_energetics.py`
- Notebook: `notebooks/27_remnant_energetics.ipynb`
- Report: `reports/remnant_energetics.md`
- Figure: `premium/figures/remnant_energetics.html`
