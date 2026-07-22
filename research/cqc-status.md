# Review status and relation to known results

Status checked 2026-07-22 UTC.

Technical certificate: [cqc-counterexample.md](cqc-counterexample.md).
Detailed search record: [literature-search.md](literature-search.md).

## The conjecture and its formal scope

- Original statement: Schneeloch, Broadbent, and Howell, *Uncertainty
  relation for mutual information*, Phys. Rev. A 90, 062119 (2014),
  [arXiv:1404.6496](https://arxiv.org/abs/1404.6496).  Eq. (1) reads

  $$
  H(\hat Q^A{:}\hat Q^B)+H(\hat R^A{:}\hat R^B)\le I(A{:}B),
  $$

  with the $\hat Q$ pair an **arbitrary** pair of observables and the
  $\hat R$ observables required only to be mutually unbiased with the
  corresponding $\hat Q$ on each subsystem (footnote [11] defines mutual
  unbiasedness operationally: an eigenstate of one is equally likely to be
  measured in any eigenstate of the other).  The full text contains no
  restriction on state rank, support, or marginal spectrum.  The qutrit
  computational/Fourier pair satisfies the definition exactly; the
  counterexample is squarely inside the quantified domain.
- Cases proven in the original paper: pure states; states with one
  subsystem maximally mixed (entropy $\log N^A$ of the **full** space);
  minimally disturbing measurements (observable commuting with the reduced
  state, footnote [12]); asymmetric two-qubit Werner states.  The
  counterexample state evades all four: it is mixed, its marginals have
  spectrum $(1/2,1/2,0)$, its residual uncertainty
  $H(Z^A)+H(X^A)-\log_2 3-S(A)=0.41504$ is strictly positive, and
  $\rho_A$ has off-diagonal element $0.25$ in both measurement
  eigenbases.
- Their Monte Carlo search used $10^7$ Haar-random states in each of
  $2\otimes2$, $2\otimes3$, $3\otimes3$ and $10^6$ in
  $2\otimes4$, $3\otimes4$, $4\otimes4$, plus perturbed boundary
  states. The counterexample lives in $3\otimes3$, inside the sampled
  range, but was not encountered by that random search.
- Precedent noted in their footnote [17]: the analogous Lindblad
  conjecture was disproven by Luo and Zhang.

## Open status as of July 2026

- Iqbal, *On the CQC conjecture: a sufficient condition and an extension*,
  Quantum Information Processing 25, 250, published 2026-07-10
  ([arXiv:2509.08286](https://arxiv.org/abs/2509.08286),
  [journal](https://link.springer.com/article/10.1007/s11128-026-05258-2)),
  states explicitly that the conjecture "still remains open." Its simulations
  in dimensions 3 and 5 concern the proposed ECQC extension and should not be
  described as a new broad simulation of the original two-basis conjecture.

## Interaction with proven results and with Iqbal's extension

Computed in `scripts/verify_cqc_mpmath.py`; all values for the rank-2
certificate state:

- Iqbal Proposition 3 sufficient condition
  $I(Z^A{:}B)-I_Z+I(X^A{:}B)-I_X\ge\log d-H(A)$: LHS $=0.02333$,
  RHS $=0.58496$.  The condition **fails** on this state, as it must —
  it provably implies CQC.
- Coles–Piani bound $I(Z^A{:}B)+I(X^A{:}B)\le\log d-S(A|B)$: holds with
  slack $0.51432$.  No proven theorem is violated; only the conjectured
  universal statement fails.
- Extended conjecture ECQC (Iqbal Conjecture 3.1, all $d+1=4$ qutrit
  MUBs, minimum over size-3 subsets of the per-MUB classical mutual
  informations): the two extra MUBs carry almost no correlation
  ($0.05192$ bits each), the minimizing subset sums to $0.89300 <
  I(A{:}B)=1.53100$, so **ECQC is not violated** — margin $-0.63800$,
  and $-0.63169$ for the 1%-white-noise full-rank state.  Notably the
  subset $\{Z,X,M_2\}$ sums to $1.63024 > I(A{:}B)$; ECQC survives
  because the minimizing triple excludes one of the two high-mutual-information
  bases. This construction therefore does not violate ECQC, which remains the
  natural surviving refinement.

## Novelty sweep

- Search methods included exact-phrase and keyword searches for the CQC
  conjecture and displayed inequality, targeted arXiv and web searches,
  Crossref and DOI metadata, and the citation records returned by OpenAlex and
  Semantic Scholar for `10.1103/PhysRevA.90.062119`. At search time,
  Crossref reported seven citing works, OpenAlex eight, and Semantic Scholar
  five. The union was inspected. Coverage is necessarily incomplete: recent,
  unindexed, non-English, or differently named work may have been missed.
- Wu, Poulsen, and Mølmer,
  [Phys. Rev. A 80, 032319 (2009)](https://doi.org/10.1103/PhysRevA.80.032319),
  proved complementary-measurement information bounds with Bob's POVM held
  fixed while Alice changes basis. That is not the CQC setup, where both
  parties switch local measurements, and it neither states nor supplies this
  counterexample.
- The indexed trail included work on uncertainty with quantum memory,
  high-dimensional entanglement certification, entropic uncertainty reviews,
  Wehrl entropy, classical entropies in a condensate, the 2022 fixed-purity
  study, and Iqbal's 2026 paper. None reported a counterexample to the original
  CQC inequality. The similarly titled “Complementary quantum correlations
  among multipartite systems” concerns monogamy and polygamy of correlation
  measures and is a terminology collision.
- Iqbal (above) treats the original conjecture as open and gives no
  counterexample. Alsing, Tison, Schneeloch, Birrittella, and Fanto,
  [arXiv:2205.01723](https://arxiv.org/abs/2205.01723)
  (Phys. Rev. Research 4, 043114 (2022)): fixed-purity sampling of the CQC
  relation **only for two qubits**, all points inside the conjectured
  triangle, no violation — and $2\otimes2$ is exactly where the
  subspace mechanism is unavailable.
- Targeted web searches for a published counterexample, violation, or
  disproof of the CQC relation found nothing.
- Not conclusive: a manual Google Scholar pass and direct contact with
  Schneeloch, Broadbent, Howell, and Iqbal remain the outstanding steps
  before any public priority claim.

## Current claim

> The attached certificate exactly violates the published CQC inequality. A
> targeted search of exact terminology, arXiv, Crossref, OpenAlex, Semantic
> Scholar, and the citation records returned for the original paper through
> July 22, 2026 found no earlier counterexample. This does not establish
> novelty or priority; independent expert and author review is pending.

## Verification status

Three separately implemented programs agree to at least 20 significant digits
(`scripts/verify_cqc_numpy.py`, `scripts/verify_cqc_exact.py`,
`scripts/verify_cqc_mpmath.py`). The technical note also gives a direct
algebraic derivation of the probability tables and sign certificate. The sign
of the violation
reduces to the integer inequality $29^{58}>3^{114}\cdot10^{30}$, checked
in exact integer arithmetic. The exact verifier now also derives the
full-rank state and marginal spectra and both measurement tables directly,
then proves the 1%-white-noise gap positive through the exact certificate

$$
36000\Delta_{\mathrm{full}}=\log_2(N/D),\qquad N>D,
$$

with the prime factorizations of $N$ and $D$ displayed in
[cqc-counterexample.md](cqc-counterexample.md).


## Provenance of the certificate

The construction, derivation, explanatory text, and initial verification
artifacts were generated by OpenAI GPT-5.6 Pro in a prompted exchange. The
three Python checks and Mathematica notebook were produced within the same
model-assisted workflow: their agreement is useful corroboration, but not
independent expert replication. The human repository steward supplied the
initial prompt and follow-up questions, preserves the record, and does not
claim mathematical authorship or independent verification. See
[`../PROVENANCE.md`](../PROVENANCE.md).
