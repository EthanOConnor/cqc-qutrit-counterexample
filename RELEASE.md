# Release record

## Version 1.0.0 — 2026-07-22

This is the first circulation-ready version of the candidate CQC
counterexample certificate.

The public repository is intentionally intended to begin with a single root
commit containing this complete state. Earlier exploratory and editorial
history is preserved separately in the private development repository
`EthanOConnor/cqc-counterexample`; the release tree was assembled from that
record through commit
`20ed99a9695dafb609936f4a937b624c14b15b01`, with the repository URL in
`CITATION.cff` changed to the intended public location.

That collapsed public history is a publication choice, not a claim that the
root commit marks the first generation of the mathematical content. The source,
human stewardship, automated verification status, and limits of the present
review are described in `PROVENANCE.md`.

### Included certificate

- explicit rank-two qutrit-pair state;
- qutrit computational and Fourier mutually unbiased bases;
- exact common rational joint-probability table;
- exact violation
  `h_2(1/10) - 2 h_2(1/30) = 0.0473109929522169...` bits;
- integer sign certificate `29^58 > 3^114 10^30`;
- exact full-rank white-noise robustness certificate;
- SymPy, NumPy, mpmath, and Mathematica implementations;
- literature and scope notes current through 2026-07-22;
- CC0-1.0 dedication and machine-readable citation metadata.

### Review status

The included implementations were generated in the same model-assisted
workflow. Their agreement is internal corroboration rather than independent
expert replication. Correctness, intended scope, novelty, and priority remain
open to independent human review.
