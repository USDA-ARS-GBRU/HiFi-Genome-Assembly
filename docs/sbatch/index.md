# sbatch Templates

This section catalogs the reusable Slurm templates in `01_sbatch_templates/`.

Treat them as starting points for project-local copies in `01_sbatch/`, not as universal scripts that should run unchanged on every cluster.

## Assembly and Input Templates

| Template | Purpose | Example |
| --- | --- | --- |
| `bam2fastq.sbatch` | Converts PacBio BAM input to FASTQ for downstream workflows that expect FASTQ. | `sbatch --export bam=03_reads_raw/sample.bam,outdir=03_reads_raw 01_sbatch/bam2fastq.sbatch` |
| `btrim_hifi_adapters.sbatch` | Screens or trims adapter sequence using `btrim` for HiFi read preprocessing. | `sbatch --export reads=03_reads_raw/sample.fastq.gz,patterns=examples/btrim_patterns.example.txt,sample=sample 01_sbatch/btrim_hifi_adapters.sbatch` |
| `hifiasm.sbatch` | Runs hifiasm for the main PacBio HiFi assembly step. | `sbatch --export reads=03_reads_raw/sample.fastq.gz,sample=sample 01_sbatch/hifiasm.sbatch` |
| `assembly_stats.sbatch` | Collects first-pass assembly statistics after FASTA generation. | `sbatch --export fasta=07_assemblies/sample.primary.fa,sample=sample 01_sbatch/assembly_stats.sbatch` |
| `busco.sbatch` | Runs BUSCO on an assembly or annotation output. | `sbatch --export fasta=07_assemblies/sample.primary.fa,lineage=embryophyta_odb12,sample=sample 01_sbatch/busco.sbatch` |
| `merqury.sbatch` | Runs Merqury for k-mer completeness and QV review. | `sbatch --export reads=03_reads_raw/sample.fastq.gz,fasta=07_assemblies/sample.primary.fa,sample=sample 01_sbatch/merqury.sbatch` |
| `mummer_plot.sbatch` | Builds MUMmer-based dotplots for structural review. | `sbatch --export ref=references/ref.fa,query=07_assemblies/sample.primary.fa,sample=sample 01_sbatch/mummer_plot.sbatch` |
| `minimap_assembly_paf.sbatch` | Builds minimap2 PAF alignments for dotplotting or structural review. | `sbatch --export ref=references/ref.fa,query=07_assemblies/sample.primary.fa,sample=sample 01_sbatch/minimap_assembly_paf.sbatch` |
| `minimap_hifi_to_assembly.sbatch` | Aligns HiFi reads back to the assembly for support review. | `sbatch --export reads=03_reads_raw/sample.fastq.gz,fasta=07_assemblies/sample.primary.fa,sample=sample 01_sbatch/minimap_hifi_to_assembly.sbatch` |

## Contamination and Organelle Templates

| Template | Purpose | Example |
| --- | --- | --- |
| `blobtoolkit_prep.sbatch` | Prepares BlobToolKit inputs such as coverage and taxonomic support tables. | `sbatch --export fasta=07_assemblies/sample.primary.fa,bam=08_stats/sample_vs_assembly.bam,sample=sample 01_sbatch/blobtoolkit_prep.sbatch` |
| `fcs_adaptor.sbatch` | Runs NCBI FCS-adaptor screening for adapters and vectors. | `sbatch --export fasta=07_assemblies/sample.primary.fa,sample=sample 01_sbatch/fcs_adaptor.sbatch` |
| `fcs_gx.sbatch` | Runs NCBI FCS-GX cross-species contamination review. | `sbatch --export fasta=07_assemblies/sample.primary.fa,sample=sample 01_sbatch/fcs_gx.sbatch` |
| `organelle_screen.sbatch` | Screens assembly sequences against organelle references. | `sbatch --export fasta=07_assemblies/sample.primary.fa,organelle_db=references/organelle.fa,sample=sample 01_sbatch/organelle_screen.sbatch` |
| `sourmash_reads.sbatch` | Sketches and searches reads with sourmash for fast contamination review. | `sbatch --export reads=03_reads_raw/sample.fastq.gz,db=references/plant_db.sig.zip,sample=sample 01_sbatch/sourmash_reads.sbatch` |

## Curation Templates

| Template | Purpose | Example |
| --- | --- | --- |
| `minimap_reference_to_assembly_igv.sbatch` | Aligns a reference genome to the assembly for IGV-based breakpoint review. | `sbatch --export ref=references/ref.fa,assembly=07_assemblies/sample.primary.fa,sample=sample 01_sbatch/minimap_reference_to_assembly_igv.sbatch` |
| `post_correction_validation.sbatch` | Re-runs validation after accepted manual corrections. | `sbatch --export before=07_assemblies/sample.primary.fa,after=07_assemblies/sample.corrected.fa,sample=sample 01_sbatch/post_correction_validation.sbatch` |

