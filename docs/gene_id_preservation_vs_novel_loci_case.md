# Gene ID Preservation vs Novel-Locus Recovery Case

This worked case covers a hard annotation decision that comes up often in crop projects with a strong reference annotation nearby: should the release set prioritize stable inherited IDs, or should it prioritize recovery of novel loci even when that makes the final annotation harder to compare across assemblies and public resources?

## Scenario

A soybean-like crop assembly has a close reference cultivar with a well-used gene naming system. The project generates two realistic release-track candidates:

- a Liftoff-heavy transfer that preserves most inherited gene IDs and structures
- a hybrid set that keeps many transferred models but adds a curated set of RNA-supported novel loci

The transfer-heavy set is easier for downstream users because names remain familiar. The hybrid set is biologically richer, but it introduces new loci, retired loci, and a more complicated provenance story.

## Evidence Snapshot

| Candidate | Preserved reference-like IDs | RNA-supported novel loci retained | Main strength | Main concern |
| --- | --- | --- | --- | --- |
| transfer-heavy | 94.7% | 38 | stable continuity with reference resources | under-recovers cultivar-specific loci |
| hybrid curated | 89.8% | 412 | better recovery of supported novelty | more complex ID and provenance mapping |

## What Makes This Hard

Both choices can be defensible.

The wrong move is pretending that one metric answers the question automatically.

Use this logic:

1. ask whether the project promise is continuity with an existing reference framework, discovery of cultivar-specific biology, or both
2. verify that novel loci are supported by RNA-seq, Iso-Seq, protein evidence, or repeated structural evidence
3. separate truly novel loci from split, duplicated, or TE-inflated artifacts
4. decide whether the release package can carry an identifier crosswalk without confusing downstream users
5. prefer the option that best matches the biological goal and the expected user community

## Recommended Resolution

In this case, the hybrid curated set is still the better release gene set because the project goal includes recovering cultivar-specific biology, and the added loci have real evidence support. However, the release should not casually discard the inherited naming framework.

Recommended release approach:

- keep inherited IDs wherever models remain equivalent
- assign new stable IDs only to supported novel loci
- publish a crosswalk table linking inherited IDs, updated IDs, retired loci, and newly added loci
- explain clearly in methods text that continuity was preserved when biologically justified, but not at the expense of suppressing supported new loci

## Decision-Log Language

```text
The release gene set prioritized supported novel-locus recovery while preserving inherited reference-style IDs for equivalent transferred models. A transfer-heavy candidate retained greater identifier continuity but under-represented cultivar-supported loci, so a curated hybrid set was selected together with an explicit identifier crosswalk to maintain downstream usability.
```

## What To Archive

Archive:

- the transfer-only and hybrid summary tables
- a retained-versus-new loci table
- an identifier crosswalk
- short notes explaining why each new locus was retained

## Reviewer Response Language

```text
We aimed to preserve identifier continuity where transferred models remained biologically equivalent, but we did not treat inherited IDs as more important than supported cultivar-specific loci. The release annotation therefore retains stable inherited IDs for equivalent models while introducing new stable identifiers for supported novel loci, accompanied by a crosswalk table for downstream users.
```
