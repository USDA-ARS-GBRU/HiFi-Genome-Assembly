# Gene Annotation

Gene annotation should be evidence-driven. For crop plants, the best strategy depends on available RNA-seq, Iso-Seq, related annotations, protein evidence, repeat masking, and the purpose of the release.

## Strategy Comparison

| Tool | Best use | Caution |
| --- | --- | --- |
| Liftoff | close cultivar/species annotation transfer | can miss novel genes or struggle across structural divergence |
| BRAKER3 | RNA-seq/protein-supported ab initio prediction | environment and evidence preparation matter |
| MAKER | configurable evidence integration and iterative annotation | more setup and curation required |

Many crop projects benefit from a hybrid strategy: Liftoff to preserve known models, BRAKER3 to add evidence-supported predictions, and MAKER or custom curation to integrate evidence into a final gene set.

## Inputs to Freeze

Before annotation, freeze:

- final or near-final soft-masked FASTA
- sequence ID map
- repeat GFF3 and repeat library provenance
- RNA-seq alignments, assembled transcripts, or Iso-Seq evidence
- related species protein FASTA
- reference GFF3 for liftover when appropriate
- decision logs for excluded contaminant, organelle, alternate, or haplotig sequences

Use `docs/repeat_to_gene_annotation_handoff.md` before handing the masked genome into gene annotation.
For release-gene-set selection, see `docs/gene_set_decision_guide.md`.
For downstream function labels and QC summaries, see `docs/functional_annotation_guide.md` and `docs/annotation_qc_dashboard_guide.md`.

## Liftoff

```bash
sbatch \
  --export target_genome=13_repeats/sample.softmasked.fa,reference_genome=references/ref.fa,reference_gff=references/ref.gff3,sample=sample \
  01_sbatch/liftoff.sbatch
```

Use Liftoff when the reference annotation is close enough that most gene structures should be conserved.

## BRAKER3

```bash
sbatch \
  --export genome=13_repeats/sample.softmasked.fa,species=Genus_species_sample,rnaseq_bam=14_genes/rnaseq/sample.bam,proteins=14_genes/evidence/related_proteins.fa \
  01_sbatch/braker3.sbatch
```

Use BRAKER3 when RNA-seq and/or protein evidence are available and a full de novo annotation is needed.

## MAKER

```bash
sbatch \
  --export control_dir=14_genes/maker/control_files,outdir=14_genes/maker/run \
  01_sbatch/maker.sbatch
```

Use MAKER when a configurable evidence-integration workflow is needed.

## Minimum QC

Track:

- gene count
- transcript count
- protein FASTA
- transcript FASTA
- BUSCO protein-mode score
- internal stop codon screen
- functional annotation rate
- TE-derived gene review
- table2asn validation results

Inspect gene density by chromosome or scaffold. Sudden gene deserts, extreme clusters, or many genes on contamination-flagged contigs usually indicate a sequence, masking, evidence, or contamination issue.

## Release Rule

Do not publish gene annotation without documenting evidence sources, repeat masking, tool versions, validation results, and any filtering used to remove transposable-element-derived or low-confidence models.
