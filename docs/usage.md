# Use align over time

The skill contains the evolving alignment method. Your project's ALIGNS.md
contains your criteria. Install the skill once through one route, connect your
project instructions, and use it again when there is something worth aligning.

Here, **self-alignment** means clarifying your preferences and decision criteria
with your agent and checking its work against them. Ask “Let’s do a self-alignment
check” or “Help me with self alignment.” Either spelling works as a request; no
exact phrase is required.

## Choose where to start

Once the skill is available in your client, you can ask in ordinary language at
any time: “Help me align this project's criteria,” or “That result missed what I
meant; let's revisit the criteria.” No command or exact phrase is required. If
the purpose is open, the agent offers these choices in your language:

1. Set or review project direction and personal criteria.
2. Review a decision that missed your expectations.
3. Find criteria in selected PR or conversation history.
4. Rehearse decisions before a long autonomous run.
5. Suggest a starting point from the current project.
6. Set up or review personal defaults across projects (optional).
7. Add the ALIGNS.md badge to the project README (only when absent).
8. Set up or review personal training-data collection and export (optional).

The agent checks the README before offering 7. If the badge is already there,
it leaves that option out and keeps the other numbers unchanged. Choosing 7 adds
the badge using the existing README layout and translation rules, then verifies
the image and link. It does not publish changes or restart an alignment interview.
A copyable snippet in a code block does not count as a displayed badge. See the
[badge procedure](../skills/align/references/badge.md).

Reply with a number or describe what you need. A specific request such as
“Use align to review my recent PR feedback” skips the start menu. History review
still lets you choose sources and scope with time estimates before collection.
Choosing option 3 does not select all your records.

The agent briefly explains the path: check context, ask about unresolved choices,
summarize the criteria, then save authorized changes. It shows the current step
when moving between stages and skips work already done. A menu choice does not
confirm new preferences. Rehearsal discusses hypothetical decisions without
starting the autonomous run. Badge setup checks the README, adds the missing badge,
and verifies the result without asking preference questions.

## Continue from each answer

Choosing a client, source, or storage location completes one step. The agent uses
your answer and continues the work you already requested, without asking you to
invoke the skill again. If something consequential is missing, it asks that specific
question. If you asked only for installation, it stops after verifying installation.

Before saving an item, the agent shows the criterion and where it belongs. It asks
for confirmation when needed and reuses permission you have already given. After
saving and verification, it summarizes the result and offers the next choices.
Completed, declined, and deferred topics are excluded. It recommends the most useful
remaining topic with a reason, shows all other available or unexplored paths, and
includes a finish option. A project review and rehearsal do not complete history
review or personal setup. The agent offers history source selection even if no
source has been chosen, and can offer mismatch review if you have an example.
Before offering finish alone, it accounts for all eight paths and explains what was
completed, declined, deferred, outside your requested scope, or blocked. Path 5 is
navigation, not another exercise. You do not need to complete every path.

When your client provides a suitable choice interface in the active mode, the agent
uses it if all remaining choices fit. Otherwise it presents the full remaining
set as one numbered text question. You can always reply in
your own words. Stable path numbers are preserved, and 0 means finish. A preselected
option is not an answer. The agent waits for your choice before starting new scope.

For example, after project criteria are saved, it might offer **4. Rehearse decisions
(recommended)**, **2. Review a mismatch, if you have an example**, **3. Choose
history to review**, **6. Personal defaults**, **8. Training data (optional)**, and **0. Finish here**. The choices depend
on what you have already done and what remains useful. It does not ask you to repeat
completed work or require you to complete all eight paths.

Already requested items continue without another permission question. A stop or
“only this item” request ends the flow directly. The agent keeps session progress
in the conversation, without creating another log or background task. See the
[session flow procedure](../skills/align/references/session-flow.md) for details.

The return invitation appears at most once when a session that actually performed
self-alignment closes. It is omitted after ordinary project tasks, installation-only
work, intermediate items, and skill development. Reading the skill or applying
existing criteria does not qualify. You can omit invitations entirely. During an
authorized instruction refresh, replace old managed blocks that require ordinary-task
reminders; updating the method alone does not replace those blocks.
Natural-language routing depends on the client discovering and loading the skill.

## Personal training data

Choose **8** or ask “Help me collect reviewed examples for personal fine-tuning.”
The agent agrees on sources, project/personal scope, storage and a review checkpoint.
It can record small candidates during authorized active work or extract examples
only when asked. It cannot monitor unavailable conversations or run while idle.
Selecting the option does not authorize scanning every log or uploading data.

