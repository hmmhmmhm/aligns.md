# ALIGNS.md for team-specific coding-agent training data

A technical and adoption brief for engineering leaders, model teams and MLOps.

**English** · [한국어](translated-briefs/ko.md) · [日本語](translated-briefs/ja.md) · [Manual submission guide](team-training-data.md) · [Data contract](../skills/align/references/team-training.md)

## The decision this supports

Use ALIGNS.md to preserve the judgments a team already makes during code reviews
and agent conversations, then prepare approved examples for a team-run training
experiment. A reviewer explaining why a patch is too broad provides information
that a final merged patch alone may not preserve. Capturing that context, the
correction and the accepted result makes the decision available for later training.

The proposed adoption is a bounded data pilot in one repository or workstream.
ALIGNS.md supplies collection guidance, a manual review contract and local export
tools. The team controls the records, reviewers, model and training infrastructure.
No hosted intake service, background conversation logger or model training starts
when the skill is installed.

**Current readiness:** suitable for an MLOps-owned data pilot. Text and selected
tool-action exports have passed local loading/tokenizer checks with one pinned
tokenizer. Actual trainer integration and improved coding outcomes remain to be
measured. This brief reports implementation checks separately from model results.

## Where the data's value comes from

| Source | What it already contains | What ALIGNS.md asks the team to preserve |
| --- | --- | --- |
| Agent conversation | Request, proposed response and subsequent corrections | Context available at the choice, explicit target acceptance, applicable criteria |
| Code review | Patch discussion and requested changes | Why one implementation fits the team's needs, the accepted patch and its limits |
| CI or local checks | Test commands, outputs and failures | Base revision, environment and evidence attached to the reviewed code target |
| Current team criteria | Agreed priorities and constraints | Version and relevant snapshot so examples do not silently teach obsolete rules |
| Successful first attempt | An accepted result with little discussion | Explicit acceptance, avoiding a dataset made entirely of repair dialogues |

Useful cases include keeping changes maintainable, preserving an API, asking for
missing requirements at the right time, and reporting only checks actually run.
For implementation learning, collect the accepted patch or action. A promise to
make a focused change is useful response-style data, but does not demonstrate
implementing that change.

Team criteria must be explicitly agreed. A frequent comment or one maintainer's
preference is not automatically a team label. Individual agreements stay separate.

## Data products and intended uses

| Product | Contents | Intended use | Boundary |
| --- | --- | --- | --- |
| `sft-completion.jsonl` | Prompt plus one selected assistant completion | Text decision, code-patch or selected tool-action SFT | Configure completion-only loss and inspect actual trainer masks |
| `dpo.jsonl` | Same-context prompt, chosen and rejected text | Preference optimization | Human-approved comparison; no tool DPO |
| `evaluation.jsonl` | Held-out task families and expected responses | Team rubric or executable evaluation | Expected text alone is not a code evaluator |
| `manifest.json` | Sources, hashes, reviews, exclusions, counts and learning kinds | Dataset lineage and audit | Private metadata; not a trainer input |
| Legacy `sft.jsonl` | Text conversation with the selected answer appended | Existing text pipelines | Earlier assistant turns remain; use the selected-completion file by default |

