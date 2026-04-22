# 3D-DNA and Juicebox/JBAT Workflow

3D-DNA is a Hi-C scaffolding and misjoin-correction workflow commonly paired with Juicebox Assembly Tools (JBAT) for visual curation. In this protocol, use it as an alternative or complement to YaHS. The key principle is the same: accept only scaffold structures that survive contact-map review, dotplots, and biological sanity checks.

## When to Use 3D-DNA/JBAT

Use this path when:

- the project needs interactive contact-map curation
- YaHS and 3D-DNA disagree and the disagreement needs visual review
- the genome has large repeats, heterozygosity, or chromosome structure that benefits from manual contact-map editing
- collaborators already use Juicebox/JBAT as their review environment

Pause when:

- the input assembly still has obvious contamination, organellar carryover, or haplotig duplication
- the Hi-C library comes from a different genotype or tissue mixture without documentation
- the contact map is too weak or noisy to support joins
- automated correction proposes many breaks that are not supported by independent evidence

## Inputs

Typical inputs:

```text
07_assemblies/sample.primary.fa
10_scaffolding/sample/juicer/aligned/merged_nodups.txt
```

The `merged_nodups.txt` file usually comes from the Juicer Hi-C mapping workflow. Some sites produce equivalent files from Arima or Dovetail workflows; record the exact command path in the methods.

## Template Job

Copy the template:

```bash
cp 01_sbatch_templates/3d_dna_scaffold.sbatch 01_sbatch/
```

Submit:

```bash
sbatch \
  --export assembly=07_assemblies/sample.primary.fa,merged_nodups=10_scaffolding/sample/juicer/aligned/merged_nodups.txt,sample=sample \
  01_sbatch/3d_dna_scaffold.sbatch
```

The first-pass command usually resembles:

```bash
run-asm-pipeline.sh \
  --editor-repeat-coverage 2 \
  07_assemblies/sample.primary.fa \
  10_scaffolding/sample/juicer/aligned/merged_nodups.txt
```

The repeat-coverage setting should be treated as a starting point, not a universal truth. For repetitive crop genomes, compare output against dotplots, read coverage, and Hi-C maps before accepting edits.

## Juicebox/JBAT Review

Open the generated `.hic` and `.assembly` files in Juicebox Assembly Tools. During review:

- inspect every chromosome-scale block from end to end
- look for abrupt contact breaks at proposed joins
- compare strong off-diagonal signals with dotplot evidence
- avoid dragging small repeat-rich contigs into chromosomes without support
- record every manual edit in the scaffolding decision log

Recommended decision columns are in:

```text
docs/scaffolding_decision_log_template.md
```

## After Manual Curation

After saving a reviewed `.assembly` file from JBAT, run the post-review 3D-DNA workflow to produce a curated FASTA and AGP. Exact commands vary by installation, but the common pattern is:

```bash
run-asm-pipeline-post-review.sh \
  --sort-output \
  reviewed.assembly \
  liftover.agp \
  07_assemblies/sample.primary.fa
```

Archive:

```text
*.assembly
*.hic
*.agp
*.fasta
*.cprops
*.asm
*.log
scaffolding_decisions.tsv
```

## Comparison Against YaHS

When both YaHS and 3D-DNA are run:

| Pattern | Interpretation | Action |
| --- | --- | --- |
| same chromosome order/orientation | strong support | accept if contact map is clean |
| same order but different gap sizes | scaffolder convention difference | document AGP and gap sizes |
| local inversion disagreement | possible orientation issue or true structural variation | inspect in JBAT, dotplot, and reference-to-assembly IGV |
| one tool over-places short contigs | repeat-driven placement risk | leave weak contigs unplaced |
| many automated breaks | possible overcorrection | require breakpoint-level evidence before editing FASTA |

## Release Rule

Do not treat JBAT dragging as evidence by itself. The evidence is the combination of contact-map improvement, scaffold consistency, dotplots, gap/AGP validation, and documented review decisions.

## References

- 3D-DNA GitHub: https://github.com/aidenlab/3d-dna
- Juicebox GitHub: https://github.com/aidenlab/Juicebox
- Juicebox Assembly Tools documentation: https://github.com/aidenlab/Juicebox/wiki/Juicebox-Assembly-Tools