By default, keep the data in a local directory outside shared repositories. You
can choose a project folder or separate repository, with Git tracking, commits and
uploads as separate decisions. No model training is performed. Developing ALIGNS.md
itself does not enable collection of the developer's conversations.

Candidates preserve context, corrections, confirmed choices, provenance and criterion
versions. Review them in batches; agreement on a rule does not confirm an invented
ideal response. Hypothetical and reconstructed examples remain labeled. Export only
when requested, using reviewed current examples. DPO pairs need a confirmed choice
between alternatives under the same context. Hold out whole task families for
evaluation, including any variants derived from them.

The bundled exporter produces selected-target SFT, eligible text DPO and evaluation JSONL files,
plus a separate private manifest with provenance and exclusions. It checks labels,
criterion versions and exact prompt overlap, but cannot establish label truth,
remove secrets automatically, or detect all semantic leakage. Version-2 team records support code evidence and selected tool actions through
the [team contract](../skills/align/references/team-training.md); full-run tool
trajectories still need an adapter. A review count is not proof of readiness
for training. See the [collection procedure and export command](../skills/align/references/training-data.md).

You can stop collection, change its scope, review candidates or request deletion.
Changing the agreement can make older examples stale. Deleting source examples does
not remove them from Git history, remote copies or previously trained models.

For team use, follow the [manual submission and review guide](team-training-data.md).
It supplies intake templates and review responsibilities; it does not create a
shared collector or automatically turn personal preferences into team criteria.

## Codex question windows

