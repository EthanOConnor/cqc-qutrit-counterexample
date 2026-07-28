# Release record

## Version 1.0.0 — 2026-07-22

This is the first circulation-ready version of the CQC counterexample
certificate.

The public repository intentionally began with a single root commit containing
that complete state. Earlier exploratory and editorial history is preserved
separately in the private development repository. The collapsed public history
is a publication choice, not a claim that the root commit marks the first
generation of the mathematical content. Source, stewardship, automated
verification status, and review limits are described in `PROVENANCE.md`.

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
replication. The release is an immutable record of the exact certificate, not
a substitute for formal peer review.

## Subsequent development on `main`

The repository now also contains an explicit computational/Fourier family in
every equal local dimension `d >= 3`, an exact no-go for that family at `d = 2`,
a working analysis of the unrestricted qubit question, and replacement upper
bounds. These additions postdate the archived v1.0.0 tree.
