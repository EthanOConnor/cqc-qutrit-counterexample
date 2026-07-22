# Literature search record

Search performed: July 20–22, 2026

Scope: the complementary-quantum correlation (CQC) relation of Schneeloch,
Broadbent, and Howell, especially any proof, disproof, explicit counterexample,
or construction based on a lower-dimensional support embedded in a qutrit.

## Result

No earlier counterexample was found. The newest directly relevant
version-of-record paper located, published July 10, 2026, explicitly says that
the original CQC conjecture remains open.

This is evidence about the state of the indexed literature, not proof of
novelty or priority. Unindexed manuscripts, very recent work, non-English
literature, private communications, and terminology not captured by the
queries may have been missed.

## Search methods

The search used:

- exact-phrase and keyword web searches for `"complementary-quantum
  correlation"`, `"CQC conjecture"`, `"CQC relation"`, the displayed mutual
  information inequality, `counterexample`, `rank-deficient`, `embedded qubit`,
  and the distinctive rational values and entropy expression in this
  certificate;
- arXiv-targeted searches for the same terms;
- Crossref bibliographic and DOI metadata searches;
- the OpenAlex record and citation records returned for
  `10.1103/PhysRevA.90.062119` (OpenAlex work `W2033363990`);
- the Semantic Scholar record and indexed citation trail for the same DOI;
- direct inspection of the original paper, the 2022 fixed-purity numerical
  study, the 2026 CQC paper, and the most closely related pre-2014 work found.

At search time Crossref reported seven citing works and OpenAlex reported eight.
Semantic Scholar exposed five. The union was inspected; none reported a
counterexample to the original CQC conjecture.

## Directly relevant works

### Wu, Poulsen, and Mølmer (2009)

S. Wu, U. V. Poulsen, and K. Mølmer, “Correlations in local measurements on a
quantum state, and complementarity as an explanation of nonclassicality,”
*Physical Review A* **80**, 032319 (2009),
[doi:10.1103/PhysRevA.80.032319](https://doi.org/10.1103/PhysRevA.80.032319).

This paper derives complementary-measurement information bounds predating the
CQC conjecture. Its Proposition 2 holds Bob's POVM fixed while Alice switches
between mutually unbiased bases. That is not the original CQC setup, in which
both parties switch their local measurements, and it neither states nor supplies
the present counterexample.

### Schneeloch, Broadbent, and Howell (2014)

J. Schneeloch, C. J. Broadbent, and J. C. Howell, “Uncertainty relation for
mutual information,” *Physical Review A* **90**, 062119 (2014),
[doi:10.1103/PhysRevA.90.062119](https://doi.org/10.1103/PhysRevA.90.062119),
[arXiv:1404.6496](https://arxiv.org/abs/1404.6496).

This is the original conjecture. It quantifies over arbitrary bipartite states
and arbitrary first local observables, requiring only that the second observable
on each subsystem be mutually unbiased with its local first observable. It proves
special cases and reports Monte Carlo searches, including $3\otimes3$, with no
counterexample.

### Alsing et al. (2022)

P. M. Alsing, C. C. Tison, J. Schneeloch, R. J. Birrittella, and M. L. Fanto,
“The distribution of density matrices at fixed purity for arbitrary dimensions,”
*Physical Review Research* **4**, 043114 (2022),
[doi:10.1103/PhysRevResearch.4.043114](https://doi.org/10.1103/PhysRevResearch.4.043114),
[arXiv:2205.01723](https://arxiv.org/abs/2205.01723).

The CQC application in this paper reexamines $N=4$, meaning a two-qubit
composite system, with fixed-purity sampling. It reports no violation. It does
not perform the qutrit-pair construction used here.

### Iqbal (2026)

H. Iqbal, “On the CQC conjecture: a sufficient condition and an extension,”
*Quantum Information Processing* **25**, 250 (2026),
[doi:10.1007/s11128-026-05258-2](https://doi.org/10.1007/s11128-026-05258-2),
[arXiv:2509.08286](https://arxiv.org/abs/2509.08286).

The article was published July 10, 2026 and explicitly describes the original
CQC conjecture as open. It proves a sufficient condition and proposes an
extended CQC (ECQC) conjecture. Its random-state simulations in dimensions 3
and 5 concern the ECQC extension; they should not be described as a new broad
simulation of the original two-basis CQC conjecture.

## Indexed citation trail checked

OpenAlex listed the following substantive works citing the 2014 paper (plus one
duplicate repository record):

- “Tightening the entropic uncertainty bound in the presence of quantum
  memory” (2016), doi:10.1103/PhysRevA.93.062123.
- “High-dimensional entanglement certification” (2016),
  doi:10.1038/srep27637.
- “Entropic uncertainty relations and their applications” (2017),
  doi:10.1103/RevModPhys.89.015002.
- “Wehrl entropy, entropic uncertainty relations, and entanglement” (2021),
  doi:10.1103/PhysRevA.103.062222.
- “The distribution of density matrices at fixed purity for arbitrary
  dimensions” (2022), doi:10.1103/PhysRevResearch.4.043114.
- “Area laws and thermalization from classical entropies in a Bose-Einstein
  condensate” (2025/2026 indexed record), doi:10.1103/7jzy-g3vd.
- “On the CQC conjecture: a sufficient condition and an extension” (2026),
  doi:10.1007/s11128-026-05258-2.

The similarly titled “Complementary quantum correlations among multipartite
systems” concerns monogamy and polygamy of quantum-correlation measures, not
the Schneeloch–Broadbent–Howell CQC inequality, and was excluded as a
terminology collision.

## Current claim

> The attached certificate exactly violates the published CQC inequality. A
> targeted search of exact terminology, arXiv, Crossref, OpenAlex, Semantic
> Scholar, and the citation records returned for the original paper through
> July 22, 2026 found no earlier counterexample. This does not establish
> novelty or priority; independent expert and author review is pending.


## Provenance note

This search record was assembled by OpenAI GPT-5.6 Pro in the same prompted
workflow that generated the candidate counterexample and its automated checks.
It is a documented search, not an independent novelty opinion. See
[`../PROVENANCE.md`](../PROVENANCE.md).
