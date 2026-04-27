# Release Methods and Structured Comments

Use this page when you need release-ready wording for manuscripts, NCBI metadata entry, and optional GenBank structured comments.

The goal is consistency. The assembly method, coverage, sequencing technology, and release object names should match across:

- manuscript methods
- BioProject or submission notes
- release manifest
- accession tracking table
- Genome Submission Portal metadata
- optional `.cmt` structured comment files used with `table2asn`

## Official Guidance Checked During Drafting

- NCBI genome submission portal requests assembly method, assembly method version or date, genome coverage, and sequencing technology metadata: [About Genome (WGS) Submission](https://submit.ncbi.nlm.nih.gov/about/genome/)
- NCBI structured comment guidance documents a `Genome-Assembly-Data` structured comment with required fields for assembly method, genome coverage, and sequencing technology, and notes that the portal may prompt for this information directly: [Adding a Structured Comment to GenBank Submissions](https://www.ncbi.nlm.nih.gov/genbank/structuredcomment/)

Inference from those sources: for this protocol, structured comments should be treated as an optional reproducibility aid when building `.sqn` packages locally, not as a substitute for accurate portal metadata.

## Minimal Assembly Methods Template

Use short, factual wording:

```text
High-molecular-weight DNA was extracted from young leaf tissue of <cultivar/accession>. PacBio HiFi reads were generated on the <instrument> platform to approximately <coverage>x genome coverage. A de novo assembly was generated with hifiasm v. <version>. Optional scaffolding used <tool and version>. Contamination screening included <tools>. Assembly quality was assessed with <metrics>. Repeat masking used <tool>. Gene annotation used <tool(s)> with <evidence>. The final release object was submitted as <assembly-only or annotated genome>.
```

## Published-Method Crop Template

Use this when the project follows the current recommended crop lane:

```text
PacBio HiFi reads were assembled de novo with hifiasm v. <version>. Assembly candidates were evaluated using contiguity statistics, BUSCO <lineage/version>, Merqury k-mer QV/completeness, <LAI/LTR_retriever if used>, read-mapping or Inspector evidence where applicable, whole-genome dotplots, and contamination/organelle screening with <tools>. Chromosome-scale scaffolding was performed with <YaHS/3D-DNA/RagTag/other> v. <version> using <Hi-C/Omni-C/reference/map evidence>, followed by contact-map and AGP review. Repeats were annotated with <EDTA/RepeatModeler2/RepeatMasker/curated library>, and gene annotation used <Liftoff/BRAKER3/MAKER/hybrid> with <RNA-seq/Iso-Seq/protein/reference> evidence.
```

## T2T Escalation Template

Use this only when the project actually included the extra evidence:

```text
Candidate T2T regions were evaluated separately from ordinary chromosome-scale scaffolding. Evidence included <PacBio HiFi>, <ultra-long ONT>, <Hi-C/Omni-C>, <optical map/FISH/genetic map if used>, terminal telomere motif searches, centromere candidate annotation, difficult-repeat review, gap-status summaries, and spanning-read validation. We use <chromosome-scale/near-gapless/candidate T2T/T2T-quality> language according to the per-chromosome evidence table.
```

## Minimal Reviewer-Response Template

```text
The public release package was prepared from the frozen assembly version <assembly_version>. Sequence identifiers, AGP, annotation inputs, and metadata were checked for consistency before submission. Because <reason if relevant>, the first public release was submitted as <assembly-only or annotated genome>, while other package variants were retained as comparison candidates.
```

## Genome-Assembly-Data Structured Comment Example

NCBI's structured comment page says the genome structured comment uses `StructuredCommentPrefix` and `StructuredCommentSuffix` values for `Genome-Assembly-Data`.

Example tab-delimited `.cmt` content:

```text
StructuredCommentPrefix	Genome-Assembly-Data
Assembly Method	hifiasm v. 0.25.0; YaHS v. 1.2a
Genome Coverage	38x PacBio HiFi
Sequencing Technology	PacBio Revio HiFi; Hi-C
Assembly Name	maize_line_a_v1
StructuredCommentSuffix	Genome-Assembly-Data
```

For local `table2asn` workflows, this can be saved as a `.cmt` file and supplied alongside the FASTA or with the `-w` argument.

## Example Release Notes Fields

Record these values in one place before submission:

- assembly name
- assembly method and version/date
- scaffolding method and version/date
- estimated genome coverage
- sequencing technologies used
- alternate assembly candidates compared, if any
- QC metrics and database versions, including BUSCO lineage, Merqury k-mer size, LAI method, and contamination databases
- contamination-screening summary
- repeat-masking method
- annotation method and evidence
- release object type

## Phrases To Avoid

- "chromosome-level" if the released object is still unplaced or unresolved without that caveat
- "complete" if internal gaps or unresolved joins remain
- "submitted with annotation" if the first public package was assembly-only
- "final" when the actual release is explicitly a draft candidate

## Safer Replacements

- "chromosome-scale assembly"
- "first public assembly release"
- "annotated release candidate"
- "assembly package submitted; annotation package retained for later submission"

## Related Files

- `docs/v0.9_ncbi_release_kickoff.md`
- `docs/release_package_decision_guide.md`
- `docs/annotation_submission_handoff.md`
- `docs/ncbi_metadata_templates.md`
- `docs/methods_text_template.md`
- `examples/accession_tracking.tsv`
