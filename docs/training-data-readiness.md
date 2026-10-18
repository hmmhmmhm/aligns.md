# Training-data readiness for MLOps teams

Historical pre-0.11 audit. See the [current implementation and evidence](team-mlops-brief.md).
The findings below describe the original version and are retained unchanged.

Reviewed on 2026-10-18 against the exporter in commit `c80929d`. This is a
source audit and an offline fixture check. No team dataset, trainer execution,
model training, or independent MLOps review was available.

ALIGNS.md can supply supervision about a team's decisions: which changes reviewers
accept, when they expect clarification, and what evidence makes work complete.
The current exporter prepares text examples that an MLOps team can adapt for SFT
or preference training. It is not yet a validated intake pipeline for training a
coding agent from submitted batches.

## Current compatibility

| Use | Current support | Additional checks |
| --- | --- | --- |
| Text decision SFT | Conversational `messages` in `sft.jsonl`. | Context, target labels, chat template, loss masking and token limits. |
| Text preference training | Explicit `prompt`, `chosen`, `rejected` in `dpo.jsonl`. | Same-context comparison, conflicts and label provenance. |
| Code or patch SFT | Text may contain code or a patch. | Base revision, dependencies, patch applicability and test results are not enforced. |
| Tool-using trajectories | Rejected by this exporter. | Separate adapter for tool schemas, calls, responses and selected assistant actions. |
| Evaluation | Held-out prompt/expected-response records. | Executable evaluator, team rubric and independent tasks. |
| Team submissions | Manual guide and templates. | Intake validation and enforcement of team approval. |

