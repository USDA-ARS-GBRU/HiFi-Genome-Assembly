# Hi-C Scaffolding Reader Path

Hi-C scaffolding orders and orients contigs into chromosome-scale scaffolds using chromatin contact evidence. In crop genome projects, Hi-C scaffolding should improve organization without hiding contamination, haplotigs, weak contigs, or real structural variation.

## Before Scaffolding

Do not scaffold until:

- the contig assembly has passed basic QC
- contamination and organelle review are complete enough for scaffolding input
- obvious misassembly candidates have been reviewed
- the Hi-C library source and genotype are documented
- the expected chromosome number is known or explicitly uncertain
- a decision log exists for scaffold choices

## Tool Choices

| Tool | Best use | Caution |
| --- | --- | --- |
| YaHS | fast Hi-C scaffolding and common current default | still requires contact-map review |
| 3D-DNA/JBAT | interactive manual contact-map curation | manual dragging is not evidence by itself |
| SALSA2 | older Hi-C scaffolding workflows | compare against newer tools when possible |
| ALLHiC | some polyploid and allele-aware contexts | requires careful biological setup |
| RagTag | reference-guided scaffolding when Hi-C is absent or as comparison | reference bias can hide true variation |

## YaHS Path

Start with:

- [YaHS Hi-C workflow](../yahs_hic_workflow.md)
- `01_sbatch_templates/yahs_hic_scaffold.sbatch`

Review expected outputs:

```text
sample.yahs_scaffolds_final.fa
sample.yahs_scaffolds_final.agp
sample.yahs_scaffolds_final.bin
sample.yahs_scaffolds_final.chrom.sizes
```

Convert to `.hic` for Juicebox/JBAT review when needed.

## 3D-DNA/JBAT Path

Start with:

- [3D-DNA/Juicebox workflow](../3d_dna_juicebox_workflow.md)
- `01_sbatch_templates/3d_dna_scaffold.sbatch`

Use 3D-DNA/JBAT when interactive contact-map review is central, when YaHS and 3D-DNA disagree, or when collaborators require JBAT review files.

## Contact Map QC

Review:

- square chromosome blocks along the diagonal
- no strong unexplained off-diagonal blocks
- no abrupt contact drops at joins
- orientation and order consistency
- weak or repeat-rich contigs that should remain unplaced

Use [Hi-C contact map QC](../hic_contact_map_qc.md) as the checklist.

## Candidate Comparison

Compare candidates before choosing a release scaffold:

```bash
scripts/compare_scaffolding_candidates.py \
  --candidate contig=07_assemblies/sample.primary.fa \
  --candidate yahs=10_scaffolding/sample/yahs/sample.yahs_scaffolds_final.fa \
  --candidate 3d_dna=10_scaffolding/sample/3d_dna/sample.FINAL.fasta \
  -o 10_scaffolding/sample.scaffolding_candidate_metrics.tsv
```

Do not choose solely by N50. Prefer the candidate with the strongest contact-map support, AGP validity, dotplot consistency, contamination review, and documented decisions.

## Required Release Artifacts

```text
10_scaffolding/sample.final.fa
10_scaffolding/sample.final.agp
10_scaffolding/sample.scaffolding_decisions.tsv
10_scaffolding/sample.scaffolding_candidate_metrics.tsv
10_scaffolding/qc/contact_map_screenshots/
15_release/sample.agp_validation.tsv
15_release/sample.fasta_validation.tsv
```

## Release Rule

The final scaffold FASTA, AGP, contact map, dotplots, contamination decisions, and scaffold decision log must describe the same assembly structure.
