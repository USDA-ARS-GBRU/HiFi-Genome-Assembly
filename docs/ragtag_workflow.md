# RagTag Correction and Scaffolding Comparison

RagTag is useful for comparing an assembly against a close reference, testing homology-based correction, and building a reference-guided scaffold proposal. It should be treated as a review aid, not as a substitute for biological judgment.

## What RagTag Does

RagTag provides tools for assembly correction, scaffolding, patching, merging, and format utilities. The two commands most relevant here are:

- `ragtag.py correct <reference.fa> <query.fa>`: identifies putative misassemblies in the query assembly using homology to the reference and breaks query sequences at candidate misassembly points.
- `ragtag.py scaffold <reference.fa> <query.fa>`: orders and orients query sequences by comparison to the reference and joins them with gaps; it does not alter the input query sequences themselves.

## When to Use It

Good use cases:

- a close, high-quality reference exists
- a dotplot suggests a possible chimera or orientation issue
- a draft contig assembly needs a reference-guided scaffold comparison
- Hi-C data are unavailable, low quality, or being used as an independent check

Poor use cases:

- the reference is distant or structurally divergent
- the crop lineage has known inversions, introgressions, or pan-genome presence/absence variation
- the goal is to force a new assembly to match an older reference
- contamination or haplotig duplication has not been reviewed yet

## Template Job

Copy templates into a project `01_sbatch/` directory:

```bash
cp 01_sbatch_templates/ragtag_correct_scaffold.sbatch 01_sbatch/
```

Run correction only:

```bash
sbatch \
  --export reference=references/close_reference.fa,query=07_assemblies/sample.primary.fa,sample=sample,mode=correct \
  01_sbatch/ragtag_correct_scaffold.sbatch
```

Run scaffolding only:

```bash
sbatch \
  --export reference=references/close_reference.fa,query=07_assemblies/sample.primary.fa,sample=sample,mode=scaffold \
  01_sbatch/ragtag_correct_scaffold.sbatch
```

Run correction followed by scaffolding:

```bash
sbatch \
  --export reference=references/close_reference.fa,query=07_assemblies/sample.primary.fa,sample=sample,mode=both \
  01_sbatch/ragtag_correct_scaffold.sbatch
```

## Compare Outputs

Review:

- RagTag corrected FASTA
- RagTag scaffold FASTA
- AGP files
- confidence scores and logs
- whole-genome dotplots before and after
- Hi-C contact map if available
- read depth around proposed breaks
- BUSCO/Merqury/contiguity changes

Do not automatically accept the most contiguous result. A reference-guided scaffold can look tidy while hiding real cultivar-specific structure.

## Decision Table

| Observation | Interpretation | Recommended action |
| --- | --- | --- |
| RagTag proposes a break that matches Hi-C and read-depth evidence | Likely misassembly | Consider breaking and document evidence |
| RagTag proposes a break but HiFi reads and Hi-C support the original assembly | Possible reference disagreement | Retain original assembly |
| RagTag scaffolds small contigs onto chromosome ends | May improve placement | Accept only if evidence supports orientation and placement |
| RagTag forces many contigs to a distant reference order | Reference bias risk | Use as comparison only |
| RagTag output improves N50 but worsens BUSCO or Merqury patterns | Possible overcorrection | Investigate before release |

## Release Rule

If RagTag changes are accepted, treat the output as a new assembly version. Regenerate FASTA index, AGP, dotplots, repeat annotation, gene annotation, release manifest, and NCBI validation products as needed.
