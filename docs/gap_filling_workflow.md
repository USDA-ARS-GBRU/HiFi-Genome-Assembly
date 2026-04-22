# Gap Filling Workflow

Gap filling is the process of replacing `N` runs in scaffolded assemblies with sequence. It is not the same as general polishing, and it should not be run automatically on every crop assembly.

## When to Consider Gap Filling

Consider gap filling when:

- scaffolded chromosomes contain biologically important gaps
- HiFi or ONT reads span the gap
- Hi-C or optical-map evidence supports the surrounding scaffold structure
- the project is aiming for near-gapless or T2T-ready chromosomes
- the filled sequence can be validated independently

Pause when:

- gaps represent uncertain scaffold joins
- contaminant or organellar sequence has not been reviewed
- the gap is in a complex repeat with no confident local evidence
- filling would obscure uncertainty before NCBI submission

## First Step: Count Gaps

```bash
scripts/summarize_fasta_gaps.py \
  10_scaffolding/sample.scaffolds.fa \
  -o 10_scaffolding/sample.gaps.tsv \
  --summary 10_scaffolding/sample.gap_summary.tsv
```

Use the gap table to prioritize gaps by length, chromosome, evidence, and biological importance.

## Tool Options

| Tool | Best use | Inputs | Cautions |
| --- | --- | --- | --- |
| LR_Gapcloser | Long-read gap closure with raw or corrected reads | scaffold FASTA plus long-read FASTA | Older Perl/shell workflow; review output carefully |
| TGS-GapCloser2 | Long-read gap closure for large genomes | scaffold FASTA plus TGS read FASTA | FASTA read input expected; validate filled sequence and details |
| Gapless | Combined scaffolding, gap filling, and assembly correction | long reads plus draft assembly | Treat correction behavior conservatively |
| TRFill | Complex repeat-region gap filling, including T2T-style gaps | homologous reference, assembly, HiFi/ONT, optional Hi-C | Best for targeted complex gaps; requires careful config |

## Template Jobs

LR_Gapcloser:

```bash
sbatch \
  --export scaffolds=10_scaffolding/sample.scaffolds.fa,reads_fasta=03_reads_raw/sample.hifi.fa,sample=sample,platform=p \
  01_sbatch/lr_gapcloser.sbatch
```

TGS-GapCloser2:

```bash
sbatch \
  --export scaffolds=10_scaffolding/sample.scaffolds.fa,reads_fasta=03_reads_raw/sample.hifi.fa,sample=sample,tgstype=hifi \
  01_sbatch/tgsgapcloser2.sbatch
```

TRFill:

```bash
sbatch \
  --export config=00_metadata/trfill.haploid.config.txt,sample=sample,reads_format=HiFi \
  01_sbatch/trfill.sbatch
```

## Validation After Gap Filling

After any fill:

1. Count gaps before and after.
2. Compare FASTA statistics before and after.
3. Align the filled assembly against the pre-fill assembly.
4. Map HiFi reads across filled regions.
5. Review Hi-C support around filled scaffold intervals.
6. Validate AGP and FASTA headers.
7. Re-run BUSCO/Merqury where appropriate.
8. Document accepted and rejected fills in a gap-filling decision log.

## Decision Log

Use `examples/gap_filling_decisions.tsv` as a starter table. At minimum, record:

- gap ID
- sequence ID
- gap coordinates
- proposed tool
- final decision
- read evidence
- Hi-C/reference evidence
- reviewer/date
- downstream files regenerated

## Release Rule

Do not remove all Ns simply to make a genome look finished. A documented unresolved gap is better than an unsupported fill.

## References and Tools

- Comprehensive evaluation of long-read gap-filling tools: https://pubmed.ncbi.nlm.nih.gov/38275608/
- LR_Gapcloser paper: https://academic.oup.com/gigascience/article/8/1/giy157/5256637
- LR_Gapcloser GitHub: https://github.com/CAFS-bioinformatics/LR_Gapcloser
- TGS-GapCloser paper: https://academic.oup.com/gigascience/article/9/9/giaa094/5902284
- TGS-GapCloser2 GitHub: https://github.com/BGI-Qingdao/TGS-GapCloser2
- Gapless paper: https://www.life-science-alliance.org/content/6/7/e202201471
- Gapless GitHub: https://github.com/schmeing/gapless
- TRFill paper: https://pubmed.ncbi.nlm.nih.gov/40721805/
- TRFill GitHub: https://github.com/panlab-bioinfo/TRFill
