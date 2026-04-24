# Release Submission Packet

This page is the simplest ordered path through the release docs for someone who needs to assemble a coherent submission packet without guessing which page comes next. It is written as an internal handoff flow, so a lab member can see what should be frozen, reviewed, exported, and checked before submission.

## Internal Handoff Flow

### 1. Freeze the release object

Confirm which assembly, annotation set, AGP, organelle decision, and metadata package are in scope for this submission. Do not start packaging while these inputs are still drifting.

Read:

1. [NCBI submission path](release/ncbi_submission.md)
2. [Release package decision guide](release_package_decision_guide.md)

Output:

- one declared release package type
- one frozen assembly version
- one declared annotation status: assembly-only, pending, or combined release

### 2. Align identifiers and handoff files

Make sure sequence IDs, annotation IDs, manifest rows, and accession-tracking notes all refer to the same objects.

Read:

1. [Annotation submission handoff](annotation_submission_handoff.md)
2. [Accession handoff worked example](accession_handoff_worked_example.md)
3. [Community database release companion](community_database_release_companion.md)

Output:

- a stable identifier crosswalk
- annotation files that match final FASTA sequence IDs
- accession notes that can be handed to collaborators without translation

### 3. Build and audit the submission bundle

Package the files, then run audits before anyone uploads anything.

Read:

1. [Release bundle worked example](release_bundle_worked_example.md)
2. [Release methods and structured comments](release_methods_and_structured_comments.md)
3. [table2asn and discrepancy triage](table2asn_discrepancy_triage.md)

Output:

- FASTA, AGP, GFF3, manifest, and `.cmt` files that agree
- a discrepancy triage note or clean validation report
- a release bundle that passes internal helper checks

### 4. Prepare the submitter handoff

End with the exact bundle and notes that another person could submit without guessing what is final.

Read:

1. [Release candidate worked case](release_candidate_worked_case.md)
2. [table2asn reviewer-response examples](table2asn_reviewer_response_examples.md)

Output:

- a final handoff folder
- short methods text
- short reviewer-response language for common release questions

## Recommended Packet Order

1. [NCBI submission path](release/ncbi_submission.md)
2. [Release package decision guide](release_package_decision_guide.md)
3. [Annotation submission handoff](annotation_submission_handoff.md)
4. [Accession handoff worked example](accession_handoff_worked_example.md)
5. [Release bundle worked example](release_bundle_worked_example.md)
6. [Release methods and structured comments](release_methods_and_structured_comments.md)
7. [table2asn and discrepancy triage](table2asn_discrepancy_triage.md)
8. [Release candidate worked case](release_candidate_worked_case.md)
9. [Community database release companion](community_database_release_companion.md)

## What This Packet Should Produce

By the end of this sequence, you should have:

- a decision on assembly-only versus combined release
- a stable set of FASTA, AGP, GFF3, and manifest files
- a clean accession-tracking story
- structured comments and methods text that match the actual release objects
- a release bundle that can be audited before submission
- an internal handoff path that another lab member can execute without reverse-engineering your intent

## When To Use This Page

Use this packet when:

- a lab member needs the shortest path to submission readiness
- the release docs feel too spread out
- you want a stable review order for internal signoff

## Related Pages

- [Release](release/index.md)
- [v0.5 human review runbook](release/v0.5_human_review_runbook.md)
- [v0.5 maintainer precheck](release/v0.5_maintainer_precheck.md)
