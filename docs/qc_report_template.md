# Assembly QC Report Template

Use this template for each assembly that will be reviewed internally, included in a manuscript, or prepared for public release.

## Assembly Identity

| Field | Value |
| --- | --- |
| Sample ID |  |
| Species |  |
| Cultivar/accession |  |
| Taxonomy ID |  |
| Ploidy |  |
| Expected haploid genome size |  |
| Assembly version |  |
| Assembly date |  |
| Analyst |  |
| Repository commit |  |

## Input Data

| Data type | File(s) | Yield | Notes |
| --- | --- | --- | --- |
| PacBio HiFi |  |  |  |
| Hi-C |  |  |  |
| RNA-seq |  |  |  |
| Iso-Seq |  |  |  |
| Reference genomes |  |  |  |

Record whether reads were trimmed or filtered. If trimming was used, include the tool, version, parameters, and evidence that trimming improved or did not harm assembly quality.

## Genome Profiling

| Metric | Value | Tool/version |
| --- | --- | --- |
| k-mer size |  |  |
| Estimated genome size |  |  |
| Heterozygosity |  |  |
| Repeat content |  |  |
| Main homozygous peak |  |  |
| Ploidy interpretation |  |  |

Interpretation:

- Does the k-mer profile match the known biology?
- Is there evidence of residual heterozygosity, polyploidy, contamination, or overrepresented organellar DNA?

## Assembly Commands

```bash
# Paste the exact hifiasm command and job identifier here.
```

## Contiguity Metrics

| Metric | Primary assembly | Haplotype 1 | Haplotype 2 | Notes |
| --- | --- | --- | --- | --- |
| Total length |  |  |  |  |
| Number of sequences |  |  |  |  |
| N50 |  |  |  |  |
| L50 |  |  |  |  |
| Longest sequence |  |  |  |  |
| GC content |  |  |  |  |

Interpretation:

- Is the assembly size plausible?
- Are there excess small contigs?
- Is there evidence that haplotigs or homeologs are duplicated in the primary assembly?

## Completeness and Accuracy

| Metric | Value | Tool/version | Notes |
| --- | --- | --- | --- |
| BUSCO lineage |  |  |  |
| BUSCO complete single-copy |  |  |  |
| BUSCO duplicated |  |  |  |
| BUSCO fragmented |  |  |  |
| BUSCO missing |  |  |  |
| Merqury QV |  |  |  |
| Merqury completeness |  |  |  |
| Inspector error summary |  |  |  |

Interpretation:

- Are duplicated BUSCOs expected from biology or likely assembly redundancy?
- Does Merqury indicate high base accuracy?
- Are missing BUSCOs clustered in repeat-rich or low-coverage regions?

## Structural Review

List each whole-genome alignment, dotplot, Hi-C map, optical map, or genetic map used.

| Evidence | File/path | Conclusion |
| --- | --- | --- |
| Reference dotplot |  |  |
| Self dotplot |  |  |
| Assembly-to-assembly dotplot |  |  |
| Hi-C contact map |  |  |
| Read support |  |  |

Misassembly candidates:

| Candidate ID | Sequence | Coordinates | Evidence | Decision |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Contamination Review

| Screen | Result | Action |
| --- | --- | --- |
| FCS-adaptor |  |  |
| FCS-GX |  |  |
| BlobToolKit |  |  |
| sourmash/Kraken/Centrifuge |  |  |
| Chloroplast |  |  |
| Mitochondria |  |  |

Document every removed, masked, or retained suspect sequence.

## Telomere, Centromere, and Gap Status

| Metric | Value | Method |
| --- | --- | --- |
| Expected chromosome number |  |  |
| Chromosome-scale scaffolds |  |  |
| Terminal telomeres detected |  |  |
| Internal telomere signals |  |  |
| Putative centromeres annotated |  |  |
| Gaps |  |  |

## Repeat Annotation

| Metric | Value | Tool/version |
| --- | --- | --- |
| Repeat library method |  |  |
| Total masked percentage |  |  |
| LTR retrotransposon percentage |  |  |
| DNA transposon percentage |  |  |
| Unclassified repeat percentage |  |  |

## Gene Annotation

| Metric | Value | Tool/version |
| --- | --- | --- |
| Annotation strategy |  |  |
| Protein-coding genes |  |  |
| Transcripts |  |  |
| Mean CDS length |  |  |
| BUSCO protein complete |  |  |
| Functional annotation rate |  |  |

## Release Decision

Release status:

- [ ] exploratory assembly only
- [ ] internal draft
- [ ] manuscript draft
- [ ] NCBI pre-submission candidate
- [ ] public release

Required actions before release:

- [ ] FASTA headers validated
- [ ] AGP validated, if applicable
- [ ] FCS reports reviewed
- [ ] organellar sequences handled intentionally
- [ ] annotation validation complete, if submitting annotation
- [ ] BioProject/BioSample/SRA metadata linked
- [ ] methods text drafted

Final decision and rationale:

```text

```

