# Gene Annotation Strategy

Gene annotation should be evidence-driven. For crop plants, the best strategy depends on available RNA evidence, related annotations, protein evidence, and the purpose of the release.

## Strategy Comparison

| Tool | Best use | Strengths | Cautions |
| --- | --- | --- | --- |
| Liftoff | Same species or close cultivar with high-quality annotation | Fast, preserves gene IDs where appropriate | Can miss novel genes and struggle across structural divergence |
| BRAKER3 | RNA-seq and/or protein-supported ab initio annotation | Strong automated evidence integration | Requires careful environment setup and evidence preparation |
| MAKER | Full evidence integration and iterative annotation | Flexible, established for eukaryotic genomes | More configuration-heavy; benefits from training/curation |

The best crop genome annotation is often a hybrid strategy. Liftoff can preserve known gene models for a closely related reference, BRAKER3 can add evidence-supported predictions, and MAKER can integrate transcript, protein, repeat, and ab initio evidence into a curated release set.

## Inputs to Freeze Before Annotation

Prepare:

- final or near-final soft-masked genome FASTA
- exact sequence ID map used for release
- repeat GFF3 and repeat library provenance
- RNA-seq alignments, assembled transcripts, or Iso-Seq evidence when available
- related species protein FASTA
- related cultivar/species GFF3 for liftover when appropriate
- decision log for excluded contaminant, organellar, alternate, and haplotig sequences

Use `docs/repeat_to_gene_annotation_handoff.md` before starting annotation so the repeat mask, repeat GFF, and final release sequence IDs stay synchronized.
For release-gene-set comparison and selection, see `docs/gene_set_decision_guide.md`.
For functional labels and compact release summaries, see `docs/functional_annotation_guide.md` and `docs/annotation_qc_dashboard_guide.md`.

## Liftoff Template

```bash
sbatch \
  --export target_genome=13_repeats/sample.softmasked.fa,reference_genome=references/ref.fa,reference_gff=references/ref.gff3,sample=sample \
  01_sbatch/liftoff.sbatch
```

Use Liftoff when the reference annotation is close enough that gene structure is expected to be mostly conserved.

## BRAKER3 Template

```bash
sbatch \
  --export genome=13_repeats/sample.softmasked.fa,species=Genus_species_sample,rnaseq_bam=14_genes/rnaseq/sample.bam,proteins=14_genes/evidence/related_proteins.fa \
  01_sbatch/braker3.sbatch
```

Use BRAKER3 when RNA-seq and/or protein evidence are available and a full de novo annotation is needed.

## MAKER Template

```bash
sbatch \
  --export control_dir=14_genes/maker/control_files,outdir=14_genes/maker/run \
  01_sbatch/maker.sbatch
```

Use MAKER when you need a highly configurable evidence integration workflow or iterative annotation improvement.

## Minimum Annotation QC

- gene count
- transcript count
- protein FASTA
- transcript FASTA
- BUSCO protein-mode score
- internal stop codon screen
- functional annotation rate
- TE-derived gene review
- table2asn validation if submitting to NCBI

Also inspect gene density by chromosome or scaffold. Sudden gene deserts, extreme gene clusters, or many genes on contaminant-flagged contigs usually indicate a sequence naming, masking, contamination, or evidence-alignment problem.

## Choosing a Release Gene Set

Use the gene set that is:

- supported by transcript and/or protein evidence
- consistent with related crop annotations
- not inflated by haplotig duplication or unfiltered TE-derived predictions
- compatible with NCBI validation
- reproducible from archived command lines, versions, and inputs

Keep intermediate annotation attempts. Reviewers often ask why a final gene count differs from related assemblies, and older runs can explain whether the difference came from masking, evidence choice, or filtering.

## Release Rule

Do not publish annotation without documenting evidence sources, repeat masking strategy, tool versions, and validation results.