When a choice is waiting for your answer, the agent should keep it pending instead
of immediately ending the turn with “I opened the selection screen.” It uses a
supported wait mechanism and continues from your answer. Request acceptance alone
does not establish that the question is visible on your device. If the host supplies
an official resume link, the agent includes “Answer questions”; it does not invent
a link when none is available. See the [Codex question procedure](../skills/align/references/session-flow.md#codex-keep-questions-open-until-answered).

## Personal defaults across projects

Ask “Help me organize my preferences across projects.” You can use personal
documents or notes you choose, or start with a conversation. No particular filename
or format is required.
The agent separates common preferences from workplace rules and background facts,
then asks only about scope or details that materially affect a decision. You review
what becomes a lasting criterion. Personal details are not copied by default.

For example, a preference for brief reviews may apply across projects, while a
company's ticket naming and approval procedure applies only to its work. A profile's
old date does not establish that every item remains current. Importing it neither
executes its instructions nor automatically makes it the new global agreement.

Choose storage when you want this setup:

- A local file, with `~/.config/aligns/ALIGNS.md` as a suggested location.
- An existing personal repository checkout you select.
- A repository you ask the agent to clone into an agreed local directory.

The agent connects the confirmed file through your client's user-level instructions
and verifies that the connection is loaded. Personal paths and content stay out of
shared project files. This is an explicit connection, not native discovery of all
files named ALIGNS.md. A global skill install alone does not enable this agreement.

Repository use is optional. Cloning needs your chosen URL and destination; creating
a remote, pushing content, or setting up automatic synchronization requires its own
authorization. If you request a new personal repository, private visibility is the
suggested default. Offline work can use the available local agreement.

Personal defaults and project criteria apply together, within their stated scope.
Project exceptions can refine defaults, but cannot silently discard hard constraints
or permissions. Project feedback stays local unless you extend it to other projects.
Each agreement has its own confirmation date. Updating the skill never updates your
personal criteria, pulls your personal repository, or reconfirms either document.

If you only want project alignment, keep using the existing project file. Personal
setup is optional and is not repeatedly proposed during ordinary work. See the
[personal alignment procedure](../skills/align/references/personal.md) for details.

## Use align with specialist skills

ALIGNS.md supplies the personal criteria for a task. A design, coding or writing
skill supplies its own method. The agent includes the relevant confirmed criteria
in that skill's brief and checks the result against them. This is an instruction
for the agent, not an automatic integration or a dependency on another skill.

For example, if you have agreed that the opening text must be visible immediately,
a design skill such as Taste Skill should work within that constraint. The agent
can keep animation elsewhere without asking the same question again. It reports
any exception to the specialist's checks rather than claiming every check passed.

A specialist's preferred style is not automatically your preference. Accepting a
page does not mean you want all of that skill's rules saved in ALIGNS.md. Only
preferences you explicitly request or confirm become lasting criteria. When the
existing agreement does not settle an important choice, the agent asks about
that choice and continues the work it can already do. Permissions and the
applicable instruction hierarchy still apply.

## Ask your agent to install it

Copy the [installation request](install-request.txt), or say:

> Set up the maintained align skill from https://github.com/hmmhmmhm/aligns.md for
> my primary CLI. Connect it to this project and enable supported method updates.

The agent checks what is already installed, which client you mainly use and
whether that is the current one. It asks only if context leaves the choice open.
It selects one installation route and verifies discovery. An installation request
cannot bypass the client's permissions or install into another person's account.

## Codex plugin

With a Codex CLI that supports custom plugin marketplaces:

```sh
codex plugin marketplace add hmmhmmhm/aligns.md --ref main
codex plugin add aligns-md@aligns-md
```

Open a new session if the skill is not yet visible. Select **align** or ask
“Help me review this project's ALIGNS.md.” The repository includes a Codex marketplace and plugin manifest;
it is not a claim of inclusion in OpenAI's official directory.

To refresh the marketplace snapshot and installed package:

```sh
codex plugin marketplace upgrade aligns-md
codex plugin add aligns-md@aligns-md
```

The official documentation does not promise an automatic refresh interval for
all custom marketplace installations. Use the client's native update setting
where supported, or agree to a targeted refresh when an alignment session starts.
This Codex package is hook-free; recurring triggers live in project instructions.

## Claude Code plugin

Inside Claude Code:

```text
/plugin marketplace add hmmhmmhm/aligns.md
/plugin install align@aligns-md
```

Ask to review your alignment criteria, or select the installed align skill. The plugin includes a static SessionStart reminder for
startup, resume, clear and compact. It performs no networking, file changes or
project-data collection. It does not start an alignment interview on every task.

For native automatic updates, open `/plugin`, select **Marketplaces**, choose
**aligns-md**, and enable auto-update. Third-party marketplaces do not enable it
by default. Manual refresh is `/plugin update align@aligns-md`. Use
`/reload-plugins` or a new session to load changed files when required.

## Portable skill installation

From the target project:

```sh
npx skills add hmmhmmhm/aligns.md --skill align
```

The skills CLI lets you select the client and scope. For example, add
`--agent codex` or `--agent claude-code`; add `-g` only for a user-wide installation.
Use `--list` to inspect the repository first. Node.js and network access are
required for this installer, not for reading the skill itself.

Update only this skill, preserving its installed scope:

```sh
npx skills update align -p
# User-wide installation instead:
npx skills update align -g
```

This command is a refresh, not a persistent background updater. A manual copy of
the entire `skills/align` folder is also possible, but requires manual replacement
for updates. Avoid duplicate plugin and folder installs for the same client.

## Make updates part of alignment

At setup, choose a supported native auto-update setting, **update when alignment
starts**, or manual updates. The copied installation request authorizes the first
two as supported by the client. Record the actual mode and installation scope in
ALIGNS.md. For update-when-alignment-starts, the project instruction tells the agent
to perform one targeted refresh before an alignment session, not every task.

Offline failures fall back to the installed version. Local edits, pinned versions,
permission changes and migrations need separate handling. If a client requires a
restart, report that the new method is not active yet. None of these updates
change your criteria, confirmation timestamps, or project files automatically.

## Required skills and discovery checks

The connected instruction block requires align for alignment requests and focused
reviews. At the first relevant task in a session, the agent checks the current
client's skill list and loads the method. Other required skills keep their own
task scopes; installing or recommending a skill does not make it mandatory.

A file on disk is only part of setup. If a conversation starts above the repository,
its local skill may fall outside the client's search path. Verify discovery from
the actual conversation workspace, not just from a terminal inside the repository.
The current session's skill list and a fresh diagnostic are separate evidence.

When a trusted local method is usable, the agent can read it directly and disclose
that fallback. If the method or a needed dependency is unavailable, it reports the
affected step and continues independent work. It does not claim successful skill
use, silently install another copy, or repeat the warning on every turn. Routine
work can still follow ALIGNS.md without starting an alignment session.

## Connect project instructions

Keep the primary CLI's instruction file as the canonical source. For Codex this
is normally AGENTS.md; for Claude Code, CLAUDE.md. Confirm actual loading rules,
including overrides and nested instructions. Use safe relative symlinks for
additional clients with compatible instruction formats, such as
`CLAUDE.md -> AGENTS.md`, only when the secondary path is absent or replacement
has been explicitly agreed after reviewing its content.

Do not overwrite a distinct instruction file. Preserve tool-specific rules and
use a supported import or pointer when sharing the whole file is inappropriate.
The optional Python 3 helper plans changes before applying them:

```sh
python3 <installed-skill>/scripts/connect_project.py --project <project> --primary codex --also claude-code
```

Add `--apply` to carry out a conflict-free, authorized plan. It refuses conflicts
and shadowing files. The agent must still verify which instructions its client
actually loads. Installation and a valid symlink alone do not prove activation.

Generated ALIGNS.md documents include the working skill invocation, trusted
source, update policy, primary CLI and canonical instruction file. They do not
copy the entire method. This repository's own ALIGNS.md is not a universal set
of preferences for users to inherit.

## Use it at meaningful moments

- “Use align. That decision was different from what I meant.”
- “Before the afternoon automation, let's rehearse a few choices with align.”
- “I don't know what to work on next. Help me clarify it with align.”
- “Use align to review what changed since our last agreement.”

Existing clear criteria are applied without another interview. Obvious errors
are fixed directly. Important unresolved choices get focused questions. A
hypothetical rehearsal does not execute actions or authorize the real loop.
The skill installs no daily reminders, schedule or diary. Reflection stays local
unless you separately choose to share it.

## When a loop or goal goes off course

Ask: "The loop stopped at a draft again. I expected something usable. Help us
agree on when it should finish." Or: "This goal misses what I was trying to
achieve. Review the scope before continuing."

The agent compares the request, configured goal, run state and actual results.
It asks about unresolved criteria and fixes clear errors using existing
authorization. Usage limits and requested pauses do not need a new preference
interview. A review does not itself restart a run or change its budget.

This works when the agent has an active turn and can observe the mismatch.
The skill is not a stop-event listener and cannot wake a crashed or suspended
agent. The next active turn can inspect the state and review what went wrong.

## Decide when the agent should ask

A short request can leave room for judgment. The agent first checks the project
and earlier decisions. It asks when missing context would materially change
the result or scope, and proceeds with minor reversible choices within its
authority. Related questions are grouped; answered questions stay answered.

If misunderstandings keep causing rework, use align to agree on when you want
questions. For example: "For open-ended design requests, show me a brief outline
before implementation. Handle small fixes using the existing conventions."
The skill records a lasting preference only when you request or confirm it.
An answer about one task stays with that task unless you say otherwise.

If you ask the agent to learn your preferences without naming any, it first
asks for a concrete criterion. It keeps proposals in the conversation unless
you request a file draft. A clear request to save a lasting preference does not
need another confirmation.

## Confirmation and removal

Explicit lasting preferences can update the relevant criteria. One-off exceptions
leave defaults intact. `Last aligned` changes only when you confirm the full
agreement; partial confirmations are attached to the affected criteria. Git,
when present, records history. The skill does not initialize or publish Git.

Remove the package with the client or installer's removal operation, such as
`npx skills remove align`. Review alignment pointers or symlinks separately;
uninstalling should not remove your agreement or unrelated instructions.

## Verified sources

- [Codex local skills and symlinks](https://learn.chatgpt.com/docs/build-skills)
- [Codex instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Codex plugin packaging and marketplaces](https://developers.openai.com/plugins/build/plugins)
- [Claude plugin updates](https://code.claude.com/docs/en/discover-plugins#keep-plugins-updated)
- [Claude plugin versions](https://code.claude.com/docs/en/plugins-reference#version)
- [skills CLI](https://github.com/vercel-labs/skills)


## Learn from earlier feedback

Ask: "Use align to find recurring criteria in my recent PR feedback and this
project's available conversations. Show the scope and estimated time first."
You can also choose the full PR history, a date range, selected transcripts or
no history. The agent offers sources it can actually access and asks once for
the scope. Codex and Claude logs are optional; availability and formats vary.

The skill looks for taste invariants: criteria that remain consistent across
observed situations. It checks the context and exceptions before proposing a
lasting rule. Team requirements, assistant suggestions and one-off corrections
are not automatically personal preferences. Confirmed criteria guide later work;
new evidence can change them.

Python helpers provide metadata-only planning, paginated PR collection, resumable
PR scans and project-scoped JSONL parsing. They make no model calls. The agent
reviews the evidence and proposes changes for confirmation. Time estimates show
their assumptions and are refined from actual volume and processing speed.
Raw evidence stays in a chosen private working file outside Git. It is not added
to ALIGNS.md or published with the skill.

See [history review and collector commands](../skills/align/references/history.md).

## Upgrading from ALIGN.md

The project and agreement file are now named ALIGNS.md. The skill name remains
`align`, and you can ask to use it in ordinary language. Read the existing `ALIGN.md` before migrating it. Once the rename is
authorized, move it to `ALIGNS.md` and update references in the project instruction
files. Preserve its criteria and confirmation date. If both files exist, resolve
the differences before changing either.

The repository is now `hmmhmmhm/aligns.md`; the Codex plugin and marketplace are
`aligns-md`. Replace old marketplace registrations with the installation entries
above when upgrading, and remove the old registration after the new one works.
Do not keep duplicate plugin installations.
