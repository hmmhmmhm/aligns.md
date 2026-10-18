# Prepare training examples around your team's judgment

ALIGNS.md can help a team turn recurring corrections and agreed decisions into
examples for a coding agent. Option 8 supplies local candidate collection, review
and local dataset export. The workflow below adds a manual handoff and team
review. It is an operating guide, not a hosted submission service or a claim that
a trained model will fit the team without evaluation.

For technical review or an adoption decision, share the [MLOps and team decision
brief](team-mlops-brief.md), also available in [Korean](translated-briefs/ko.md).
It includes the implemented checks, reproducible evidence and remaining validation
work. The [initial readiness audit](training-data-readiness.md) is retained as
the record of the gaps that prompted these changes.

## Set up a small pilot

Choose one repository or workstream and a few decisions worth learning, such as
when to ask for context, how much complexity to introduce, and what a completion
report must verify. Record the team's agreed criteria and their version. Keep
individual preferences separately scoped; a maintainer's personal preference or
a frequently repeated comment is not automatically a team rule.

Before collecting, agree on:

- Participating contributors and the sources each person permits.
- A private submission destination owned by the team, with an authorized reviewer.
- Who can approve a case as representing the team's criteria and who resolves
  disagreements. Leave unresolved cases out instead of using majority frequency
  as a preference label.
- A manual cadence, for example once per sprint, with no required quota.
- Retention, withdrawal, and permission to use the selected code or conversation
  excerpts for the intended training. Permission to store a record is separate
  from permission to send it to a model provider.

Do not create a schedule or start collecting teammates' conversations from this
guide alone. Each person chooses their own sources through option 8. No private
personal ALIGNS.md file needs to be submitted.

## Submit only selected examples

At the agreed checkpoint, the contributor asks their agent to review new candidates
and prepares a batch for the chosen team destination. They check the exact files
before manually submitting them. An empty batch is fine; repeated examples do not
make a better dataset.

Use a directory such as `submissions/<batch-id>/` in the team's selected private
storage. It contains:

| File | Purpose |
| --- | --- |
| `submission.json` | Selected scope, contributor alias, intended use, record IDs and file hashes. Start with the [submission template](templates/team-submission.json). |
| `records.jsonl` | Selected version-2 decision records, including input context, approved targets, correction and verification evidence. |
| `review.json` | Team reviewer decisions, added after review using the [review template](templates/team-review.json). |

In `submission.json`, each `files` entry records a relative file path and its
SHA-256 hash. Keep hashes current after redaction. In `review.json`, copy
`decision_fields` into `decisions` for each record and fill it with the actual
review result; the empty template is not approval.

Keep credentials, customer identifiers, unnecessary personal details and full raw
logs out. Include code or patches only when permitted and needed to understand the
decision. Preserve actual test results and explicit verification gaps. These files
can still contain private team information after review.

Submission is manual. A contributor can copy the batch to approved private storage
or create a PR in a team-selected private data repository. Creating a batch does
not authorize a commit, PR, push, upload, or changing repository visibility. The
ALIGNS.md public repository is not the intake destination.

## Review against team criteria

The reviewer checks each record's provenance, source-use permission, applicable
criterion version and target answer. Record `approved`, `needs_changes` or
`excluded`, with the reason and approval date. Approval of a PR or collection
settings does not stand in for approval of the training target.

Keep the original submission intact. The version-2 review binds its exact bytes
with `submission_sha256` and each original record with `record_sha256`. Provide
an approval reference and an authorized reviewer alias. The team policy lists
allowed reviewers, current criteria snapshots, permitted use, withdrawals and
shared task-family splits. Use the [policy template](templates/team-policy.json).
Never recompute approval hashes to hide edits made after review.

The validated exporter derives namespaced record IDs and applies the reviewer's
shared task family without rewriting originals. Use one family for the same issue,
PR or derived scenario across contributors. A reviewer must explicitly establish
the team scope; personal records are not relabeled automatically.

For DPO, the reviewer must approve the comparison as well as the preferred answer.
Both alternatives need the same available facts and instructions. New requirements
added during a correction make it a different context, not an observed preference
pair. Keep hypothetical and reconstructed examples labeled and opt them in separately.

## Export, then train and evaluate separately

Build an export plan over the approved team scope. Assign whole task families to
training or evaluation before making variants. Review semantic duplicates across
contributors; the exporter detects exact overlap but cannot identify every related
task. The [option-8 procedure](../skills/align/references/training-data.md#export-on-request)
describes the exporter and the supported record shape.

Use the [version-2 contract and commands](../skills/align/references/team-training.md)
for team submissions. The bundled `export_team_dataset.py` checks batch and artifact
hashes, reviewer declarations against the selected policy, approved record hashes,
required context, criterion versions, withdrawals and split assignments. It rejects
contradictory preference cycles and stops before writing on invalid input. It does
not authenticate reviewers or independently execute the submitted tests.

Prefer `sft-completion.jsonl`, which separates input from the selected target.
The export also includes text DPO, held-out evaluation and a private provenance
manifest. Selected tool actions retain schemas/calls/results; code examples need
recorded passing checks and hashed evidence. The legacy text exporter remains for
personal records and must not substitute for team approval validation.

The formats follow [TRL dataset formats](https://huggingface.co/docs/trl/dataset_formats).
Run the bundled local-tokenizer checker, then check the actual training stack's
labels, tool argument schemas and context limits. Tool-action compatibility is
model-specific, and full-run trajectory learning is not implemented.

The team chooses the training model, provider and training run. Compare the same
base coding model with the same ALIGNS.md and tools before and after fine-tuning.
Use held-out tasks to check corrections required, unnecessary clarification,
criterion fit and code/test correctness. Keep independent team review where possible.
Lower correction counts with worse code are not a successful result. Data volume
alone does not show that a model is ready to train or safe to replace the baseline.

Version each exported dataset and keep a private index of included records and
training runs. If a record is withdrawn or a criterion changes, exclude affected
records from later exports and identify older datasets and runs that used them.
Deleting a record does not erase Git history, remote copies or learned weights.

## What is available and what remains

Available now: collection guidance, version-2 templates, validated manual batch
exports, selected-target SFT, text DPO, code evidence checks, selected tool-action
export, output hashes and a local-tokenizer boundary checker.

Before a real pilot, choose contributors, reviewers, scope, private storage,
cadence and a target model. Reviewer authentication, semantic duplicate/conflict
review, isolated code execution, trainer integration, model training and measured
team outcomes remain the team's work. No shared data store is created by installing
the skill.

Suggested request at the manual checkpoint:

> Review my newly collected option-8 candidates for this team's approved scope.
> Prepare a batch with only the examples I have cleared for team training, preserving
> provenance and verification limits. Show me the selected files and exclusions.
> Leave submission to the team destination to me.
