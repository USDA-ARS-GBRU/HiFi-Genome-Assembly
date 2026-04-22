# PAF-Based Dotplot Options

MUMmer remains useful, but minimap2 PAF workflows are fast, flexible, and easy to reuse with modern visualization tools. PAF is especially convenient when comparing large crop genomes, screening many cultivars, or moving between dotplots and IGV/manual curation.

## Generate PAF with minimap2

Use assembly presets based on expected divergence:

```bash
sbatch \
  --export target=references/close_reference.fa,query=07_assemblies/sample.primary.fa,sample=sample_vs_ref,preset=asm20 \
  01_sbatch/minimap_assembly_paf.sbatch
```

Rules of thumb:

- `asm5`: very close assemblies
- `asm10`: close cultivar or subspecies comparisons
- `asm20`: more diverged crop references
- add `-c` when downstream tools benefit from CIGAR in the PAF `cg` tag

## Visualization Options

| Tool | Input | Strength | Caution |
| --- | --- | --- | --- |
| dotPlotly | minimap2 PAF | Static and interactive dotplots; widely used in genome assembly examples | Large plant PAF files may need filtering |
| pafr | minimap2 PAF in R | Scriptable ggplot-style dotplots and coverage plots | Best for custom R workflows |
| SVbyEye | minimap2 PAF | Visualizes pairwise, multi-sequence, self, and whole-genome alignments | Review installation and plotting expectations before large runs |
| wgatools dotplot | PAF/MAF | Interactive HTML output and alignment-detail views | Large interactive plots may need length filtering |
| PanDots | PAF | Pangenome-style chromosome visualizations | Best for selected chromosomes or anchored pangenome comparisons |
| Pteranodon | FASTA inputs with internal alignment/interactive editing | Point-and-click split, invert, join, and rename workflow | Treat auto mode as a candidate generator; verify edits independently |

## dotPlotly Example

```bash
pafCoordsDotPlotly.R \
  -i 09_dotplots/paf/sample_vs_ref.asm20.paf \
  -o 09_dotplots/sample_vs_ref.dotplotly \
  -m 2000 \
  -q 500000 \
  -k 20 \
  -s -t -l -p 12
```

## pafr Example

```r
library(pafr)
library(ggplot2)

ali <- read_paf("09_dotplots/paf/sample_vs_ref.asm20.paf")
p <- dotplot(ali, label_seqs = TRUE, order_by = "qstart") + theme_bw()
ggsave("09_dotplots/sample_vs_ref.pafr_dotplot.png", p, width = 12, height = 12)
```

## wgatools Example

```bash
wgatools dotplot \
  -f paf \
  09_dotplots/paf/sample_vs_ref.asm20.paf \
  > 09_dotplots/sample_vs_ref.wgatools.html
```

## Choosing Filters

For first-pass whole-genome plots, remove tiny alignments that make the plot unreadable. For breakpoint review, lower filters around the candidate contig to avoid hiding the relevant alignment break.

Record:

- minimap2 version
- preset
- whether CIGAR was emitted with `-c`
- minimum alignment length used for plotting
- chromosome/contig filters
- whether secondary alignments were retained or removed

## Release Rule

PAF dotplots can nominate suspicious regions, but they do not prove a misassembly by themselves. Manual break decisions should still reference the correction log, validation output, and at least one independent support track.

## Tool Links

- minimap2: https://github.com/lh3/minimap2
- dotPlotly: https://github.com/tpoorten/dotPlotly
- pafr: https://dwinter.github.io/pafr/
- SVbyEye: https://github.com/daewoooo/SVbyEye
- wgatools: https://github.com/wjwei-handsome/wgatools
- PanDots: https://pypi.org/project/pandots/
- Pteranodon: https://github.com/w-korani/Pteranodon
