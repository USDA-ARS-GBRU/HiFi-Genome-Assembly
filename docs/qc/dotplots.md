# Dotplots for Assembly Review

Dotplots show large-scale alignment structure between assemblies or between an assembly and a reference. They are fast, visual, and extremely useful for crop genome review, but they are not automatic proof of misassembly.

## When to Make Dotplots

Make dotplots:

- after the first contig assembly
- before destructive correction
- after manual breaks or reorientation
- before and after scaffolding
- when comparing raw-read, filtered-read, default, and diagnostic assemblies
- for any chromosome or scaffold discussed in a manuscript or reviewer response

## MUMmer Workflow

MUMmer remains a strong option for assembly-vs-reference plots:

```bash
nucmer --maxmatch -t 32 -p sample_vs_ref reference.fa sample.fa
delta-filter -1 sample_vs_ref.delta > sample_vs_ref.1delta
mummerplot --png --large --layout -p sample_vs_ref sample_vs_ref.1delta
```

Use this when you want classic whole-genome collinearity plots and a close enough reference is available.

## minimap2 PAF Workflow

PAF workflows are fast and flexible for large crop genomes:

```bash
minimap2 -x asm20 -t 32 reference.fa sample.fa > sample_vs_ref.paf
```

Rule of thumb:

| Preset | Use |
| --- | --- |
| `asm5` | very close assemblies |
| `asm10` | close cultivar or subspecies comparisons |
| `asm20` | more diverged crop references |

Add `-c` when downstream tools need CIGAR in the PAF `cg` tag.

## Visualization Options

| Tool | Input | Strength |
| --- | --- | --- |
| mummerplot | MUMmer delta | classic static dotplots |
| dotPlotly | PAF | static and interactive genome dotplots |
| pafr | PAF | scriptable R/ggplot workflows |
| SVbyEye | PAF or FASTA workflows | visual structural variant exploration |
| wgatools dotplot | PAF/MAF | interactive HTML output |
| PanDots | PAF | pangenome-style selected chromosome views |
| Pteranodon | FASTA/alignments | visual curation and candidate editing |

## Interpretation Patterns

| Pattern | Possible meaning | Default response |
| --- | --- | --- |
| clean diagonal | broad collinearity | retain |
| terminal flip | true inversion, orientation error, or reference difference | check Hi-C/read evidence before flipping |
| chromosome jump | chimera, translocation, introgression, or reference error | inspect independent evidence |
| repeated block | segmental duplication, haplotig duplication, TE-rich region | check depth and Merqury spectra |
| assembly-only sequence | genuine insertion, reference gap, contamination, or organelle sequence | screen taxonomy and read support |

## Evidence Standard

Do not break, remove, flip, or reorder sequence based only on one dotplot against one reference. Require independent support such as:

- Hi-C contact-map break
- HiFi read mapping change at the same coordinate
- k-mer or coverage support
- multiple related references
- contamination/organelle evidence
- validated AGP/scaffold consistency

## Figure Expectations

Captions should state:

- assembly version
- reference and version
- aligner and preset
- alignment filters
- region shown
- decision made from the figure

Use `docs/dotplot_figures.md` for more figure/caption guidance.

## Related Pages

- [Dotplot and misassembly curation](../dotplot_misassembly_curation.md)
- [PAF-based dotplot options](../paf_dotplot_options.md)
- [Manual correction workflow](../manual_correction_workflow.md)
- [Correction report examples](../correction_report_examples.md)
