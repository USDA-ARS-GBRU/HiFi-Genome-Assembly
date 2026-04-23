# Citation and License Review

Use this page before tagging a public release. The goal is to make the repository easy to cite, clear to reuse, and honest about what the protocol does and does not guarantee.

## Files to Review

| File | Purpose | Review question |
| --- | --- | --- |
| `CITATION.cff` | citation metadata for GitHub and citation managers | Is the title, version, release date, repository URL, and author/contributor wording correct? |
| `LICENSE` | reuse terms for code and documentation | Is MIT still the intended license for helper scripts, templates, and docs? |
| `README.md` | public landing protocol | Does it point readers to citation, license, contribution, and status information? |
| `CONTRIBUTING.md` | contributor expectations | Does it explain citation updates for newly added tools? |
| `.github/` templates | public collaboration path | Do issues and pull requests ask for enough reproducibility context? |

## Current Repository Position

The repository currently uses:

- citation format: `CITATION.cff`
- license: MIT
- version source of truth: `VERSION`
- changelog: `CHANGELOG.md`
- public repository: `https://github.com/USDA-ARS-GBRU/HiFi-Genome-Assembly`

Before a stable tag, confirm whether the `CITATION.cff` author field should remain organization-level or list named contributors.

## Tool Citations

This protocol depends on many external tools. Cite the repository when using the protocol, and cite the underlying tools used in the actual analysis. When adding a new tool to the protocol:

- link the official repository or documentation
- cite the primary paper when available
- include the tool version in methods text or logs
- explain what evidence is needed before trusting the output
- avoid implying endorsement beyond the documented workflow role

## Stable Release Checklist

- [ ] `VERSION` matches `CITATION.cff`.
- [ ] `CHANGELOG.md` has a section for the release.
- [ ] `CITATION.cff` release date matches the intended tag date.
- [ ] Citation author/contributor wording is approved.
- [ ] License choice is approved for code, sbatch templates, and documentation.
- [ ] README includes citation, license, contribution, and status links.
- [ ] GitHub issue and pull request templates are present.
- [ ] Public examples contain no private sample names, unpublished genome data, or raw reads.
- [ ] Release notes explain the development status and any known limitations.

## Local Audit

Run:

```bash
scripts/check_public_release_metadata.py -o /tmp/public_release_metadata.tsv
```

This audit checks the presence of public metadata files and verifies that `VERSION`, `CITATION.cff`, `LICENSE`, and README references agree.

## Release Note Language

```text
This release provides a modular PacBio HiFi genome assembly protocol for crop plant genomes. It includes HPC-oriented workflow templates, QC and curation guidance, scaffolding and finishing review logic, annotation entry points, and public-release checks. Users should cite this repository and the specific third-party tools used in their analysis.
```
