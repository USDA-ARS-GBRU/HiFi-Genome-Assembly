# Organelle Detection and Release Decision Workflow

Crop plant HiFi assemblies often contain chloroplast and mitochondrial sequence. This is not automatically a problem; the issue is whether organellar sequence is being represented intentionally and consistently in the nuclear genome assembly, organelle assembly, and public submission package.

## Goals

- Identify likely chloroplast-derived contigs.
- Identify likely mitochondrial-derived contigs.
- Distinguish true nuclear organellar insertions from free organelle contigs when possible.
- Decide whether each sequence should be retained, removed, masked, placed in a separate organelle submission, or flagged for review.

## Inputs

```text
07_assemblies/sample.primary.fa
references/chloroplast.fa
references/mitochondrion.fa
08_stats/read_mapping/sample.hifi_to_assembly.bam
09_dotplots/
11_contamination/fcs_adaptor/
11_contamination/fcs_gx/
```

## Screening Strategy

1. Build a combined organelle reference FASTA from trusted chloroplast and mitochondrial assemblies from the same species or a close relative.
2. Align the nuclear assembly candidate to organelle references with minimap2 `-x asm5` or BLASTN.
3. Summarize contig-level alignment coverage, identity, and read depth.
4. Cross-check suspect contigs with FCS-GX, BlobToolKit, GC content, and coverage.
5. Review whether the contig is a complete organelle, a nuclear organellar insertion, or a mixed/chimeric sequence.

Example:

```bash
sbatch \
  --export assembly=07_assemblies/sample.primary.fa,organelle_refs=references/organelle_refs.fa,sample=sample \
  01_sbatch/organelle_screen.sbatch
```

## Decision Categories

| Category | Evidence | Default action |
| --- | --- | --- |
| Complete chloroplast genome | high identity across most of a chloroplast reference, high organelle-like coverage | remove from nuclear assembly; submit separately if desired |
| Complete mitochondrial genome | high identity across most of a mitochondrial reference, high organelle-like coverage | remove from nuclear assembly; submit separately if desired |
| Small organelle-derived contig | mostly organelle alignment, no nuclear context | remove from nuclear assembly unless release plan includes organelles |
| Nuclear organellar insertion | organelle-like segment embedded in otherwise nuclear sequence with normal nuclear coverage | retain and document |
| Chimeric contig | nuclear and organellar segments joined suspiciously, unsupported by reads/Hi-C | split/remove only with evidence and document |
| Ambiguous hit | short or low-identity alignment | retain for now; mark for review |

## Evidence to Record

For every sequence removed or retained after organelle review, record:

```text
sample
sequence_id
length
organelle_type
alignment_coverage
alignment_identity
read_depth
FCS_GX_result
decision
rationale
reviewer
date
```

## Release Guidance

- Do not submit free chloroplast or mitochondrial contigs as part of the nuclear genome unless that is an intentional and accepted submission design.
- Do not remove true nuclear organellar insertions simply because they align to an organelle reference.
- If organelles are assembled, submit them as organelle genome records with appropriate topology and annotation.
- Document all sequence removals in the assembly decision log.

