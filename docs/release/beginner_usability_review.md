# Beginner Usability Review

Use this review before tagging a stable milestone. The reviewer should be able to start from the repository landing page, understand the workflow shape, and find the detailed instructions needed for a crop PacBio HiFi genome assembly without private context from the authors.

## Reviewer Profile

Choose a reviewer who is close to the intended audience:

- beginning bioinformatics graduate student
- new genome assembly analyst
- collaborator familiar with command-line work but not this protocol
- crop genomics researcher who needs to evaluate whether the workflow is review-ready

The reviewer does not need to run a full genome assembly. The goal is to test whether the documentation teaches the workflow and exposes decision logic.

## Review Tasks

Ask the reviewer to start at `README.md` and complete these tasks:

| Task | Expected path | Pass condition |
| --- | --- | --- |
| Find the current version and development status | README, `docs/status.md` | reviewer can state whether the protocol is stable or in development |
| Find how to prepare HiFi reads and screen adapters | README, `docs/assembly/prepare_reads.md` | reviewer can choose between btrim, HiFiAdapterFilt, and PacBio guidance |
| Choose an hifiasm mode for a heterozygous crop | README, `docs/assembly/hifiasm_parameters.md` | reviewer can explain primary, trio, and Hi-C integrated options |
| Identify the core QC figures for a manuscript | README, `docs/qc_figures.md`, `docs/qc/` | reviewer can list metrics, Merqury, BUSCO, contamination, dotplots, and contact maps |
| Decide whether to break a questionable contig | README, `docs/curation/`, `docs/toy_manual_correction_case_study.md` | reviewer can explain evidence needed before editing FASTA |
| Compare scaffolding candidates | README, `docs/scaffolding_worked_decision_case.md` | reviewer can explain why highest N50 is not automatically best |
| Find NCBI submission checks | README, `docs/release/`, helper scripts | reviewer can identify FASTA header, manifest, bundle, and metadata checks |

## Questions for the Reviewer

Use plain answers. Do not coach the reviewer during the test unless they are blocked.

1. Where did you first get lost?
2. Which section felt too long for a first pass?
3. Which decision point needed a stronger example?
4. Which command or file path was hard to adapt to your own project?
5. What would you need before trusting this protocol for a real crop genome release?

## Scoring

| Score | Meaning |
| --- | --- |
| 3 | clear without author help |
| 2 | usable, but reviewer hesitated or needed to reread |
| 1 | unclear, reviewer needed outside explanation |
| 0 | missing or misleading |

Record results in:

```text
examples/beginner_usability_review.tsv
```

## Interpreting Results

- Any score `0` blocks a stable tag.
- Any repeated score `1` should become a documentation issue.
- Scores `2` are acceptable for development milestones but should guide the README-to-docs migration.
- Comments about tool choice, parameter logic, and release decisions are more important than comments about minor wording.

## Release Gate

Before tagging `v0.5.0`, complete at least one beginner usability review and decide whether the findings are:

- fixed immediately
- filed as GitHub issues
- deferred to v0.6 or later with a clear reason

Do not mark the outside-reader pass complete until the response to each finding is recorded.
