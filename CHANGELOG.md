# Changelog

## 0.9.1

- Keep required Codex async choices pending instead of immediately issuing a completion response; wait through supported mechanisms and resume from the answer.
- Distinguish dispatch acceptance from visible UI and user input. Honor cancellation and superseding requests.
- Include a question-resume link only when officially supplied or documented, without guessing routes or IDs.

## 0.9.0

- Add optional path 7 to place the ALIGNS.md badge in a project README, offered only after confirming that it is absent.
- Reuse the provided badge and existing layout, distinguish displayed badges from code examples, and skip duplicates.
- Extend session coverage and instruction templates to seven paths while preserving existing numbers and optional scope.

## 0.8.4

- Keep every remaining alignment path visible, including unexplored history review and optional personal setup, instead of limiting follow-ups to two topics.
- Account for all six paths before offering finish alone; distinguish unknown context from completed or inapplicable work.
- Preserve optional paths, source selection, explicit stopping, and scope boundaries; fall back to a full numbered list when a question UI cannot fit the choices.

## 0.8.3

- Use “Let’s do a self-alignment check” in English return invitations and accept both “self alignment” and “self-alignment” requests.
- Define self-alignment as clarifying user criteria and checking agent work against them, with matching explanations in all README languages.

## 0.8.2

- Recognize “자가정렬 진행해봅시다” as a natural-language request to start or resume alignment.
- Add a short return invitation at installation, alignment-item, and ordinary task completion through the skill and instruction templates.
- Keep ongoing choices intact, avoid duplicate reminders, and distinguish refreshed instructions from a method-only update.

## 0.8.1

- Separate item completion from session completion with a next-choice step and an explicit finish option.
- Exclude completed, declined, and deferred topics; recommend the most useful eligible next step and preserve progress across replies.
- Prefer supported structured-question tools within their mode limits, with numbered text as fallback and no implied selection from defaults.
- Preserve direct closure for stop or single-item-only requests and continue already authorized work without extra gates.

## 0.8.0

- Resume authorized alignment work after menu, client, source, and storage answers instead of ending with another invocation suggestion.
- Confirm concrete saves when needed, reuse existing authorization, and offer one relevant next topic after completing an alignment item.
- Preserve scope choices and stopping; do not invent follow-ups or turn routine work into an interview.
- Use natural-language requests throughout current skill guidance, UI prompt, and all README translations while retaining the skill name and existing aliases.

## 0.7.1

- Describe optional source material as user-selected personal documents or notes, with no required filename or format.
- Synchronize this wording across the skill, usage guide, and English, Korean, and Japanese READMEs.

## 0.7.0

- Add optional menu choice 6 for personal alignment across projects; keep choices 1-5 stable.
- Review selected personal documents or notes for scoped criteria without importing private details or workplace rules indiscriminately.
- Support local files, selected checkouts, and user-requested clones through a private user-level pointer, with separate synchronization authorization.
- Keep personal defaults, project exceptions, and confirmation dates independent; retain project-only use.

## 0.6.2

- Require align for alignment work and check applicable required skills from the actual session workspace.
- Distinguish files on disk, client discovery, and loading the method; disclose manual fallback and blocked steps accurately.
- Preserve scoped specialist requirements without turning recommendations into dependencies or checking installations on every task.

## 0.6.1

- Carry confirmed personal criteria into specialist-skill briefs and result reviews.
- Keep specialist defaults separate from user preferences and resolve settled conflicts without another question.
- Preserve instruction hierarchy and permissions; report exceptions to specialist checks without changing criteria or claiming a pass.

## 0.6.0

- Offer five numbered starting points when align is invoked without a clear purpose. Accept numbers or free-form answers.
- Show a short outline for the selected path and identify meaningful step transitions.
- Skip the menu for clear requests, reuse prior choices, and preserve history-scope and agreement authorization.

## 0.5.2

- Review unresolved criteria when a loop or goal is configured, stops, or is marked complete against user expectations.
- Separate judgment mismatches from known errors, usage limits and requested pauses. Preserve restart permissions and completion evidence.
- Clarify that discovery requires an active agent turn; the skill cannot wake a stopped process.
- Retain loop/goal discovery evidence, including a rejected description that loaded the method for unnecessary cases.

## 0.5.1

- Ask for an actual criterion before creating an agreement from a vague request to learn preferences. Keep unrequested drafts in the conversation.
- Continue saving explicit lasting preferences without another confirmation.
- Add reproducible multilingual discovery checks with retained requests, execution evidence and offline replay.

## 0.5.0

- Check existing context before asking about a brief request.
- Group questions about consequential gaps and proceed within delegated scope.
- Use repeated context-related misunderstandings to review when the user wants questions.
- Keep task answers separate from confirmed lasting preferences.

## 0.4.0

- Rename the project, agreement file, repository, and site to ALIGNS.md.
- Keep `$align` as the skill invocation.
- Preserve existing criteria when migrating a legacy `ALIGN.md`; never replace it with a new agreement.
- Retain original benchmark transcripts and source snapshots under their recorded names for verification.

## 0.3.0

- Add optional recent/full PR and project conversation review with disclosed time estimates.
- Collect paginated PR feedback with partial coverage reports and resumption.
- Parse selected Codex and Claude JSONL text while retaining project boundaries.
- Use scoped, revisable taste invariants to propose criteria from evidence, with
  counterexamples and confirmation before inferred criteria become agreements.

## 0.2.0

- Make align a maintained practice with focused review after consequential drift,
  recurring missing criteria, uncertain direction, and before long autonomous work.
- Add Codex and Claude Code plugin marketplaces, explicit update policies, and a
  static Claude SessionStart reminder.
- Connect the primary CLI's instructions while preserving distinct client files.
  Provide a helper for safe relative links and an idempotent trigger block.
- Replace the standalone README interview with an installation request.
- Record invocation and update mode in new agreements; preserve confirmation dates
  during method updates and narrow reviews.

## 0.1.0

- Initial project alignment skill and public distribution.
