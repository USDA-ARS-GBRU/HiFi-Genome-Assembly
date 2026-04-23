# Contributing

Contributions are welcome. This protocol is intended to be practical, beginner-friendly, and strong enough for manuscript review and public genome release.

## What Good Contributions Include

- Clear rationale for the workflow, tool, parameter, or documentation change.
- Links to primary tool documentation, papers, or official repositories when adding external tools.
- Example commands that can be adapted to HPC environments.
- Notes on when not to use a tool or parameter.
- Validation commands or toy examples when adding helper scripts.
- Updates to README inventories and docs indexes when adding public files.

## File Expectations

Documentation:

- Use concise Markdown.
- Prefer focused pages under `docs/` for new web-doc content.
- Keep the root README as the longform master narrative until the v1.0 docs split.
- Define less-common abbreviations on first use.

Helper scripts:

- Use Python standard library when practical.
- Include `argparse` help.
- Write tab-delimited outputs for audit tables.
- Add a toy validation command to GitHub Actions when feasible.

sbatch templates:

- Keep templates cluster-adaptable.
- Use environment variables for sample-specific inputs.
- Print or capture tool versions where possible.
- Avoid hard-coded accounts, partitions, or private paths.

Examples:

- Keep examples tiny and public-safe.
- Do not commit raw reads, real unreleased genomes, private metadata, or large analysis outputs.
- Use `temp/` or other ignored local folders for development-only references.

## Validation Before Pull Requests

Run:

```bash
python3 -m py_compile scripts/*.py
bash -n 01_sbatch_templates/*.sbatch
scripts/check_repo_inventory.py --readme README.md -o /tmp/repo_inventory.tsv
scripts/check_markdown_links.py README.md docs -o /tmp/markdown_links.tsv
scripts/check_docs_coverage.py -o /tmp/docs_coverage.tsv
```

For helper changes, also run the relevant toy examples from the README or GitHub Actions workflow.

## Citation and Licensing

Keep `CITATION.cff` and `LICENSE` present. When adding a tool, cite the tool's paper or official documentation in the relevant docs page or README reference section.

## Review Standard

A contribution should make the protocol more reproducible, teachable, or review-ready. Avoid adding tools as a list only; explain where they fit, when they fail, and what evidence is needed before trusting their output.
