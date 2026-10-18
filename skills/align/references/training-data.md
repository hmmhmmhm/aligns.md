# Optional personal training data

Use for path 8 or an explicit request to collect, review, stop collecting, remove,
or export personal training examples. Preparing data does not train a model or
demonstrate a performance gain. ALIGNS.md already affects inference when read;
this path prepares material for later user-run fine-tuning.

For selected team submissions, load [team training data](team-training.md). Use its
version-2 records and validated batch exporter rather than treating personal
confirmation flags as team approval.

## Agree on collection once

Reuse settings and authorization already given. Otherwise establish:

- Scope: this project, selected personal criteria, or both with separate labels.
- Sources: current conversation from now on, or specifically selected history.
  For historical review, follow [history review](history.md), including scope and
  estimated time. Existing access to logs is not permission to collect them.
- Storage: suggest a local directory outside repositories, such as
  `~/.local/share/aligns/datasets/<user-chosen-name>/`. Offer a project directory
  or a separate repository only when wanted. Choose Git tracking, commits and
  remote uploads separately; inspect visibility before an authorized upload.
- Mode: record candidates during authorized active work, or extract only on
  request. Choose a review checkpoint, such as a requested alignment session or
  a configurable number of new candidates. Twenty candidates can be a review
  reminder, never a training-readiness threshold. No scheduler is implied.

Show the concrete settings before saving if not already authorized. Save them as
`collection.json` in the selected directory, with schema version 1, enabled state,
scope, selected sources, collection start, mode, review checkpoint, and Git/upload
policy. Save exact source selectors, not credentials or the whole conversation.
Restrict local dataset files to the user where the platform supports it. If a
project folder is chosen without Git tracking, check ignore behavior and whether
files are already tracked; an ignore rule does not untrack existing content.
Do not create files merely because the option was displayed. Developing the skill
does not opt the developer into data collection.

For future active turns, connect the chosen settings through the appropriate
private user instruction or project instruction only within the selected scope.
The pointer should say: read these settings, collect only while enabled and within
their sources/scope, and load this reference for capture or review. Keep private
paths and settings out of shared instructions. If no private connection is usable,
offer request-only mode rather than exposing a path or promising automatic capture.
No daemon, universal session monitor, or access to unavailable logs is provided.

## Capture small decision records

Record candidates when a user corrects a consequential judgment, confirms a
criterion, chooses in a hypothetical rehearsal, or accepts a verified result.
Keep only the request, context, visible response, correction, accepted resolution,
and evidence needed to understand that decision. Store candidates in
`records.jsonl`, one JSON object per line, using unique IDs. Do not dump transcripts,
infer approval from silence or a merged PR, or collect hidden reasoning.

Preserve scope, criterion version, source references and timestamps. Distinguish
observed decisions, hypothetical choices, and reconstructed examples. A generated
alternative has no human preference label until the user actually compares it.
Repeated scoped choices can support taste-invariant candidates, not automatic
promotion to a global preference. Agreement on a criterion is not acceptance of
an invented ideal answer. Record missing targets as null and keep the candidate.

Use this record shape (values below are field descriptions, not training data):

| Field | Content |
| --- | --- |
| `schema_version`, `id`, `group_id` | Version 1, unique example ID, task/session family ID shared by related examples and derivatives. |
| `recorded_at`, `scope`, `criteria_version` | ISO timestamp with zone, scoped identifier, version of the relevant criteria. |
| `source_refs`, `origin` | Minimal source locators; `observed`, `hypothetical`, or `reconstructed`. |
| `context`, `response`, `correction`, `accepted_response` | Relevant evidence; absent values remain null. |
| `confirmation`, `verification` | User confirmation evidence separately from actual execution checks and unverified limits. |
| `status`, `privacy_reviewed` | `candidate`, `reviewed`, `excluded`, or `superseded`; review of secrets and unnecessary personal data. |
| `training` | Optional normalized text messages: `prompt`, `chosen`, optional `rejected`; booleans `target_confirmed`, `pair_confirmed`, `same_context`. |

