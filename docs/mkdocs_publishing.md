# MkDocs and GitHub Pages Publishing

This project now uses MkDocs as the documentation-site framework and GitHub Actions as the publishing path to GitHub Pages.

Expected site URL after Pages is enabled for the repository:

```text
https://usda-ars-gbru.github.io/HiFi-Genome-Assembly/
```

## What Is In The Repo

- `mkdocs.yml`: navigation and site configuration
- `.github/workflows/deploy-docs.yml`: build and deploy workflow
- `docs/`: documentation source tree

## Recommended GitHub Pages Settings

In the repository settings:

1. Open `Settings -> Pages`
2. Set the source to `GitHub Actions`
3. Save the setting

After that, pushes to `main` should build and publish the MkDocs site.

## Current Publishing Strategy

- keep the root `README.md` as the GitHub landing page
- publish the focused docs tree to GitHub Pages
- link the public docs site from the README

This gives first-time visitors a short repo overview while keeping the detailed protocol in a real docs site.

## Migration Rule

Do not wait for the documentation site to be perfect before publishing it. It is acceptable for the Pages site to reflect an active-draft state as long as the README and docs status make that clear.

## Related Files

- `mkdocs.yml`
- `docs/site_platform_decision.md`
- `docs/readme_to_docs_migration_plan.md`
