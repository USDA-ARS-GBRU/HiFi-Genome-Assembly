# Dotplot and Misassembly Curation

Dotplots are one of the fastest ways to find large assembly problems, but they are also easy to overinterpret. Crop genomes contain repeats, real structural variation, introgressions, polyploid segments, and reference errors. Use dotplots as evidence, not as automatic correction commands.

## Review Inputs

Collect:

- assembly FASTA
- closest available reference FASTA
- at least one alternate related assembly when available
- HiFi read alignment depth
- Hi-C contact map if scaffolding was done
- BUSCO, Merqury, and k-mer evidence
- contamination and organelle review decisions
- assembly decision log

## Alignment Options

For chromosome-scale review, use MUMmer or minimap2/paftools-style workflows.

```bash
nucmer --maxmatch -t 32 -p sample_vs_ref reference.fa sample.fa
delta-filter -1 sample_vs_ref.delta > sample_vs_ref.1delta
mummerplot --png --large --layout -p sample_vs_ref sample_vs_ref.1delta
```

```bash
minimap2 -x asm20 -t 32 reference.fa sample.fa > sample_vs_ref.paf
```

Use more permissive presets for distant references and more stringent filters for close cultivar-to-cultivar comparisons.

## Decision Cases

| Pattern | Possible meaning | Before editing | Default action |
| --- | --- | --- | --- |
| Single clean diagonal | Strong chromosome-scale agreement | Check chromosome naming and orientation | Retain |
| Terminal orientation flip | Inversion, orientation error, or reference difference | Check Hi-C, reads, related assemblies | Retain or flip only with independent support |
| Mid-contig chromosome jump | Chimera, translocation, introgression, or reference problem | Check read depth, Hi-C break, k-mers, alternate references | Break only when multiple evidence types support misassembly |
| Repeated block | Segmental duplication, haplotig duplication, collapsed repeat, or TE-rich region | Check depth and purge statistics | Retain, purge, or annotate depending on evidence |
| Reference gap filled by assembly | True improvement, contaminant insertion, or organellar insertion | Check taxonomy, read support, and related assemblies | Retain if supported |

Example decision rows are in `examples/dotplot_decisions.tsv`.

## Evidence Standard for Breaking an Assembly

Breaking a contig or scaffold is a serious edit. Require at least two independent signals when possible:

- abrupt Hi-C contact map break
- HiFi read alignments stop or change orientation at the same position
- k-mer support drops or changes copy number
- alignment to multiple related references supports the break
- contamination or organelle screen supports non-nuclear origin
- the break improves AGP/scaffold consistency without reducing supported sequence

Do not break solely because of one dotplot against one reference. Crop references may contain cultivar-specific inversions, presence/absence variation, or their own misassemblies.

## Correction Log Template

For every proposed edit, record the evidence in `docs/correction_decision_log_template.md`.

Minimal fields:

```text
edit_id:
sequence_id:
coordinates:
proposed_action: retain, break, reverse_complement, reorder, remove, mask, submit_separately
primary_evidence:
secondary_evidence:
tools_and_versions:
reviewer:
date:
final_decision:
reason_not_automated:
```

For break edits, `scripts/split_fasta_at_breaks.py` accepts a TSV with `sequence_id` and `break_after_1based` columns. A value of `1000` means the first output segment ends at base 1000 and the next begins at base 1001.

Toy example:

```bash
scripts/split_fasta_at_breaks.py \
  --fasta examples/toy/toy_assembly.fa \
  --breaks examples/toy/toy_breaks.tsv \
  -o /tmp/toy_split.fa \
  --map /tmp/toy_split.map.tsv
```

See `docs/dotplot_figures.md` for figure and caption expectations.

## Release Rule

The final FASTA, AGP, dotplots, Hi-C map, and correction log must agree. If a scaffold is broken or renamed, regenerate downstream repeat, gene, and release validation files or confirm that coordinates remain valid.
