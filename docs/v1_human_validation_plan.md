# v1.0 Human Validation Plan

This page outlines the broader human validation layer planned before a `v1.0` release.

## Goal

The goal is not only to prove that the docs are internally consistent. The goal is to learn whether real users can move through the protocol with the right level of confidence and restraint.

For the operational version of this plan, use the [human validation runbook](human_validation_runbook.md).

## Validation Groups

Plan to gather feedback from at least three perspectives:

1. a beginning bioinformatics graduate student
2. an experienced genome-assembly practitioner
3. a lab member who is comfortable on HPC but not deeply familiar with crop genome release workflows

## Suggested Validation Tasks

Each reviewer should be asked to complete a realistic path, not just skim pages.

Suggested tasks:

- start a new project using the [project starter kit](project_starter_kit.md)
- choose a worked path and explain why it fits the biological scenario
- follow the release packet far enough to explain what files must be frozen before NCBI submission
- identify one place where the docs feel too dense, too vague, or too optimistic

## Minimum Questions To Capture

Record:

- what page they started on
- where they became unsure
- whether the uncertainty was navigation, terminology, or biological judgment
- whether the examples felt realistic
- whether the workflow encouraged overly strong claims

## Success Criteria For v1.0

The protocol is closer to `v1.0` when:

- reviewers can choose a correct entry path without live coaching
- worked examples feel representative of real crop projects
- release and annotation paths are understandable without hidden tribal knowledge
- no major section encourages overclaiming completeness or submission readiness

## Where To Record Feedback

Use or extend:

- `examples/beginner_usability_review.tsv`
- `examples/human_validation_sessions.tsv`
- issue templates in `.github/ISSUE_TEMPLATE/`
- section-specific docs updates in the relevant lane

## Related Pages

- [How to use this protocol in a real project](how_to_use_this_protocol.md)
- [Project starter kit](project_starter_kit.md)
- [Active draft lanes](active_draft_lanes.md)
- [Human validation runbook](human_validation_runbook.md)
