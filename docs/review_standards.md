# Assembly Review Standards

These standards define practical pass, review, and fail signals for crop plant PacBio HiFi genome assemblies. Thresholds are intentionally conservative and should be interpreted in biological context.

## Review Levels

| Level | Meaning |
| --- | --- |
| Pass | Metric is consistent with a release-quality assembly. |
| Review | Metric may be acceptable but requires explanation or additional evidence. |
| Fail | Metric is not acceptable for release without correction or explicit justification. |

## Core Assembly Metrics

| Metric | Pass | Review | Fail |
| --- | --- | --- | --- |
| Total assembly size | within expected biological range from k-mers/literature | 10-25% from expected | >25% from expected without explanation |
| Number of contigs/scaffolds | appropriate for assembly stage | unusually fragmented for data type | extreme fragmentation relative to read length/coverage |
| Contig/scaffold N50 | comparable to current crop assemblies for species/genome size | lower than expected but biologically usable | too low for intended release or analysis |
| GC content | consistent with related references and reads | modestly shifted | strongly shifted, suggesting contamination or filtering error |

## Completeness and Accuracy

| Metric | Pass | Review | Fail |
| --- | --- | --- | --- |
| BUSCO complete | high for selected lineage | lower than expected for lineage | poor gene-space completeness |
| BUSCO duplicated | low for diploid/inbred primary assembly | elevated but explainable by polyploidy/biology | high duplication suggesting unpurged haplotigs |
| Merqury QV | high enough for intended release | moderate, needs read/error review | low, suggests base accuracy issue |
| Merqury completeness | high | moderate, explain missing k-mers | low, suggests missing assembly content |

## Structural Review

| Evidence | Pass | Review | Fail |
| --- | --- | --- | --- |
| Reference dotplot | mostly collinear, differences explainable | inversions/translocations need support | clear unreviewed chimeras or misjoins |
| Self dotplot | no unexplained whole-genome duplication | possible duplicated haplotigs | strong unpurged duplication in primary assembly |
| Hi-C contact map | clean chromosome blocks | local ambiguity or weak regions | major off-diagonal signals or misjoins |
| Read mapping | even nuclear coverage | outliers documented | unsupported joins or suspect low-coverage contigs |

## Contamination and Organelles

| Metric | Pass | Review | Fail |
| --- | --- | --- | --- |
| FCS-adaptor | no actionable records | records corrected/documented | unresolved adapter/vector records |
| FCS-GX | no actionable foreign contamination | suspect records reviewed | unresolved foreign contamination |
| BlobToolKit/GC/coverage | no unexplained outlier clusters | outliers documented | likely contaminant clusters retained without rationale |
| Organelle screening | free organelle contigs handled intentionally | ambiguous organelle-like sequence reviewed | unreviewed organelle genomes in nuclear release |

## Telomeres, Centromeres, and Gaps

| Metric | Pass | Review | Fail |
| --- | --- | --- | --- |
| Terminal telomeres | consistent with assembly stage | missing telomeres documented | claimed T2T without terminal support |
| Internal telomeres | none or biologically explained | reviewed as possible misjoin | unreviewed internal telomere signal |
| Gaps | expected for scaffolded assembly | gap-rich regions documented | AGP/FASTA gap inconsistencies |

## Annotation Review

| Metric | Pass | Review | Fail |
| --- | --- | --- | --- |
| Repeat masking | species-appropriate repeat fraction | repeat fraction unusual but explained | obvious under/over-masking |
| Gene count | consistent with crop lineage | shifted but explainable | implausible gene count |
| Protein BUSCO | high for lineage | lower than genome BUSCO, explain evidence | poor annotation completeness |
| Functional annotation | acceptable for intended release | incomplete but transparent | missing or misleading functional annotation |

## Release Rule

An assembly can move to public release only when:

- All fail-level items are corrected or explicitly justified.
- All review-level items have written decisions in the assembly decision log.
- FASTA validation passes.
- AGP validation passes when AGP is used.
- Contamination reports are reviewed.
- Tool versions and commands are captured.