## Scaffolding and Gap-Filling Templates

| Template | Purpose | Example |
| --- | --- | --- |
| `3d_dna_scaffold.sbatch` | Runs 3D-DNA scaffolding with Hi-C alignments. | `sbatch --export assembly=07_assemblies/sample.primary.fa,hic_bam=10_scaffolding/sample.hic.bam,sample=sample 01_sbatch/3d_dna_scaffold.sbatch` |
| `yahs_hic_scaffold.sbatch` | Runs YaHS for Hi-C scaffolding. | `sbatch --export assembly=07_assemblies/sample.primary.fa,hic_bam=10_scaffolding/sample.hic.bam,sample=sample 01_sbatch/yahs_hic_scaffold.sbatch` |
| `ragtag_correct_scaffold.sbatch` | Runs RagTag correction or scaffolding against a related reference. | `sbatch --export assembly=07_assemblies/sample.primary.fa,reference=references/ref.fa,sample=sample 01_sbatch/ragtag_correct_scaffold.sbatch` |
| `lr_gapcloser.sbatch` | Runs LR_Gapcloser on a scaffolded assembly. | `sbatch --export assembly=10_scaffolding/sample.scaffolds.fa,reads=03_reads_raw/sample.fastq.gz,sample=sample 01_sbatch/lr_gapcloser.sbatch` |
| `tgsgapcloser2.sbatch` | Runs TGS-GapCloser2 for long-read gap filling. | `sbatch --export assembly=10_scaffolding/sample.scaffolds.fa,reads=03_reads_raw/sample.fastq.gz,sample=sample 01_sbatch/tgsgapcloser2.sbatch` |
| `trfill.sbatch` | Runs TRFill for difficult repeat-associated gap filling. | `sbatch --export assembly=10_scaffolding/sample.scaffolds.fa,reads=03_reads_raw/sample.fastq.gz,sample=sample 01_sbatch/trfill.sbatch` |

## T2T and Repeat Templates

| Template | Purpose | Example |
| --- | --- | --- |
| `tidk_telomere.sbatch` | Runs tidk to summarize telomere motifs and terminal evidence. | `sbatch --export fasta=07_assemblies/sample.primary.fa,motif=TTTAGGG,sample=sample 01_sbatch/tidk_telomere.sbatch` |
| `quartet_telomere_centromere.sbatch` | Runs quarTeT-style telomere and centromere evaluation. | `sbatch --export fasta=07_assemblies/sample.primary.fa,sample=sample 01_sbatch/quartet_telomere_centromere.sbatch` |
| `edta.sbatch` | Runs EDTA for plant-focused repeat annotation. | `sbatch --export genome=07_assemblies/sample.primary.fa,sample=sample,species=others,sensitive=1 01_sbatch/edta.sbatch` |
| `repeatmodeler_repeatmasker.sbatch` | Runs RepeatModeler2 and RepeatMasker for a de novo repeat workflow. | `sbatch --export genome=07_assemblies/sample.primary.fa,sample=sample 01_sbatch/repeatmodeler_repeatmasker.sbatch` |

## Gene Annotation Templates

| Template | Purpose | Example |
| --- | --- | --- |
| `liftoff.sbatch` | Transfers annotation from a related reference using Liftoff. | `sbatch --export target_genome=13_repeats/sample.softmasked.fa,reference_genome=references/ref.fa,reference_gff=references/ref.gff3,sample=sample 01_sbatch/liftoff.sbatch` |
| `braker3.sbatch` | Runs BRAKER3 with transcript and protein evidence. | `sbatch --export genome=13_repeats/sample.softmasked.fa,rnaseq_bam=14_genes/rnaseq/sample.bam,proteins=14_genes/evidence/proteins.fa,species=Genus_species_sample 01_sbatch/braker3.sbatch` |
| `maker.sbatch` | Runs MAKER for integrated annotation. | `sbatch --export control_dir=14_genes/maker/control_files,outdir=14_genes/maker/run 01_sbatch/maker.sbatch` |
| `table2asn_validate.sbatch` | Runs table2asn validation for release-ready annotation packages. | `sbatch --export fasta=15_release/sample.genome.fa,gff=15_release/sample.annotation.gff3,template=00_metadata/template.sbt,sample=sample 01_sbatch/table2asn_validate.sbatch` |

## How To Use These Templates

Good habits:

- copy templates into `01_sbatch/` before editing
- document cluster-specific changes in your decision log
- keep the environment method and module versions next to the template you actually ran
- treat gap filling, reference-guided scaffolding, and annotation templates as later-stage tools, not day-one defaults

## Related Pages

- [sbatch template index](../sbatch_template_index.md)
- [Project starter kit](../project_starter_kit.md)
- [Scripts](../scripts/index.md)