The `training` object is a reviewed derivative of the evidence, not a place to
invent missing responses. `target_confirmed` requires evidence for acceptance of
that target, not just approval of collection. `pair_confirmed` requires a user
preference between those alternatives under the same context. Record the evidence
in `confirmation`; do not mark examples accepted by model judgment alone.

Keep relevant code, patches and check results when the example depends on code.
Version-1 records handle text decisions. Version-2 team records also support
code evidence and selected tool actions; follow the team reference for their
requirements. Preserve unsupported trajectories separately rather than flattening
them into fake text exchanges.

## Review before export

At the chosen checkpoint, offer a batch review with counts and short examples.
Reuse existing confirmations; ask only about unresolved labels or scope. Do not
interrupt every task or repeatedly prompt after a declined checkpoint. Track the
last reviewed IDs in collection settings so the same batch is not offered again.

Exclude duplicates, irrelevant personal details, secrets, unsupported labels and
examples that conflict with current criteria. Changed criteria make affected
examples ineligible until reviewed; keep `superseded` separate from deletion.
Tell the user what was excluded and why. Collection permission is not permission
to export or upload. Stop collecting when disabled; deletion applies only to
selected files, not automatically to Git history, remote copies or trained weights.

For DPO, both alternatives must answer the same prompt with the same available
facts and instructions. A correction that adds facts or changes the task is not
such a pair. Keep an unpaired record instead. Never synthesize a rejected answer
and describe it as an observed rejection. Hypothetical and reconstructed examples
remain labeled and require explicit inclusion in an export.

Assign whole task/session families to train or evaluation before creating variants.
Related examples and derivatives must share a `group_id`. Review semantic overlap
across groups too; exact-match checks cannot detect paraphrases. Keep evaluation
examples out of every training file. Compare base + ALIGNS.md against fine-tuned +
the same ALIGNS.md on held-out tasks before claiming a benefit.

## Export on request

Prepare a local `export-plan.json` with `schema_version: 1`, `current_criteria`
(scope to approved criterion-version map), `groups` (group ID to `train` or `eval`),
and `include_origins` (default `["observed"]`). Inspect all selected scope mappings
and origins with the user, reusing explicit authorization. For example, a fictional
plan might map `project:sample` to `v2` and `sample-task-1` to `eval`.

Run the bundled exporter only for the authorized files and destination:

```sh
python3 <skill-dir>/scripts/export_training_data.py \
  --records <dataset-dir>/records.jsonl \
  --plan <dataset-dir>/export-plan.json \
  --output <new-local-export-directory>
```

It creates `sft-completion.jsonl` (`prompt`, `completion`), legacy text-only
`sft.jsonl` (`messages`), `dpo.jsonl`
(`prompt`, `chosen`, `rejected`), `evaluation.jsonl`, and `manifest.json`.
The manifest retains example IDs, source references, scope, origin and exclusion
reasons outside the trainer files. It is private data too. The exporter refuses
an existing destination, duplicate IDs, missing split assignments for eligible
examples, and exact prompt overlap between train and evaluation. It filters
unreviewed, unconfirmed, stale or privacy-unreviewed records and duplicate
prompt/target examples. It does not verify
the truth of labels, strip secrets for you, or establish enough data for training.

Prefer `sft-completion.jsonl` with completion-only loss so earlier rejected
assistant turns remain context rather than training targets. Check actual token
masks and length limits on the selected model. The exporter also rejects invalid
timezone timestamps and preference cycles for identical contexts and criteria.

Check the counts and samples, report unsupported/omitted examples, and note an
empty train or evaluation set. No fixed count proves readiness. User-selected
training tools may require a different chat template or format adapter. The text
formats follow [TRL dataset formats](https://huggingface.co/docs/trl/dataset_formats).
Training, evaluation execution, Git commits and uploads are separate actions.
ALIGNS.md remains the current agreement; these optional records are not its diary.
