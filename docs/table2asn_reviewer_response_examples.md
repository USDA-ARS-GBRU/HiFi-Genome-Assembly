# table2asn Reviewer-Response Examples

Use this page when annotation-validation issues show up during manuscript review, internal release review, or a submission handoff.

The point is to answer clearly without pretending every warning category is either trivial or fatal. Good responses explain:

- what the issue was
- whether it reflected a structural problem or a naming problem
- what was fixed
- what was retained intentionally and why

## Principles

Keep the response short and evidence-based.

Good response pattern:

1. name the issue class
2. say whether it was corrected
3. say what evidence or rule guided the correction
4. say what the final release package now contains

## Example 1: FASTA/GFF3 identifier mismatch

Reviewer concern:

> The annotation package appears to contain features on sequence identifiers not present in the submitted assembly.

Strong response:

> We confirmed that an earlier annotation draft still referenced pre-freeze sequence identifiers. We regenerated the annotation package against the frozen release FASTA, reran local FASTA/GFF3 ID audits and `table2asn`, and replaced the earlier package with the corrected identifier set.

## Example 2: Missing locus tags

Reviewer concern:

> Several gene models appear to lack locus tags required for public annotation release.

Strong response:

> We standardized locus-tag handling across the release gene set and regenerated the submission package using a single locus-tag strategy. The final annotation package now applies consistent locus tags across all released gene models.

## Example 3: Genes crossing gaps

Reviewer concern:

> Some genes may span unresolved gaps in the assembly.

Strong response:

> We reviewed candidate models overlapping assembly gaps and treated gap-spanning features as structural issues rather than naming issues. Models that could not be supported across unresolved gaps were split, trimmed, marked partial where appropriate, or removed from the release gene set before final packaging.

## Example 4: Internal stop codons

Reviewer concern:

> The annotation validation report contains CDS models with internal stop codons.

Strong response:

> We inspected all flagged CDS models against the frozen genomic sequence and annotation evidence. Unsupported or broken models were corrected or excluded from the release gene set. Models retained after review were documented as biologically plausible edge cases rather than ignored validator output.

## Example 5: Informal or overly specific product names

Reviewer concern:

> Product descriptions appear informal or inconsistent with public database conventions.

Strong response:

> We revised functional descriptions to use conservative, database-friendly product names and removed unsupported specificity. Where confident naming was not justified, we used more general annotation language rather than overstate function.

## Example 6: Why annotation was not submitted with the first assembly release

Reviewer concern:

> Why was the assembly released without the annotation package?

Strong response:

> We separated the first public assembly release from the annotation release candidate because annotation discrepancy review had not yet completed against the frozen identifiers. The assembly package itself was ready for release, and we prioritized a coherent first public assembly object over simultaneous release of an annotation package still in cleanup.

## Example 7: Warnings retained with rationale

Reviewer concern:

> Some warning categories remain in the validation outputs.

Strong response:

> Remaining warnings were reviewed individually after structural inconsistencies, locus-tag issues, and gap-related problems had been resolved. The residual warning categories reflected biological edge cases rather than package inconsistency, and they were documented in the release notes and internal handoff materials.

## Phrases To Avoid

- "The warnings were ignored."
- "table2asn is overly strict."
- "These are probably fine."
- "We left them because the submission portal accepted the files."

## Safer Replacements

- "reviewed and documented"
- "retained with rationale"
- "resolved before final packaging"
- "not part of the released annotation set"

## Related Files

- `docs/table2asn_discrepancy_triage.md`
- `docs/annotation_submission_handoff.md`
- `docs/release_candidate_worked_case.md`
- `examples/annotation_validation/expected_table2asn_review.md`
