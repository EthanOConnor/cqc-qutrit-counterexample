# Publication and archival procedure

The intended public repository is:

`https://github.com/EthanOConnor/cqc-qutrit-counterexample`

The repository should be created as **public and empty**: do not initialize it
with a README, license, or `.gitignore`, because all of those are already in the
root commit supplied with the release bundle.

## Publish the clean Git history

From the supplied Git bundle:

```sh
git clone -b main cqc-qutrit-counterexample-v1.0.0.bundle cqc-qutrit-counterexample
cd cqc-qutrit-counterexample
git remote remove origin
git remote add origin git@github.com:EthanOConnor/cqc-qutrit-counterexample.git
git push -u origin main
git push origin v1.0.0
```

An HTTPS remote may be used instead:

```sh
git remote add origin https://github.com/EthanOConnor/cqc-qutrit-counterexample.git
```

After the push, confirm that GitHub Actions completes the three Python
certificate jobs successfully.

## Create the Zenodo DOI

Use one archival route for the release; do not create both a manual Zenodo
record and a GitHub-integrated record for the same version.

Recommended GitHub-integration route:

1. Link the GitHub account to Zenodo.
2. In Zenodo, open the GitHub integration, select **Sync now**, find
   `EthanOConnor/cqc-qutrit-counterexample`, and enable it.
3. Only after the repository is enabled, create a GitHub release from tag
   `v1.0.0` with title `Initial public candidate certificate`.
4. Attach the supplied source `.tar.gz` and `.zip` plus the external checksum
   file as release assets if desired. GitHub's automatic source archive is also
   sufficient for Zenodo ingestion.
5. Wait for Zenodo to ingest the release, then inspect the title, creator,
   provenance description, version, and CC0-1.0 license before treating the
   record as final.
6. Record the version DOI and concept DOI in the repository README and in the
   next revision of `CITATION.cff`. Do not rewrite the tagged `v1.0.0` tree.

Zenodo will use `CITATION.cff` because this repository deliberately does not
contain `.zenodo.json`. The CFF entity author records OpenAI GPT-5.6 Pro as the
machine source. Ethan O'Connor is represented separately as contact and
repository steward, not as mathematical author.

A DOI reserved through a manually created Zenodo draft is an alternative only
when using manual upload. It should not be combined with the automated GitHub
release route, because that risks creating two DOI records for the same object.

## Suggested GitHub release notes

> First public release of an exact, machine-originated candidate
> counterexample to the complementary-quantum correlation conjecture. The main
> sign reduces to `29^58 > 3^114 10^30`; a full-rank perturbation also has an
> exact positive certificate. Provenance is disclosed in `PROVENANCE.md`.
> Independent specialist review of correctness, scope, novelty, and priority is
> pending.
