# Community Database Release Companion

Use this guide after the NCBI/INSDC release package is defined and before sending files to crop community databases.

The aim is not to create a second, drifting release. The aim is to keep the community-database package synchronized with the same frozen assembly object used for the primary public submission.

## Why This Matters

For crop genomes, many users will encounter the assembly first through a species community resource rather than directly through GenBank.

That means the community package should preserve:

- the same assembly identity
- the same versioned naming
- the same accession links
- the same gene-model release identity
- the same release notes about what is and is not public yet

## Current Examples From Community Resources

Current official community resources checked during drafting:

- MaizeGDB's genome center says it hosts maize assemblies that meet minimum requirements and uses structured genome and annotation naming conventions: [MaizeGDB Genome Center](https://www.maizegdb.org/genome)
- SoyBase documents soybean genome and annotation naming conventions and links GenBank/RefSeq-style accessions to community identifiers: [SoyBase Genome and Annotation Information](https://www.soybase.org/resources/genome_info/) and [SoyBase Genome Nomenclature](https://www.soybase.org/about/genome_nomenclature/)
- Gramene continues to provide crop comparative-genomics and pan-genome resources across many species: [Gramene 2025 update](https://pubmed.ncbi.nlm.nih.gov/41335101/)

Inference from those sources: community databases often add their own identifiers, browsers, and naming layers, so the safest practice is to ship a clear crosswalk from your public submission identifiers to community-facing names.

## Minimum Companion Package

At minimum, provide:

- frozen assembly FASTA
- AGP when relevant
- chosen gene annotation files, if public
- repeat tracks, if useful to the community resource
- accession crosswalk
- assembly and annotation version note
- methods or provenance summary

## Identifier Crosswalk Rule

Do not assume the community resource will preserve every identifier exactly as submitted.

Instead, ship a crosswalk table that connects:

- local project name
- NCBI assembly accession
- community database assembly name
- local annotation name
- community annotation name
- release date

This is especially important when the community database has its own nomenclature conventions, as seen in MaizeGDB and SoyBase.

## Synchronization Checklist

- [ ] Assembly version matches the public submission object
- [ ] FASTA sequence names match the frozen release FASTA
- [ ] AGP matches the same scaffold/chromosome structure
- [ ] annotation version is clearly stated as public or not yet public
- [ ] accession crosswalk is included
- [ ] README or release note explains any community-specific renaming
- [ ] browser tracks and downloadable files point to the same release object

## Common Failure Modes

### Community rename without crosswalk

Result:

- users cannot connect publications, NCBI accessions, and browser objects

### Community release gets newer annotation than NCBI without clear versioning

Result:

- users compare mismatched gene sets and think the public record is inconsistent

### FASTA or annotation refreshed for community upload after NCBI freeze

Result:

- there are effectively two public assemblies with one claimed version

## Good Release Pattern

A strong pattern looks like this:

1. Freeze the NCBI/INSDC release object.
2. Record the accession tracker.
3. Build a small crosswalk table for the community resource.
4. Ship the same FASTA and same versioned annotation unless a later community-only release is explicitly version-bumped.

## Reviewer-Ready Language

Methods:

> The community database companion package was generated from the same frozen release object submitted to the public nucleotide archive. Community-facing identifiers and browser labels were linked back to the public assembly and annotation accessions through an explicit crosswalk table.

Reviewer response:

> We avoided creating a second unsynchronized public release by deriving the community database package directly from the same frozen assembly object used for the archive submission. Any community-specific identifiers are cross-referenced to the public accessions.

## Related Files

- `docs/release_candidate_worked_case.md`
- `docs/accession_handoff_worked_example.md`
- `docs/release_package_decision_guide.md`
- `examples/accession_tracking.tsv`
