# Kerr-Newman ADM

The **ADM (Arnowitt–Deser–Misner) formalism** decomposes spacetime into
$3+1$ dimensions and extracts the conserved mass, angular momentum and charge
of a stationary black hole. For Kerr–Newman it yields the exact values
$M$, $J=aM$, $Q$ that label the solution (no-hair theorem). The full
derivation is in `premium/theory_kerr_newman_adm.md`.

## 3+1 decomposition

$$ds^2 = -N^2\,dt^2 + \gamma_{ij}(dx^i + N^i\,dt)(dx^j + N^j\,dt)$$

with lapse $N$, shift $N^i$ and spatial metric $\gamma_{ij}$. The
Einstein–Hilbert action becomes a constrained Hamiltonian system with
constraints $\mathcal H=0$, $\mathcal H_i=0$.

## Conserved charges

At spatial infinity the ADM mass, angular momentum and electric charge are

$$M_{\rm ADM} = \frac{1}{16\pi}\oint_{\infty} (\partial_j \gamma_{ij} - \partial_i \gamma_{jj})\,dS^i,$$

$$J = \frac{1}{8\pi}\oint_{\infty} \pi_{ij}\,\xi^j\,dS^i,$$

$$Q = \frac{1}{4\pi}\oint_{\infty} E^i\,dS_i,$$

where $\pi^{ij}$ is the conjugate momentum to $\gamma_{ij}$ and $E^i$ the
electric field. For Kerr–Newman these evaluate to $M$, $J=aM$, $Q$.

## Mass formula

The Smarr relation for Kerr–Newman:

$$M = 2\Omega_H J + \Phi_H Q + \frac{\kappa A}{4\pi},$$

with horizon angular velocity $\Omega_H$, electric potential $\Phi_H$,
surface gravity $\kappa$ and area $A$. The last term is the irreducible mass
contribution; the first two are extractable. This is the origin of the
$\sim 29.3\%$ rotational-energy reservoir.

## Cross-links

- [[Kerr-Newman Metric]] — the full solution
- [[Kerr Metric]] — the $Q=0$ limit
- [[Reissner-Nordström Metric]] — the $a=0$ limit
- [[Black Holes]] — overview of the four exact solutions
- [[Remnant Energetics]] — merger remnant spin and ISCO efficiency

Categories: Black Holes, Gravity & Spacetime