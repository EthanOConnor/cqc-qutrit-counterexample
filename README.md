# Exact certificate for a candidate qutrit counterexample to the CQC conjecture

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21499723.svg)](https://doi.org/10.5281/zenodo.21499723)

> **Review status and provenance.** This is a machine-originated candidate
> counterexample. OpenAI GPT-5.6 Pro generated the construction, derivation,
> exposition, and initial verification artifacts in response to a research
> prompt from Ethan O'Connor. O'Connor is preserving and communicating the
> artifact but does not claim mathematical authorship, discovery credit, or
> independent verification. The included exact and numerical checks were
> generated in the same model-assisted workflow; specialist review of
> correctness, scope, novelty, and priority is pending. See
> [`PROVENANCE.md`](PROVENANCE.md).

Schneeloch, Broadbent, and Howell conjectured that, for any bipartite state
and locally mutually unbiased measurement pairs,

$$
I(Z^A{:}Z^B)+I(X^A{:}X^B)\le I(A{:}B).
$$

The original statement is in
[“Uncertainty relation for mutual information,” *Physical Review A* 90,
062119 (2014)](https://doi.org/10.1103/PhysRevA.90.062119).

This repository gives an explicit state on
$\mathbb C^3\otimes\mathbb C^3$ for which the inequality is reversed.

## The certificate in brief

Inside each qutrit, set

$$
|0_L\rangle=|0\rangle,
\qquad
|1_L\rangle=\frac{|1\rangle+|2\rangle}{\sqrt2}.
$$

For two explicitly given, orthogonal maximally entangled states
$|\phi\rangle$ and $|\chi\rangle$ on this logical-qubit support, take

$$
\rho=\frac9{10}|\phi\rangle\!\langle\phi|
     +\frac1{10}|\chi\rangle\!\langle\chi|.
$$

Measuring both parties in either the qutrit computational basis or the qutrit
Fourier basis gives the same exact joint table:

$$
P_Z=P_X=
\begin{pmatrix}
29/60&1/120&1/120\\
1/120&29/240&29/240\\
1/120&29/240&29/240
\end{pmatrix}.
$$

Consequently,

$$
\begin{aligned}
I(Z^A{:}Z^B)&=I(X^A{:}X^B)=1-h_2(1/30),\\
I(A{:}B)&=2-h_2(1/10),\\
\Delta&=h_2(1/10)-2h_2(1/30)\\
&=0.0473109929522169\ \text{bits}>0.
\end{aligned}
$$

The sign is certified without floating-point arithmetic by

$$
30\Delta=\log_2\!\left(\frac{29^{58}}{3^{114}10^{30}}\right),
\qquad
29^{58}>3^{114}10^{30}.
$$

An explicit one-percent white-noise perturbation has full rank and retains a
$0.0369567802161937$-bit violation. Its sign also has an exact integer
certificate, so the effect is not confined to the rank-deficient boundary.

The complete derivation, including the definitions of $|\phi\rangle$ and
$|\chi\rangle$, is in
[`research/cqc-counterexample.md`](research/cqc-counterexample.md).

## Fast verification

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/verify_cqc_exact.py
```

The exact verifier reconstructs the state, partial traces, qutrit MUBs,
logical-support reduction, both probability tables, entropies, full-rank
perturbation, and both integer sign certificates. A successful run prints:

```text
main exact sign certificate: True
full-rank exact sign certificate: True
```

Two structurally separate checks are also included:

```sh
.venv/bin/python scripts/verify_cqc_numpy.py
.venv/bin/python scripts/verify_cqc_mpmath.py
```

The mpmath check starts from separately entered physical-basis amplitudes and
uses 60-digit arithmetic. The included GitHub Actions workflow is
configured to run all three Python checks on every push and pull request.

The Mathematica walkthrough at
[`notebooks/cqc_counterexample.nb`](notebooks/cqc_counterexample.nb) has an
exact symbolic core and a high-precision supplement. All 19 input cells were
evaluated without messages in a fresh Wolfram 14.3 kernel.

## Review guide

- [`research/cqc-counterexample.md`](research/cqc-counterexample.md) —
  self-contained construction and proof.
- [`research/cqc-status.md`](research/cqc-status.md) — scope of the published
  conjecture, proven special cases, related bounds, Iqbal's sufficient
  condition, and the ECQC extension.
- [`research/literature-search.md`](research/literature-search.md) — search
  methods, directly relevant papers, and citation-trail record.
- [`PROVENANCE.md`](PROVENANCE.md) — source attribution, repository stewardship,
  and the boundary between automated checks and independent review.
- [`scripts/`](scripts) — exact SymPy, NumPy, and high-precision mpmath
  implementations generated within the same model-assisted workflow.
- [`notebooks/cqc_counterexample.nb`](notebooks/cqc_counterexample.nb) —
  Mathematica certificate for readers who prefer a notebook.

The construction does not contradict any proven CQC special case or the
Coles–Piani bound. It violates the original two-basis CQC conjecture, while
Iqbal's 2026 ECQC extension remains satisfied for this state.

## Reuse and citation

The repository is released under [CC0-1.0](LICENSE), only to the extent that
copyright or related rights exist and are controlled by the steward or later
contributors. This dedication is not a claim that mathematical facts or
machine-generated material are copyrightable, or that the steward authored the
mathematics. See [`PROVENANCE.md`](PROVENANCE.md) for the complete statement.

Machine-readable citation metadata is in [`CITATION.cff`](CITATION.cff). Its
required `authors` field names OpenAI GPT-5.6 Pro as the machine source; Ethan
O'Connor is listed separately as repository steward and contact. Cite this
release using the [version DOI](https://doi.org/10.5281/zenodo.21499723). The
[concept DOI](https://doi.org/10.5281/zenodo.21499722) resolves to the latest
archived version.

## Literature and claim status

The search record was last updated July 22, 2026. The most recent directly
relevant published work found,
[Iqbal, *Quantum Information Processing* 25, 250
(2026)](https://doi.org/10.1007/s11128-026-05258-2), still described the
original CQC conjecture as open. No earlier counterexample was found in the
targeted terminology, bibliographic databases, or citation records returned
by those services.

That search is evidence, not proof of priority. The intended next step is
independent review by specialists and the authors of the relevant CQC papers.
The automated checks in this repository were produced in the same
model-assisted workflow and should not be described as independent replication.
