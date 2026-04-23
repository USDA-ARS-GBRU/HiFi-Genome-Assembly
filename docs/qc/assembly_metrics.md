# Assembly Metrics and Interpretation

Assembly metrics are evidence, not verdicts. A peer-review-quality crop genome should be evaluated with contiguity, gene-space completeness, k-mer completeness, base accuracy, structural evidence, contamination review, and biological context.

## Minimum Metric Set

| Category | Useful metrics |
| --- | --- |
| Input reads | total bases, read count, read N50, estimated coverage, k-mer profile |
| Contiguity | total length, sequence count, N50, N90, L50, largest contig/scaffold |
| Completeness | BUSCO genome score with lineage and version |
| Base accuracy | Merqury QV and k-mer completeness |
| Duplication | BUSCO duplicated, Merqury spectra-cn, purge/duplication reports |
| Structural quality | dotplots, Hi-C map, read mapping, Inspector if used |
| Contamination | FCS-adaptor, FCS-GX, BlobToolKit, sourmash, organelle review |
| Release readiness | FASTA validation, AGP validation, manifest audit |

## Contiguity

Start with `seqkit`, BBTools `stats.sh`, or QUAST:

```bash
seqkit stats -a 07_assemblies/*.fa > 08_stats/seqkit_assembly_stats.tsv
```

```bash
stats.sh in=07_assemblies/sample.primary.fa format=3 -Xmx4g > 08_stats/sample.primary.bbtools_stats.txt
```

```bash
quast.py \
  -t 16 \
  -o 08_stats/quast_sample \
  --large \
  --est-ref-size 1000000000 \
  07_assemblies/sample.primary.fa
```

N50 is useful for comparing assembly candidates, but it is not a quality claim by itself. A wrong scaffold join can improve N50 while making the genome biologically worse.

## BUSCO

BUSCO estimates conserved gene-space completeness.

```bash
busco \
  -i 07_assemblies/sample.primary.fa \
  -m genome \
  -l embryophyta_odb12 \
  -o sample.busco \
  --out_path 08_stats/busco \
  -c 32
```

Interpretation:

- High complete single-copy BUSCOs support gene-space completeness.
- Duplicated BUSCOs can reflect unpurged haplotigs, polyploidy, real duplication, or recent whole-genome duplication.
- Missing BUSCOs can reflect assembly gaps, wrong lineage choice, true biology, or contamination filtering mistakes.

Always state the BUSCO lineage dataset and version.

## Merqury

Merqury uses read k-mers to estimate consensus quality value and assembly completeness without requiring a reference genome.

Record:

- k-mer size
- read set used to build the meryl database
- QV
- completeness
- spectra-cn interpretation

Merqury spectra-cn plots are especially useful for distinguishing collapsed repeats, duplicated haplotigs, and missing sequence.

## QUAST With a Reference

QUAST can report reference-based signals when a close reference is available:

```bash
quast.py \
  -t 16 \
  -o 08_stats/quast_sample_ref \
  -r references/close_reference.fa \
  --large \
  07_assemblies/sample.primary.fa
```

Reference-based warnings require interpretation. A crop accession may contain real inversions, introgressions, or presence/absence variation relative to the reference.

## Inspector and Read-Mapping Evidence

Inspector and read-to-assembly mapping can localize likely base or structural errors. Use these when:

- read support around a correction is important
- reviewers request read-backed evidence
- dotplot or Hi-C signals suggest possible misassembly

Read mapping is a support layer; it does not replace whole-genome structural review.

## Dashboard

Use the project helper to combine metrics:

```bash
scripts/collect_qc_dashboard.py \
  --seqkit 08_stats/seqkit_assembly_stats.tsv \
  --hifiasm-logs 00_log/hifiasm_*.err \
  --busco 08_stats/busco/*/short_summary*.txt \
  --quast 08_stats/quast*/report.tsv \
  --merqury 08_stats/merqury/*.txt \
  -o 08_stats/assembly_qc_dashboard.tsv
```

## Decision Rule

Do not accept or reject an assembly based on one number. A defensible release candidate has coherent evidence across contiguity, completeness, base accuracy, structure, contamination, annotation readiness, and documented biological expectations.
