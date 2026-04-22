# Correction Report Examples

Use these examples as starting language for manuscript methods, release reports, and reviewer responses. Replace all bracketed fields with project-specific details.

## Manuscript Methods: No Manual Corrections

Structural consistency was evaluated using whole-genome alignments between the assembly and [reference genome/version], supported by [Hi-C/read-depth/k-mer] evidence. Candidate discordances were reviewed in dotplots and cross-checked against independent evidence. No candidate correction met the project evidence threshold for manual editing, so the submitted assembly FASTA is the direct [assembler/scaffolder] output after filtering and naming.

## Manuscript Methods: Manual Break Accepted

Candidate misassemblies were screened using [MUMmer/minimap2/RagTag] comparisons against [reference genome/version]. A putative chimera on [sequence ID] was supported by [primary evidence] and [secondary evidence]. The sequence was split after base [coordinate] using a documented 1-based breakpoint convention. Downstream AGP, FASTA index, repeat annotation, gene annotation, and release validation files were regenerated after the edit.

## Manuscript Methods: RagTag Used as Comparison Only

RagTag correction and scaffolding were run against [reference genome/version] as a reference-guided comparison. Proposed changes were not accepted automatically. Each candidate break, orientation change, or scaffold placement was evaluated against dotplots, [Hi-C/read-depth/k-mer] evidence, and known crop structural variation. The final assembly retained [accepted/rejected summary] relative to the RagTag proposal.

## Reviewer Response: Why a Discordance Was Retained

We agree that [region] appears discordant relative to [reference]. We reviewed this region using [dotplot], [Hi-C/read-depth/k-mer evidence], and [alternate reference or related assembly]. The independent evidence supports the submitted structure, while the discordance is consistent with [cultivar-specific inversion/introgression/reference gap/known structural variation]. We therefore retained the sequence and added the evidence to the correction decision log.

## Reviewer Response: Why a Contig Was Broken

We re-examined [sequence ID] after the reviewer comment. The region showed [dotplot pattern] and was independently supported by [Hi-C/read-depth/read alignment] evidence at the same coordinate. We split the sequence after base [coordinate], regenerated downstream release files, and added before/after dotplots and the correction decision entry to the repository.

## Release Report: Correction Entry

```text
edit_id: edit_0001
sequence_id: chr03
action: break
coordinate: break_after_1based=14500001
primary_evidence: Hi-C contact map break
secondary_evidence: HiFi read alignments stop at same position
accepted: yes
downstream_regenerated: FASTA index, AGP, repeats, genes, release manifest, NCBI validation
```

## Tone Guidance

Be precise and conservative. Avoid saying that a reference-guided change is correct only because it matches the reference. Say what evidence supports the edit, what alternatives were considered, and which downstream files were regenerated.
