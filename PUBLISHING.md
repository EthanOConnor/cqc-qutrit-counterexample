# Publication and archival procedure

The public repository is:

`https://github.com/EthanOConnor/cqc-qutrit-counterexample`

The initial clean history and Zenodo deposit have already been published. The
version DOI is `10.5281/zenodo.21499723`; the concept DOI is
`10.5281/zenodo.21499722`.

## Future releases

For a subsequent archival version:

1. Confirm that GitHub Actions passes every verifier in `.github/workflows/verify.yml`.
2. Update `CITATION.cff`, `README.md`, and `RELEASE.md` with the new version and date.
3. Create an annotated Git tag and GitHub release only after the Zenodo GitHub
   integration is enabled for the repository.
4. Allow Zenodo to ingest the GitHub release. Inspect creator, title, version,
   description, provenance, and CC0-1.0 metadata before treating the record as
   final.
5. Add the new version DOI to the repository without rewriting prior tags.

Zenodo uses `CITATION.cff` because the repository deliberately does not contain
`.zenodo.json`. The CFF entity author records OpenAI GPT-5.6 Pro as the machine
source. Ethan O'Connor is represented separately as contact and repository
steward, not as mathematical author.

Do not create a separate manual Zenodo deposit for the same GitHub release;
that risks duplicate DOI records for one version.

## Suggested release-note form

> Public release of an exact, machine-originated counterexample to the
> complementary-quantum correlation conjecture, with exact finite sign
> certificates and reproducible verification code. This version also includes
> the higher-dimensional computational/Fourier family and replacement upper
> bounds. Provenance is disclosed in `PROVENANCE.md`.
