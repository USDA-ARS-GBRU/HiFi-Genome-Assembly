# hifiasm Parameters and Assembly Modes

hifiasm defaults are strong for PacBio HiFi reads. For crop plant genomes, start with defaults unless biology, k-mer profiles, or diagnostic assemblies provide a clear reason to change parameters.

Recent crop pangenome papers support this conservative default: use hifiasm as the primary HiFi contig assembler, then use scaffolding, QC, and annotation evidence to decide whether the output is suitable for release.

## Default HiFi-Only Primary Assembly

Use this for many inbred or moderately heterozygous diploid crop samples:

```bash
hifiasm \
  -t 32 \
  -o 06_hifiasm/sample/sample \
  03_reads_raw/sample.fastq.gz \
  2> 00_log/hifiasm_sample.err
```

Expected review outputs:

- `*.bp.p_ctg.gfa`: primary contigs
- `*.bp.a_ctg.gfa`: alternate contigs, when generated
- hifiasm log with collected bases and peak estimates

The primary contig assembly is often the practical release candidate for inbred crops, but it still needs BUSCO, Merqury, contamination review, and dotplots.

## Preserve Run Context

Record these details for every hifiasm run:

- hifiasm version and command line
- input read files and read-filtering decisions
- thread count, memory request, and cluster job ID
- GFA outputs retained
- FASTA conversion command
- hifiasm log and extracted coverage/genome-size peaks
- whether overlap/cache/bin files were reused or regenerated

If you rerun hifiasm with new parameters or a different read set, keep it as a separate candidate rather than overwriting the earlier run.

## Hi-C Integrated Mode

Use when Hi-C reads are from the same genotype and the goal includes haplotype phasing:

```bash
hifiasm \
  -t 48 \
  -o 06_hifiasm/sample_hic/sample_hic \
  --h1 hic_R1.fastq.gz \
  --h2 hic_R2.fastq.gz \
  03_reads_raw/sample.fastq.gz \
  2> 00_log/hifiasm_sample_hic.err
```

Hi-C integrated hifiasm output is not the final chromosome-scale scaffold. Use YaHS, 3D-DNA/JBAT, or another scaffolding workflow after reviewing the contigs.

Treat hifiasm Hi-C mode as phasing support, not as a substitute for scaffolding contact-map review.

## Trio Mode

Use trio mode when parental short-read data are available and the parents are appropriate representatives of the assembled individual.

Best use cases:

- F1 or heterozygous crop material with known parents
- projects where haplotype-resolved assemblies are a deliverable
- breeding material where parental haplotypes matter biologically

Cautions:

- Wrong or contaminated parental reads can mis-bin sequence.
- Trio mode does not remove the need for QC, dotplots, and contamination screening.
- Haplotype assemblies should be evaluated separately, not only as a pair.

## Diagnostic `-l0`

`-l0` disables hifiasm's default purging behavior. Treat it as a diagnostic for inbred or unusual samples, not as an automatic improvement.

```bash
hifiasm \
  -t 32 \
  -l0 \
  -o 06_hifiasm/sample_l0/sample_l0 \
  03_reads_raw/sample.fastq.gz \
  2> 00_log/hifiasm_sample_l0.err
```

Compare default and `-l0` outputs using:

- total assembly size
- contig count and N50
- BUSCO duplication
- Merqury spectra-cn
- read-depth behavior
- dotplots and obvious duplicated blocks

## `--hom-cov`

Use `--hom-cov` only when hifiasm mis-detects homozygous coverage and you have independent evidence from k-mer spectra or read-depth analysis.

Good evidence:

- clear GenomeScope/Smudgeplot coverage peak
- consistent hifiasm log behavior across runs
- expected genome size and read coverage are known

Poor evidence:

- changing `--hom-cov` until N50 looks better
- forcing the assembly to match a reference genome size
- trying to hide heterozygosity or polyploid structure

## Other Parameter Audits

These parameters are sometimes useful, but they should be deliberate:

| Parameter or behavior | Use | Caution |
| --- | --- | --- |
| `--primary` | force primary-only output behavior in some workflows | can hide useful alternate sequence review context |
| `-s` | tune graph cleaning/stringency | compare with default before trusting improvements |
| `-z` | adjust overlap length filtering for short reads or unusual datasets | changes graph behavior; document why |
| `--write-paf` / `--write-ec` | preserve diagnostic overlaps or corrected reads when supported by the installed version | large files; plan storage |
| cached overlaps/bin files | speed reruns with the same inputs | do not reuse after changing read sets or incompatible parameters |

## Polyploid Cautions

Polyploid crops can have homeologous sequence, recent duplications, and allele dosage patterns that look confusing under diploid assumptions.

For polyploids:

- inspect k-mer spectra before assembly
- avoid interpreting all duplicated BUSCOs as assembly error
- compare homeolog-specific structure when references are available
- be cautious with purging and reference-guided correction
- document whether the release represents a haploid-like reference, primary assembly, or haplotype/subgenome-aware product

For large polyploid crops, recent wheat work still supports hifiasm as a viable contig assembler, but the review burden shifts toward representation, subgenome/homeolog interpretation, contact-map review, and repeat-aware QC.

## Output Selection

| Output | Use |
| --- | --- |
| primary contigs | common release candidate for inbred or primary references |
| alternate contigs | useful for heterozygosity review and unrepresented alleles |
| hap1/hap2 contigs | useful for phased or haplotype-level projects |
| Hi-C phased contigs | useful starting point for haplotype scaffolding |
| diagnostic parameter runs | compare and document, but do not release without evidence |

## Decision Rule

Choose the assembly mode that best matches the biology and release goal, not the mode that maximizes contiguity alone. Every non-default parameter should have a recorded reason in the assembly decision log.
