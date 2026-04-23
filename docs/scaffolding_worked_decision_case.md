# Worked Scaffolding Decision Case

This worked example shows how to move from candidate scaffolding metrics to a final assembly decision. It is intentionally small and generic, but the logic should match a real crop genome review.

## Scenario

A diploid crop accession was assembled from PacBio HiFi reads. Primary contigs were polished enough for scaffolding and no high-confidence contamination remained after screening. The project generated four candidate assemblies:

- `contig`: unscaffolded hifiasm primary contigs
- `yahs`: Hi-C scaffolding with YaHS
- `3d_dna`: Hi-C scaffolding with 3D-DNA followed by JBAT review
- `ragtag`: reference-guided scaffolding against a close cultivar

The crop has 12 expected chromosomes. A related cultivar reference exists, but known inversions and presence/absence variation are expected between cultivars.

## Candidate Metrics

Example candidate metrics are in:

```text
examples/scaffolding_decision_case/candidate_metrics.tsv
```

The summary table looks tempting at first:

| Candidate | Sequences | N50 bp | Gap count | Gap bp | First impression |
| --- | ---: | ---: | ---: | ---: | --- |
| contig | 188 | 35400000 | 0 | 0 | good contiguity before scaffolding |
| yahs | 24 | 74200000 | 14 | 1400 | chromosome-scale candidate |
| 3d_dna | 21 | 78100000 | 17 | 1700 | slightly higher N50 |
| ragtag | 12 | 91300000 | 36 | 3600 | highest N50, but reference-guided |

Do not choose `ragtag` just because it has 12 scaffolds and the highest N50. For crops, a close reference can still impose the wrong order or orientation across real structural variation.

## Evidence Review

Review the candidates with the same evidence categories used in the main workflow.

| Evidence | `yahs` | `3d_dna` | `ragtag` | Interpretation |
| --- | --- | --- | --- | --- |
| Hi-C contact map | 12 strong chromosome diagonals plus 12 weakly supported unplaced contigs | one checkerboard pattern on chr05 and one weak long-range join on chr09 | several joins lack Hi-C support | `yahs` has the cleanest contact-map evidence |
| Dotplot to related cultivar | mostly collinear; chr07 shows cultivar-specific inversion retained as assembly structure | similar, but chr05 breakpoint aligns with contact-map concern | perfect reference order, including chr07 inversion flattened to reference | `ragtag` may be hiding biological variation |
| HiFi read mapping | even depth across YaHS joins | local depth dip near chr09 join | no read support problem, but some joins are not supported by Hi-C | no candidate has a simple read-depth failure |
| AGP validation | passes | passes | passes | format validity does not prove biological correctness |
| Telomere signal | 9 of 12 scaffolds have telomere motif on at least one end | 9 of 12 | 10 of 12 | useful, but not decisive |
| Contamination screen | no flagged scaffold joins | no flagged scaffold joins | no flagged scaffold joins | no candidate rejected for contamination |

## Decision

Select the `yahs` candidate as the release-track assembly, with 12 chromosome-scale scaffolds and 12 unplaced contigs. Reject the unsupported RagTag placements even though they improve the apparent chromosome count and N50. Reject the unedited 3D-DNA candidate because the contact map contains two unresolved concerns.

Final actions:

- Accept YaHS chromosome scaffolds with strong contact-map diagonals.
- Leave 12 weakly supported contigs unplaced rather than forcing them into chromosomes.
- Retain the chr07 inversion because Hi-C, dotplot, and local read evidence support the assembly structure.
- Archive RagTag and 3D-DNA outputs as comparison evidence, not final release assemblies.
- Regenerate final FASTA index, AGP, assembly stats, gap summary, contact-map screenshots, and release bundle checks from the selected YaHS candidate.

Example decision log rows are in:

```text
examples/scaffolding_decision_case/scaffolding_decision_log.tsv
```

## Reviewer-Ready Methods Text

```text
Chromosome-scale scaffolding candidates were generated with YaHS, 3D-DNA/JBAT, and RagTag. Candidate selection was based on Hi-C contact-map support, AGP validity, whole-genome alignments, local HiFi read mapping, telomere signal, and contamination review rather than continuity statistics alone. The final release-track assembly used the YaHS scaffold set because it preserved 12 strong chromosome-scale Hi-C diagonals and avoided unsupported reference-guided joins. Twelve contigs with weak or ambiguous placement support were retained as unplaced scaffolds. A cultivar-specific chr07 structural difference was retained because it was supported by Hi-C signal, dotplot evidence, and local read mapping.
```

## Reviewer Response Example

```text
We agree that the RagTag candidate produced the highest scaffold N50 and matched the expected chromosome count. However, several RagTag joins were not supported by the Hi-C contact map, and one reference-guided orientation would have collapsed a structural difference supported by the sample's Hi-C and HiFi read evidence. We therefore selected the YaHS candidate, which had slightly lower continuity statistics but stronger independent support. The rejected RagTag and 3D-DNA candidates are retained in the project decision log and were used as comparison evidence.
```

## Teaching Notes

- A valid AGP and high N50 are necessary checks, not final proof.
- For crop genomes, reference-guided scaffolding can be useful and still wrong.
- Unplaced contigs are not failure by default. They are often better than unsupported chromosome joins.
- The best release assembly is the one with the most coherent evidence, not the most compressed statistics.
