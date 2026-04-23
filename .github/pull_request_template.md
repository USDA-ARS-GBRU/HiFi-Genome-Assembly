## Summary

Describe the change and why it is useful for crop plant PacBio HiFi genome assembly.

## Type of Change

- [ ] Documentation
- [ ] Helper script
- [ ] sbatch template
- [ ] Example or fixture
- [ ] CI/validation
- [ ] Release metadata

## Validation

Run the relevant checks before requesting review:

- [ ] `python3 -m py_compile scripts/*.py`
- [ ] `bash -n 01_sbatch_templates/*.sbatch`
- [ ] `scripts/check_repo_inventory.py --readme README.md -o /tmp/repo_inventory.tsv`
- [ ] `scripts/check_markdown_links.py README.md docs -o /tmp/markdown_links.tsv`
- [ ] `scripts/check_docs_coverage.py -o /tmp/docs_coverage.tsv`
- [ ] `scripts/check_project_metadata.py -o /tmp/project_metadata.tsv`
- [ ] Relevant toy/example helper command, if applicable

## Documentation

- [ ] README inventory updated when public files were added
- [ ] Docs index updated when focused docs pages were added
- [ ] Changelog updated
- [ ] Less-common abbreviations are defined on first use

## Data Safety

- [ ] No private sample metadata
- [ ] No unreleased genome data
- [ ] No raw reads or large analysis outputs
- [ ] Local-only files remain ignored

## Citations

List new tools, papers, official docs, or repositories cited by this change.
