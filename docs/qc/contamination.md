# Contamination Review

Contamination review is a release gate. A crop plant genome assembly should not be submitted publicly until adapter/vector sequence, cross-species contamination, and unintended organellar sequence have been screened and documented.

## Evidence Layers

| Layer | Purpose | Typical tools |
| --- | --- | --- |
| Adapter/vector | detect library artifacts and synthetic sequence | NCBI FCS-adaptor, VecScreen |
| Cross-species contamination | detect bacterial, fungal, animal, or wrong-plant sequence | NCBI FCS-GX, BlobToolKit, BLAST |
| Read-level taxonomy | check raw data before assembly | sourmash, Kraken2, Centrifuge |
| GC/coverage/taxonomy outliers | identify suspicious contig clusters | BlobToolKit |
| Organelle sequence | distinguish free organelle contigs from nuclear organellar insertions | minimap2/BLAST against organelle references |

## Directory Layout

```text
11_contamination/
  fcs_adaptor/
  fcs_gx/
  sourmash/
  blobtoolkit/
  organelle/
  decisions/
```

## Read-Level Screening

Use sourmash or a comparable taxonomic screen before assembly when possible:

```bash
sbatch \
  --export reads="03_reads_raw/sample.fastq.gz",sample=sample,database=/path/to/ncbi-euks-plants.dna.k51.sig.zip,k=51,scaled=1000 \
  01_sbatch/sourmash_reads.sbatch
```

The top containment hits should match the expected species, genus, or close relatives. Strong unrelated plant, bacterial, fungal, or animal signals require review.

## Assembly-Level Screening

Run NCBI FCS on release candidates:

```bash
sbatch \
  --export assembly=15_release/sample.genome.fa,sample=sample,fcs_image=/path/to/fcs-adaptor.sif \
  01_sbatch/fcs_adaptor.sbatch

sbatch \
  --export assembly=15_release/sample.genome.fa,sample=sample,taxid=NCBI_TAXID,fcs_image=/path/to/fcs-gx.sif,gx_db=/path/to/gxdb \
  01_sbatch/fcs_gx.sbatch
```

Follow current NCBI instructions for FCS setup because databases and container commands can change.

## BlobToolKit Review

BlobToolKit is useful when it combines:

- assembly FASTA
- read coverage
- taxonomic hits
- BUSCO results

Review contigs with unusual GC, unexpected coverage, non-plant taxonomy, organelle-like hits, or clusters inconsistent with the rest of the assembly.

## Organelle Decisions

Crop HiFi assemblies often contain chloroplast and mitochondrial sequence. This is not automatically contamination. Decide whether each sequence is:

- a free organelle contig to remove from the nuclear assembly
- a valid nuclear organellar insertion to retain
- a chimeric sequence to split only with evidence
- a separate organelle record to submit independently

See `../organelle_workflow.md`.

## Decision Categories

| Decision | Use when |
| --- | --- |
| keep | sequence is expected nuclear genome sequence |
| remove | clear contaminant or free organelle sequence not intended for nuclear release |
| mask | localized sequence should remain but be masked |
| split | sequence is chimeric and a supported break is required |
| submit_separately | organelle or symbiont sequence should be released independently |
| review | evidence is insufficient for final action |

## Release Rule

Every action other than `keep` should be represented in the contamination decision table and assembly decision log. After removal, masking, or splitting, regenerate FASTA indexes, AGP when relevant, QC dashboards, and release manifests.
