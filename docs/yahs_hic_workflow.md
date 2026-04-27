# YaHS Hi-C Scaffolding Workflow

YaHS is a fast Hi-C scaffolding tool that takes an assembly FASTA and a Hi-C alignment file, then proposes chromosome-scale scaffolds. For crop genomes, use YaHS as a strong scaffolding engine, but still review the contact map and evidence before release.

YaHS plus Juicebox-style review is now a strong first-class path for crop pangenome work, including recent rice pangenome methods. Its output is still a candidate scaffold set until contact-map, AGP, dotplot, and contamination evidence agree.

## When to Use YaHS

Use YaHS when:

- Hi-C libraries are available for the same sample or a biologically appropriate source
- the contig assembly has already passed contamination/organelle review
- major misassembly candidates have been reviewed before scaffolding
- chromosome-scale scaffolds are expected for the project or manuscript

Pause before using YaHS when:

- the Hi-C library is from a different genotype
- the assembly contains unresolved haplotig duplication
- organellar or contaminant contigs remain in the input FASTA
- the contig count is extremely high and short contigs dominate

## Template Job

Copy the template:

```bash
cp 01_sbatch_templates/yahs_hic_scaffold.sbatch 01_sbatch/
```

Submit:

```bash
sbatch \
  --export assembly=07_assemblies/sample.primary.fa,hic_r1=03_reads_raw/sample_HiC_R1.fastq.gz,hic_r2=03_reads_raw/sample_HiC_R2.fastq.gz,sample=sample \
  01_sbatch/yahs_hic_scaffold.sbatch
```

The template:

1. indexes the assembly with BWA and samtools
2. maps Hi-C reads with `bwa mem -5SP`
3. sorts and indexes the BAM
4. runs YaHS
5. writes a BAM flagstat summary

## Expected Outputs

Typical output directory:

```text
10_scaffolding/sample/yahs/
```

Review files such as:

```text
sample.hic.bam
sample.hic.bam.bai
sample.hic.flagstat.txt
sample.yahs_scaffolds_final.fa
sample.yahs_scaffolds_final.agp
sample.yahs_scaffolds_final.bin
sample.yahs_scaffolds_final.chrom.sizes
```

Exact YaHS output names can vary by version and prefix. Capture `yahs --version` and keep the job logs.

## Contact Map Generation

YaHS provides `juicer pre` support for generating contact maps for Juicebox/JBAT review. The general pattern is:

```bash
juicer pre \
  hic-to-contigs.bin \
  scaffolds_final.agp \
  contigs.fa.fai \
  | sort -k2,2d -k6,6d \
  > alignments_sorted.txt

java -Xmx32G -jar juicer_tools.jar pre \
  alignments_sorted.txt \
  sample.hic \
  scaffolds_final.chrom.sizes
```

For JBAT/manual curation mode, use the YaHS `juicer pre -a` pathway and archive the generated assembly, liftover AGP, and log files.

## Review Questions

- Do chromosome-scale contact blocks look square and continuous?
- Are strong off-diagonal signals biologically plausible or suspicious?
- Are scaffold joins supported by Hi-C contacts on both sides?
- Are small contigs being over-placed into repeat-rich regions?
- Do telomere/centromere expectations agree with scaffold orientation?
- Does the AGP match the scaffold FASTA?
- Do Merqury and FASTA summaries show the expected same sequence content before and after scaffolding, aside from intended gaps/joins?

## Release Rule

Do not release a YaHS scaffold FASTA until the contact map, AGP, dotplot, contamination decisions, and assembly decision logs agree.

## Known Cautions

- Hi-C scaffolding improves order and orientation; it does not improve base accuracy by itself.
- A cleaner contact map is not proof that every small placed contig belongs there.
- T2T or near-gapless claims require separate telomere, centromere, gap, and difficult-repeat evidence.
- Archive YaHS/Juicebox inputs and outputs so manual review can be reproduced.

## References

- YaHS GitHub: https://github.com/c-zhou/yahs
- YaHS paper: https://academic.oup.com/bioinformatics/article/39/1/btac808/6917071
