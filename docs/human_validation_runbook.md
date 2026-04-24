# Human Validation Runbook

This page turns the v1.0 human validation plan into an executable review process.

## Goal

Use this runbook when you are ready to put real people through the protocol and learn where the workflow, wording, and navigation still need work.

## Recommended Reviewer Mix

Aim for at least one reviewer from each of these groups:

1. beginning bioinformatics graduate student
2. experienced genome-assembly practitioner
3. HPC-comfortable lab member with limited release experience

## Recommended Validation Paths

Assign each reviewer one main path instead of asking them to skim the whole site.

| Reviewer type | Recommended path | Main question |
| --- | --- | --- |
| beginning student | [Project starter kit](project_starter_kit.md) -> [Worked project paths](worked_project_paths.md) -> one packet lane | Can they choose the right path without live coaching? |
| assembly practitioner | [T2T review packet](t2t_review_packet.md) or [Repeat annotation packet](repeat_annotation_packet.md) | Are the decision standards technically defensible and conservative? |
| release submitter | [Release submission packet](release_submission_packet.md) | Can they tell what is final, what is supporting context, and what should be uploaded? |

## Session Format

For each review session:

1. give the reviewer one realistic scenario
2. ask them to start from the docs home page or README
3. record the first page they choose
4. note where they hesitate, backtrack, or misinterpret a decision
5. ask them to summarize the final decision they believe the packet supports

## Minimum Questions To Capture

Record answers to these questions for every session:

- Where did the reviewer start?
- Which page felt most helpful?
- Which page felt too dense or too vague?
- Where did terminology or file naming become confusing?
- Did the packet encourage an unsupported biological or release claim?
- Could they explain the final decision in their own words?

## Tracking Sheet

Record sessions in:

```text
examples/human_validation_sessions.tsv
```

Recommended columns:

| Column | Meaning |
| --- | --- |
| `session_id` | stable review identifier |
| `reviewer_type` | student, practitioner, release_submitter |
| `scenario` | short scenario label |
| `starting_page` | first page opened |
| `path_followed` | main packet or section path |
| `success_level` | completed, partial, blocked |
| `confusion_point` | first major confusion point |
| `main_feedback` | highest-value feedback |
| `overclaim_risk` | yes/no |
| `recommended_fix` | doc improvement to make next |

## Exit Signal For v1.0

The project is getting close to broader `v1.0` readiness when:

- reviewers reliably pick the right entry path
- packet pages feel like complete guided routes rather than scattered notes
- release and annotation handoffs do not depend on tribal knowledge
- reviewers do not leave with inflated confidence about T2T or submission readiness

## Related Pages

- [v1.0 human validation plan](v1_human_validation_plan.md)
- [How to use this protocol in a real project](how_to_use_this_protocol.md)
- [Project starter kit](project_starter_kit.md)
