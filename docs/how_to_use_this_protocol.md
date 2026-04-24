# How To Use This Protocol In A Real Project

This page is the practical onboarding path for a new lab member who wants to use the protocol without getting lost in the full docs tree.

## Recommended Working Style

Treat this repository as:

1. a decision guide
2. a source of example sbatch templates
3. a source of helper scripts and toy validation fixtures
4. a release-readiness checklist

Do not treat it as a single copy-paste command stream.

## Best Companion Pages

Keep these open while you work:

- [Project starter kit](project_starter_kit.md)
- [sbatch template index](sbatch_template_index.md)
- [workflow templates and checklists](workflow_templates/index.md)
- [Status and roadmap](status.md)

## First Day Checklist

Before running large jobs, make sure you can answer:

- what is the biological sample and how inbred or heterozygous is it?
- what files belong to that sample?
- what is the expected genome size and ploidy?
- will the first deliverable be contigs, haplotypes, or chromosome-scale scaffolds?
- what evidence is available beyond HiFi reads: Hi-C, parents, RNA-seq, Iso-Seq, proteins, reference assemblies?

Record those decisions in your project metadata from the beginning.

## Suggested Reading Order For New Users

1. [Setup](setup/index.md)
2. [Assembly](assembly/index.md)
3. [QC](qc/index.md)
4. [Curation](curation/index.md), if structural problems appear
5. [Scaffolding and Finishing](scaffolding/index.md), when moving to chromosome scale
6. [Annotation](annotation/index.md)
7. [Release](release/index.md)

## Minimal Working Project Path

For many crop projects, a practical first-pass path is:

```text
set up environment
  -> profile reads and genome properties
  -> assemble with hifiasm
  -> review metrics and dotplots
  -> clean contamination and organelles intentionally
  -> manually curate only strong structural problems
  -> scaffold only after the contigs are believable
  -> freeze repeat and gene annotation decisions
  -> build and audit the release bundle
```

## When To Slow Down

Pause and review more carefully when:

- the k-mer profile and final assembly size disagree sharply
- BUSCO duplication looks too high for the biology
- dotplots suggest a structural problem near repetitive sequence
- contamination decisions affect large contigs or putative chromosomes
- scaffolding methods disagree with each other
- annotation files no longer match final FASTA sequence IDs
- table2asn discrepancies point to coordinate or naming mismatches

## What To Reuse From This Repo

- [sbatch template index](sbatch_template_index.md)
- [workflow templates and checklists](workflow_templates/index.md)
- [project starter kit](project_starter_kit.md)
- `scripts/` helper programs
- `examples/` toy validation fixtures

## What Not To Reuse Blindly

- cluster-specific walltimes, partitions, and module names
- tool defaults without checking the biological context
- reference-guided scaffolds that disagree with independent evidence
- annotation sets produced before the final assembly naming scheme is frozen

## Good Habits

- keep a project-local decision log
- keep intermediate summaries, not only final FASTA files
- write down why a correction was accepted or rejected
- keep FASTA names, AGP rows, and GFF3 IDs synchronized
- prepare release metadata earlier than feels necessary

## Related Pages

- [Status and roadmap](status.md)
- [Documentation site home](index.md)
- [Release package decision guide](release_package_decision_guide.md)
