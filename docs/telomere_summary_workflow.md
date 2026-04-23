# Telomere Summary Workflow

Telomere summaries help support chromosome-orientation and completeness claims. In most plants the canonical telomeric motif is `TTTAGGG`, but exceptions exist. Confirm the expected motif for the crop lineage before interpreting results.

## Quick Motif Summary

Use the helper for a fast terminal-window scan:

```bash
scripts/summarize_telomeres.py \
  10_scaffolding/sample.final.fa \
  --motif TTTAGGG \
  --window 10000 \
  --min-hits 3 \
  -o 12_telomere_centromere/sample.telomere_summary.tsv
```

Output classes:

| Status | Meaning |
| --- | --- |
| terminal_telomere_both | motif hits meet threshold near both sequence ends |
| terminal_telomere_one | motif hits meet threshold near one sequence end |
| internal_telomere_review | internal motif signal needs review |
| no_telomere_signal | no motif signal above threshold |

## Interpretation

- A positive terminal motif call supports completeness but does not prove a chromosome is T2T by itself.
- Missing motif signal may be biological, assembly-related, or caused by using the wrong motif.
- Internal signal can indicate a true interstitial telomeric repeat, a misjoin, or an unreviewed artifact.
- Repeat-rich subtelomeric regions can be difficult to assemble even with HiFi reads.

## Stronger Options

Use `tidk` and `quarTeT` for deeper review:

```bash
tidk search \
  --string TTTAGGG \
  --output 12_telomere_centromere/sample.tidk \
  10_scaffolding/sample.final.fa
```

```bash
quartet.py TeloExplorer \
  -i 10_scaffolding/sample.final.fa \
  -c plant \
  -o 12_telomere_centromere/quartet_telomere
```

HPC templates are available in:

```text
01_sbatch_templates/tidk_telomere.sbatch
01_sbatch_templates/quartet_telomere_centromere.sbatch
```

## Release Rule

Do not claim telomere-to-telomere chromosomes from motif counts alone. Combine terminal telomere evidence with gap status, centromere candidates, Hi-C contact maps, dotplots, and unresolved repeat review.
