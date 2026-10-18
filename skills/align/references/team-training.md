# Manual team training-data batches

Load this only for authorized team-data setup, batch review or export. Team data
collection is opt-in, with selected contributors, sources, intended use, private
storage and a manual review checkpoint. Installing align enables none of these.
Keep personal criteria separate. The designated team reviewer confirms which
criteria and targets represent the team. Do not resolve disagreements by frequency.

## Capture useful candidates

Prefer a consequential correction or explicitly accepted result. Save the original
request and available context, the actual choice, correction reason, accepted
artifact and verification evidence. Include accepted first attempts as well as
repairs. If the task involves implementation, collect the permitted patch, not only
an answer promising to make one. Reuse existing confirmations; review unresolved
labels in batches rather than interrupting every task.

Use schema version 2 for team records, extending the personal record in
[training data](training-data.md). A team record uses the approved team scope;
never relabel a personal record without explicit team review. The original remains
intact. Candidate creation is not approval.

| Field | Contract |
| --- | --- |
| `kind` | `decision`, `code`, or `tool_action`. |
| `context_reviewed` | True only after checking the model-visible input against the source. |
| `required_context` | Nonempty exact excerpts that must appear in the prompt, including the policy's criterion snapshot. |
| `input_snapshot_sha256` | Canonical digest of `{"prompt": training.prompt, "tools": training.tools or []}`. |
| `training` | Confirmed `prompt` and one selected assistant `chosen`, with optional same-context text `rejected`. |
| `code` | For code targets: `repository`, full `base_commit`, `environment`, `patch`, and `checks`. The chosen text must contain the patch. |
| `code.checks` | Nonempty recorded checks, each with command argument list, integer `exit_code: 0`, timezone timestamp `checked_at`, and hashed `evidence_path`. These are reported results, not independently executed checks. |

Use only information available at the decision point in the prompt. Later review
or test outcomes belong in evidence. When a correction adds requirements, prepare
a new-context SFT candidate rather than claiming an observed preference pair.
A context digest detects later modification; it cannot prove semantic completeness.

A `tool_action` record preserves `training.tools` function schemas, prior visible
calls and results, and one selected assistant action. Call IDs must be unique;
responses reference pending calls. Function arguments are JSON objects, not encoded
strings. The exporter validates message structure, names and call/response linkage;
it does not implement full JSON Schema argument validation. Tool DPO, whole-run
trajectory training, images and hidden reasoning are unsupported. Do not flatten
these into text or invent missing calls.

## Prepare a manual submission

Use the bundled templates in `assets/training-data/`: `team-submission.json`,
`team-review.json`, `team-policy.json`, and `record.json`. The empty templates grant
no permission. Keep the team policy under reviewer control, outside contributor
batches. It defines authorized reviewer aliases, criteria snapshots/versions,
permitted use, selected origins, withdrawn namespaced IDs and task-family splits.

A batch directory contains `submission.json`, `records.jsonl`, permitted evidence
artifacts and `review.json`. The submission lists every selected record in file
order and every input artifact's relative POSIX path and byte SHA-256. No absolute
paths, traversal or symlink files are accepted. The review binds the submission's
exact bytes through `submission_sha256`. Each approved decision binds the complete
original record using `record_sha256`. Editing a submission or record after review
requires a fresh review of the affected content, not merely recomputing hashes to
make validation pass.

Canonical record/input digests use UTF-8 JSON with `sort_keys=True`,
`ensure_ascii=False`, and `separators=(",", ":")`, then SHA-256. File hashes use raw
bytes. The bundled exporter exposes `digest` for canonical values.

The reviewer supplies a human approval reference, target confirmation, timestamp,
reason and shared task-family ID for each approved record. Pair approval is
separate. Check semantic duplicates across submissions before assigning families.
Unreviewed, declined and withdrawn records stay out. A missing or inconsistent
required field stops the export before any files are written. The tool reports
exclusions and dataset counts; repair the batch rather than bypassing validation.

Permission to prepare a batch does not authorize a commit, PR or upload. The user
manually submits selected files to the agreed private destination. Do not use the
public ALIGNS.md repository as intake. A weekly or sprint checkpoint is a team
choice, not an automatically installed scheduler. Empty batches are acceptable.

## Validate and export

Read-only check:

```sh
python3 <skill-dir>/scripts/export_team_dataset.py \
  --batch <selected-batch-directory> --policy <team-policy.json>
```

Add more `--batch` arguments for a reviewed combined export. Add
`--output <new-private-directory>` only when export is authorized. The destination
must not exist. The tool verifies supplied approvals against the selected policy,
file and record hashes, context excerpts/snapshots, code evidence references and
split assignments. It rejects preference cycles under identical input and criteria.
It does not authenticate the person behind an alias, validate the truth of a log,
execute code, detect every semantic conflict, train, or upload.

Prefer `sft-completion.jsonl` with completion-only loss. It preserves earlier turns
as prompt context and puts only the selected answer/action in `completion`.
Legacy `sft.jsonl` includes earlier assistant turns and is retained for text-only
compatibility; do not train it uncritically. `dpo.jsonl` contains confirmed text
pairs; `evaluation.jsonl` holds separate families. `manifest.json` records source
and output hashes, review provenance, exclusions, learning kinds and origins.
It remains private. Different kinds can require separate trainer datasets.

## Check the target stack

With Transformers installed in the user's chosen environment and a locally
available tokenizer, run only on the selected export:

```sh
python3 <skill-dir>/scripts/check_training_adapter.py \
  --dataset <export>/sft-completion.jsonl \
  --tokenizer <local-tokenizer-directory> --max-tokens <chosen-context-budget>
```

This performs no download or training. It rejects unstable prompt/target token
boundaries and overlength rows rather than silently truncating them. It reports
package version, tokenizer hashes and token counts. MLOps must also inspect the
actual trainer's labels/collator, tool argument schemas, loss settings, padding
and model-specific rendering. A tokenizer pass is not a training pass.

Keep an independent final evaluation set if validation guides model selection.
Compare the same base model with the same criteria and tools before and after
training. Check code correctness, corrections, unnecessary questions, task
completion and behavior under changed criteria. Data volume is not a readiness
threshold. Track unique task coverage, approval yield, missing evidence, duplicates
and review time. Keep generated examples and their parent tasks labeled together.
Record withdrawals and changed criteria for later exports; deletion does not undo
past datasets, remote copies or training runs.