The SFT and DPO structures match documented TRL formats. This establishes format
correspondence, not a successful load or training run on a particular model. TRL
uses model-specific chat formatting; tool-call datasets also retain tool messages
and schemas. See the official [SFT guide](https://huggingface.co/docs/trl/sft_trainer)
and [DPO guide](https://huggingface.co/docs/trl/dpo_trainer).

## Reproduced findings

From the repository root:

```sh
python3 tests/audits/training_readiness.py
python3 -m unittest discover -s tests -p test_training_data.py
```

The [saved observations](../tests/audits/training-readiness-2026-10-18.json)
include exporter and probe hashes. All fixture content is invented, including
reviewer evidence. Their `observed` flags exercise an export path, not real human
feedback. The 13 existing tests passed. The ten audit cases describe behavior;
they are not ten successful readiness checks.

| Finding | Observed behavior | Consequence |
| --- | --- | --- |
| Context only in evidence | A constraint in `context` was absent from trainer rows. | Review that `training.prompt` includes the relevant information available at decision time. |
| Bad assistant history | The earlier bad answer remained in SFT `messages`, without an explicit target mask. | Training may learn the unwanted answer along with its correction. |
| Contradictory preference pairs | Both A-over-B and B-over-A exported for the same prompt and criterion version. | Resolve contradictory comparisons. Multiple acceptable SFT answers alone need not conflict. |
| Free-text evidence | An unverified example and an invalid timestamp exported. | Current validation cannot establish code correctness or reliable chronology. |
| Team review is external | Export succeeded without submission or reviewer files. | Record flags do not prove an authorized team review occurred. |
| Semantic overlap | A related prompt assigned another family entered evaluation. | Exact overlap checks do not replace cross-batch lineage and duplicate review. |
| Existing boundaries | Tool calls and exact prompt overlap across splits were rejected; candidates were excluded. | Retain these controls when adding adapters and intake checks. |

TRL's conversational language-modeling format can train on the full sequence.
Even assistant-only loss can include a bad earlier assistant turn. For a selected
target, prefer a prompt/completion derivative with completion-only loss and inspect
the actual token labels. This recommendation follows
[TRL's loss configuration](https://huggingface.co/docs/trl/sft_trainer#train-on-completion-only);
it was not tested in a trainer here.

## What makes an example useful

Preserve the task as the agent saw it, the choice made, what the reviewer corrected,
and the final answer or artifact accepted. Keep acceptance separate from test
evidence: a preferred implementation can still fail a test.

Prioritize consequential decisions that recur in the team's work:

- A reviewer narrows an overbuilt change and accepts a smaller patch.
- The agent asks for a missing requirement at the right time, or asks an
  unnecessary question despite having enough information.
- A patch passes functional checks but violates a confirmed team constraint;
  the corrected patch satisfies both.
- A reviewer corrects a completion report that overstates what was tested.
- A reviewer explicitly accepts a good first attempt. Include these so that the
  dataset does not consist entirely of repair dialogues.

If the capability sought is implementation, collect the chosen code or patch.
"I will make a focused change" teaches a response style; it does not demonstrate
making that change. Retain authorized repository and base-commit references,
relevant files, patch, environment version, test commands, results and limits.
A passing test suite covers the tested behavior, not all correctness. SWE-bench
provides a concrete reference for
[patch execution and per-task test reports](https://www.swebench.com/SWE-bench/guides/evaluation/).

Only information available before the choice belongs in its input. Later review
comments and final results belong in evidence unless already available to the
agent. A correction that adds requirements creates a new-context SFT candidate,
not an observed DPO comparison under the old prompt.

Keep changing repository facts and current criteria available at inference where
needed. A trained model does not automatically adopt a changed ALIGNS.md. Evaluate
whether it follows updated criteria as well as those used during training.

## Proposed contract before scaling

These additions are proposed, not enforced by the current exporter. Preserve
original evidence and create versioned training derivatives from it.

| Field group | Information to retain |
| --- | --- |
| Identity and lineage | Batch/record IDs, shared task family, source hashes, parent examples, capture/review timestamps. |
| Learning purpose | Decision text, preference pair, code patch, tool trajectory or evaluation-only case. |
| Available context | Request, criterion snapshot/version, code and constraints, known model/harness version. |
| Target and comparison | Accepted answer/action/patch, actual alternative when available, comparison context and correction reason. |
| Review | Authorized reviewer, target approval, separate pair approval, applicable criteria and unresolved disagreements. |
| Execution | Base revision, environment identifier, commands, test results, artifacts and unverified limits. |
| Data use | Selected sources, permitted training use/destinations, redaction review, withdrawal/supersession state. |
| Export | Adapter/model/tokenizer versions, target span, token counts, truncation decisions, splits and dataset hashes. |

Keep source metadata and reviewer identities out of trainer messages unless the
task needs them. A validator can enforce consistency and completeness; it cannot
prove that a human approved an answer or that a pasted test log is true.

## Collect with a manageable review burden

During opted-in active work, capture candidates at correction or acceptance events.
Reuse existing confirmations. Do not request another rating after every task,
infer acceptance from silence, or start a background logger.

At a manual checkpoint, prepare a batch with counts by purpose, novel task family,
missing evidence and exclusion reason. Remove repeated copies. Put new, ambiguous
and conflicting decisions first. The reviewer approves explicit targets; unresolved
cases remain candidates. Submission to approved private storage is a separate action.

Route approved text decisions to SFT after checking context and targets. Confirmed
same-context comparisons can also enter DPO. Code targets need replay and test
evidence before being called verified code examples. Tool trajectories need a
separate adapter. A missing requirement should defer the affected use without
discarding evidence useful for another purpose.

Track reviewed unique examples per reviewer hour, missing-evidence rate, conflict
rate, duplicate rate, verified-code share and coverage across task families,
criteria, contributors, languages and difficulty. Set targets after the pilot.
Record-count quotas encourage filler and do not establish training readiness.

Use generated variants only for identified coverage gaps. Label their origin,
preserve parent-task lineage and review targets. Rephrasing a single example does
not create independent evidence. Keep observed and generated results distinguishable.

## Implementation order

1. Validate team batches: hashes, IDs, permitted use, criterion versions, reviewer
   decisions, withdrawals and shared task families. Quarantine incomplete records.
2. Add a versioned prompt/completion adapter, context review, contradictory-pair
   checks and token-level mask/truncation inspection on a pinned target stack.
3. Add typed code/patch evidence and a restricted replay path for authorized code.
   Handle tool trajectories with a separate tested adapter.
4. Run an end-to-end pilot. Inspect a small diverse batch, then verify loading,
   target masks, one training step and evaluation loading on the chosen model.
   This is a compatibility check, not proof of learning. Conduct an authorized
   training experiment on enough independent tasks to evaluate the intended behavior.

Freeze evaluation families before variants or tuning. Keep a final test set separate
if validation drives model selection. Compare base + ALIGNS.md against tuned +
the same ALIGNS.md with the same tools and budgets. Measure code correctness,
reviewer corrections, unnecessary questions and follow-through. Check general
coding ability and changed criteria for regressions. Analyze task families, not
individual paraphrases, and report uncertainty with small samples.

The local Python environment lacked `datasets`, `transformers`, `trl` and `torch`.
No tokenizer smoke test, training step or model quality measurement was run.
These require the team's chosen model and stack. Until then, describe this feature
as preparing reviewed training candidates and text exports, not delivering a
proven team-specific coding model.
