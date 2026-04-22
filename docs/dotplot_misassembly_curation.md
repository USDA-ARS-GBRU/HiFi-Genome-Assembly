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

See `docs/paf_dotplot_options.md` for PAF-based dotplot options including dotPlotly, pafr, SVbyEye, wgatools, PanDots, and Pteranodon-style visual curation.
See `docs/common_false_positive_corrections.md` before accepting candidate breaks from dotplots, PAF summaries, RagTag, or Pteranodon.

## Manual Reference-to-Assembly Correction

For HiFi crop assemblies, prefer manual evidence-first correction over broad automatic breaking. A practical workflow is:

1. Use dotplots to identify questionable contigs.
2. Map the reference genome to the HiFi assembly with minimap2.
3. Open the HiFi assembly as the IGV genome and load the reference-to-assembly BAM.
4. Manually inspect only the questionable contigs.
5. Record defensible breakpoints and split only where the reference alignment break is clear and independently supported.

See `docs/manual_correction_workflow.md` and `01_sbatch_templates/minimap_reference_to_assembly_igv.sbatch`.

## RagTag Comparison

RagTag can be used as a reference-guided correction and scaffolding comparison after dotplot review. See `docs/ragtag_workflow.md` and `01_sbatch_templates/ragtag_correct_scaffold.sbatch`.

```bash
sbatch \
  --export reference=references/close_reference.fa,query=07_assemblies/sample.primary.fa,sample=sample,mode=both \
  01_sbatch/ragtag_correct_scaffold.sbatch
```

Use RagTag output as a candidate edit set. Do not accept correction or scaffolding changes until they are supported by independent evidence such as Hi-C maps, read-depth profiles, k-mer support, or multiple related references.

Breakwright-style algorithmic searches, RagTag `correct`, and Pteranodon auto mode should be treated as candidate generators. If they nominate many breaks in a high-quality HiFi assembly, assume the tool may be overcorrecting until manual review proves otherwise.

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

Validate the break table before editing:

```bash
scripts/validate_breaks.py \
  --fasta examples/toy/toy_assembly.fa \
  --breaks examples/toy/toy_breaks.tsv \
  -o /tmp/toy_breaks_validation.tsv
```

Toy example:

```bash
scripts/split_fasta_at_breaks.py \
  --fasta examples/toy/toy_assembly.fa \
  --breaks examples/toy/toy_breaks.tsv \
  -o /tmp/toy_split.fa \
  --map /tmp/toy_split.map.tsv
```

See `docs/dotplot_figures.md` for figure and caption expectations.
See `docs/correction_report_examples.md` for manuscript methods and reviewer-response language.
See `docs/agp_after_splitting.md` for AGP review after FASTA edits.

## Release Rule

The final FASTA, AGP, dotplots, Hi-C map, and correction log must agree. If a scaffold is broken or renamed, regenerate downstream repeat, gene, and release validation files or confirm that coordinates remain valid.
