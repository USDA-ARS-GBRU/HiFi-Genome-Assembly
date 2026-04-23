# Documentation Platform Decision

## Decision

This project will use **MkDocs** as the primary documentation-site framework for the future public documentation site.

The longform root `README.md` remains the landing page during migration, but the focused protocol content will move into `docs/` and be organized for MkDocs navigation and GitHub Pages publication.

## Why MkDocs

MkDocs is the better fit for this repository because:

- the protocol is already large and still growing
- multiple lab members are expected to contribute over time
- the project benefits from explicit navigation and section structure
- a documentation build with a clear nav file is easier to maintain than a loose Markdown-only site
- the repo already has enough focused pages that a real documentation framework now adds value

## Why Not Docsify Right Now

Docsify remains a reasonable lightweight option, but for this project it would trade away structure exactly when the documentation set is becoming large enough to need stronger organization.

Compared with Docsify, MkDocs should make it easier to:

- maintain a stable left-hand navigation tree
- keep related pages grouped by topic
- onboard new contributors to the documentation layout
- evolve the site into a lab-maintained public protocol

## Migration Rules

- Preserve the current longform README before every major condensation pass.
- Keep the root `README.md` as a concise landing page for GitHub visitors.
- Use `docs/` as the single source for detailed procedural content.
- Prefer section index pages in MkDocs nav, then link outward to deeper pages.
- Keep the first migration pass conservative: setup/environment content first, then assembly detail.

## Preserved Source

The full pre-condensation README snapshot for this migration phase is archived at:

```text
docs/archive/README.longform.v0.5.0-dev.md
```

## Immediate Next Steps

1. Add `mkdocs.yml`.
2. Build a first-pass site navigation around the existing section index pages.
3. Move setup/environment detail out of the README.
4. Continue shortening the README in small reversible passes.

GitHub Pages publishing is part of this plan so the focused docs can become the public documentation destination while the README remains the repository landing page.