The formats correspond to [TRL's documented dataset formats](https://huggingface.co/docs/trl/dataset_formats).
The selected-completion representation helps keep an earlier mistaken answer in
context without making it the selected training target. The training configuration
still matters; see [TRL's completion-only loss](https://huggingface.co/docs/trl/sft_trainer#train-on-completion-only).

Tool-action records retain function schemas, visible calls/results and one selected
assistant action. The exporter validates call linkage and function names; it does
not validate every JSON Schema argument constraint or replay an entire agent run.
Full-run trajectories and model-specific role/channel formats need an adapter.

## Controls implemented in version 0.11.0

The [initial audit](training-data-readiness.md) identified gaps in the original
text export. These changes address the reproducible failures and add a team intake
path. A supplied approval record is evidence to inspect, not cryptographic proof
of a reviewer's identity.

| Area | Initial state | Current implementation | Remaining responsibility |
| --- | --- | --- | --- |
| Team approval | Manual guidance only | Policy allowlist, explicit target/pair approval, review reference, version and timestamp checks | Control the policy and authenticate reviewers in team infrastructure |
| Artifact integrity | Source references | Submission byte hashes, canonical record hashes, hashed evidence files, output hashes | Protect storage and retain originals |
| Context | Could exist only outside the trainer input | Required prompt excerpts and reviewed input snapshot digest for version-2 records | Verify semantic completeness and avoid future-information leakage |
| Selected target | Earlier assistant answers stayed in SFT conversation | Separate prompt/completion export | Inspect trainer labels and context truncation |
| Conflicting pairs | Opposite labels could both export | Directed preference-cycle rejection for identical context and criteria | Resolve semantic or cross-context conflicts through review |
| Code evidence | Free-text verification | Required base revision, patch in target, recorded passing checks and hashed evidence | Replay in a restricted environment; assess test coverage |
| Tools | Rejected by text-only export | Function schemas, linked calls/results and selected action export | Verify tool schemas and chosen model behavior |
| Splits | User-assigned families and exact prompt checks | Shared cross-batch family assignments, exact overlap rejection, namespaced IDs | Detect related tasks and semantic duplicates before assignment |
| Withdrawal | Manual guidance | Namespaced withdrawn-record exclusions in policy | Identify prior datasets and trained models affected |
| Invalid submissions | Manual inspection | Validate before writing; no overwrite; read-only validation mode | Repair errors without manufacturing approvals |

Validation does not execute submitted code, download a model, upload records or
start training. Code evidence checks establish that the required declared evidence
is present and unchanged. They do not independently establish that tests ran.

## Reproducible engineering evidence

These are maintainer-run synthetic checks, not a third-party certification or a
model-quality benchmark. Fixtures contain no customer conversations or team records.

| Check | Observed result | What it establishes |
| --- | ---: | --- |
| Existing exporter tests | 13 / 13 passed | Personal text export controls remain covered |
| New team-data tests | 23 / 23 passed | Approved paths and rejection behavior for tampering, missing approval, context, pairs, code evidence, calls and splits |
| Repository test suite | 67 / 67 passed | Existing repository checks plus the new tests |
| Hugging Face Datasets loading | 3 SFT-completion rows and 2 DPO rows loaded | These fixture files load in Datasets 5.1.0 |
| Tokenizer boundaries | 3 / 3 examples passed | Selected target boundaries for decision, code and tool action with the tested tokenizer |
| Fine-tuning outcome | Not measured | No trained model or improvement claim |

[Named test outcomes and source hashes](../tests/audits/team-validation-2026-10-18.json) accompany these counts.

The tokenizer is `Qwen/Qwen2.5-0.5B-Instruct`, revision
`7ae557604adf67be50417f59c2c2f167def9a775`. The check used Transformers 5.20.1,
Tokenizers 0.23.3 and Jinja2 3.1.6, without model weights or PyTorch.
The three examples had 53, 75 and 186 total tokens; their selected completions
had 12, 34 and 22 tokens. A 4,096-token inspection budget was used. These short
fixtures do not establish long-context or multi-model compatibility.

[Inputs, exports and tokenizer report](../tests/audits/mlops-2026-10-18/) retain
hashes and package versions. Reproduce the stdlib checks and optional integration:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'
# In an isolated environment with the documented dependencies and local tokenizer:
python3 tests/audits/mlops_smoke.py \
  --tokenizer <local-tokenizer-directory> --output <new-fixture-output-directory>
```

## What previous benchmarks do and do not show

The existing [confirmed-preference retention pilot](../RETENTION_BENCHMARK.md)
provides a reason to investigate retained criteria. It does not test fine-tuning.

| Measure across 12 synthetic tasks per arm | Generic instructions, can learn/save | Initialized preferences plus align |
| --- | ---: | ---: |
| Preference fit without a clarification reply | 3 / 12 | 12 / 12 |
| Later clarification replies | 9 | 0 |
| Final preference fit | 12 / 12 | 12 / 12 |

The initialized arm received information the baseline initially lacked and also
received the skill and retrieval instructions. Four additional setup replies were
assumed separately. The experiment does not isolate the filename, show superiority
over equally informed AGENTS.md, or measure human time. The
[information-equivalent comparison](../DISCOVERY_BENCHMARK.md) was a tie.

These results support testing whether retaining confirmed criteria avoids repeated
explanations in a bounded workload. They cannot be converted into a fine-tuning
uplift, training-data value estimate, or financial return.

## Pilot workflow and ownership

| Stage | Owner | Deliverable | Completion criterion |
| --- | --- | --- | --- |
| Scope | Engineering lead and contributors | One workstream, agreed criteria, permitted sources and private destination | Contributors know what is collected and for what use |
| Capture | Opted-in contributor and agent | Small candidate records from active work or selected history | Actual context, target and available evidence preserved |
| Manual checkpoint | Contributor | Selected batch with file inventory | Exact submitted files approved for the selected use |
| Review | Designated team reviewer | Bound target/pair decisions and shared task families | No unresolved label promoted to training data |
| Validation/export | MLOps | Versioned data and manifest | Contract checks pass, exclusions reviewed |
| Training integration | MLOps | Pinned tokenizer/trainer, collator check and authorized pilot run | Correct masks, no truncation loss, reproducible run |
| Evaluation | Engineering reviewer and MLOps | Held-out results and regression report | Meets criteria agreed before training |

A weekly or sprint checkpoint can work, but the team chooses its cadence. Capture
at meaningful decision events, reuse existing approvals and ask only about missing
labels. The final submission stays manual. Do not impose a per-person record quota.

## Measure usable data rather than raw volume

| Metric | Definition | Decision it supports |
| --- | --- | --- |
| Approval yield | Approved unique examples / reviewed candidates | Whether capture is producing relevant material |
| Review efficiency | Approved unique examples / reviewer hours | Whether the process reduces or shifts effort |
| Task coverage | Distinct families by criterion, workstream and difficulty | Where more evidence is needed |
| Evidence completeness | Code candidates with required replay material / code candidates | Whether coding examples can be checked |
| DPO eligibility | Approved same-context pairs / reviewed comparisons | Whether preference optimization has suitable data |
| Duplicate/conflict share | Flagged records / reviewed records, reported separately | Whether quantity is inflated or labels disagree |
| Evaluation integrity | Held-out families with no known related training task | Whether the reported result tests generalization |
| Correction burden after training | Reviewer interventions per held-out task, with code correctness | Whether training improves the team's actual workflow |

Select thresholds from the pilot's costs and goals. A fixed number of examples
cannot establish readiness. Generated variants should address identified coverage
gaps, retain their parent-task lineage and remain labeled separately. Avoid counting
paraphrases as independent evidence.

## Evaluate the model before adoption

Compare the same base model with ALIGNS.md against the tuned model with the same
ALIGNS.md, tools and task budgets. Freeze task families before generating variants.
Keep a separate final test set if validation guides checkpoint selection. Check
correctness, unnecessary questions, scope choices, completion reports and reviewer
corrections; also test general coding tasks and newly changed criteria for regressions.

Report uncertainty at the task-family level. A lower correction count accompanied
by worse code is not a successful result. Current repository facts and revised
criteria may still belong in runtime context; fine-tuning does not automatically
refresh learned behavior when ALIGNS.md changes.

## Adoption boundary

The collection/export components are available under the repository's MIT license.
That license does not grant rights to contributors' code, conversations or third-party
material. The team chooses permitted training use, retention and providers. Private
source references and manifests need the same handling as the selected records.

A practical first commitment is the bounded data pilot, followed by a model-specific
integration check. Automated reviewer authentication, semantic conflict resolution,
restricted code replay, hosted intake and measured production benefits remain
outside the current implementation. The team retains control over deployment and
can stop collecting without changing its ALIGNS.md agreement.
