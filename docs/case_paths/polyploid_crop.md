# Polyploid Crop Path

This path is for a crop genome where polyploidy, homeolog similarity, or mixed ploidy signals make a simple diploid-first interpretation risky.

## Typical Goal

Produce the most defensible assembly representation for the project stage without forcing a false diploid simplification.

## Suggested Path

1. Start with the [project starter kit](../project_starter_kit.md)
2. Spend extra time in [genome profiling](../assembly/genome_profiling.md) before choosing the assembly strategy
3. Run [hifiasm](../assembly/hifiasm.md) conservatively and compare outputs carefully
4. Use [assembly metrics](../qc/assembly_metrics.md) and [dotplots](../qc/dotplots.md) to distinguish redundancy from expected homeolog structure
5. Avoid aggressive purging until you understand what is true duplication versus assembly excess
6. Use [curation](../curation/index.md) only for strong structural evidence, not to force a cleaner ploidy story
7. Delay chromosome-scale claims until the representation is clearly defined
8. Freeze repeat and gene annotation strategy only after the sequence set is truly stable

## Default Bias

Be conservative:

- prefer an honest intermediate assembly over a cleaner-looking but biologically misleading one
- do not assume BUSCO duplication automatically means failure
- do not collapse or purge duplicated sequence just because the assembly looks too large

## What To Watch Closely

- multi-peak or hard-to-interpret genome profiles
- duplicated BUSCOs that may reflect real biology
- homeologous alignments that resemble assembly redundancy
- reference-guided placements that oversimplify subgenome structure
- annotation inflation caused by unresolved duplicated sequence

## Likely Deliverable

For many polyploid projects, the best early deliverable is:

- a clearly described assembly representation
- a decision log explaining what was retained, collapsed, or withheld
- strong QC and contamination review
- conservative wording about completeness and chromosome-scale status

## Read Next

- [genome profiling before assembly](../assembly/genome_profiling.md)
- [assembly metrics and interpretation](../qc/assembly_metrics.md)
- [repeat annotation and masking](../annotation/repeats.md)
