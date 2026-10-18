# Project Alignment

## Purpose

Help agents make decisions that reflect the user's judgment and
continuously identify and address gaps between their work and
the user's expectations.

Alignment is an essential part of working with AI. It deserves
a dedicated document because expectations differ between users
and evolve over time.

## Role of ALIGNS.md

ALIGNS.md holds the user's current goals, priorities, preferences,
constraints, and decision criteria.

Keep these separate from harness configuration and general agent
instructions. AGENTS.md should explain when and how to use ALIGNS.md,
while ALIGNS.md remains the source of alignment criteria.

## Scope

Focus initially on alignment between an individual user and their
agents. Multi-user agreements and conflict resolution are outside
the initial scope.

Provide an easy-to-use skill that works across new and existing
projects. Make it discoverable through relevant skill directories
and distribution services, verifying support and registration
status rather than assuming universal coverage.

## Success Criteria

- Agents make decisions consistent with the user's stated criteria.
- Agents notice meaningful misalignment and propose corrections.
- Users spend less effort repeating expectations and correcting
  avoidable misunderstandings.
- The skill is easy to discover, adopt, and use.

## Operating Principles

- Ask only consequential, unresolved questions.
- Distinguish confirmed expectations from assumptions.
- Adjust autonomously within existing agreements.
- Reflect lasting changes when the user's intent is clear.
- Do not turn one-off exceptions into permanent preferences.
- Never rewrite agreements to justify an agent's own results.
- Continue independent work while a decision awaits clarification.

## Questions when context is missing

When my request is brief, use the existing conversation and project documents
first. Ask only for missing information that would materially change the result
or scope, grouping related questions. Make minor reversible choices and already
delegated decisions within the authorized scope. Do not repeat answered questions.

The shared skill should help users agree on when to ask and when to proceed.
Repeated misunderstandings can prompt a focused review of that preference.
Keep task-specific answers separate from lasting criteria, and save the latter
only on explicit direction or confirmation. Never infer a user's ability or
personality from how little context they provide.

## State and History

Check whether the target project uses Git.

Keep only current alignment criteria in ALIGNS.md. When Git is
available, use its history to track changes instead of maintaining
a separate alignment log.

If Git is unavailable, explain the history limitation. Do not
initialize Git or create an alternative history file without
a user request.

Review available changes since the last alignment for meaningful
drift or new criteria. Do not repeat resolved questions without
new evidence.

Record the last full alignment time only after the user confirms
the document. Record partial confirmations separately without
implying a full review.

## Project name

Use ALIGNS.md for the project and agreement file, and hmmhmmhm/aligns.md for the
repository. Keep `align` as the skill name. The acquired aligns.md domain will
be connected separately after DNS propagation. Preserve historical benchmark
evidence and its hashes when updating current branding.

## Presentation and Licensing

- Keep English as the source of truth for repository documentation. Maintain
  Korean and Japanese README translations in the same change when shared content
  changes, preserving claims, instructions, section order, and images.
- Apply the appropriate humanizer skill to English, Korean, and Japanese prose.
- Do not use em dashes or emoji.
- Keep the README brief, with a centered title, useful badges,
  and a copyable installation request.
- Publish the project publicly under the MIT License.

## Maintained Skill and Recurring Use

Distribute the alignment method as a maintained skill. README and site copy
should guide users to install it, rather than preserving a standalone interview
prompt. Support native plugin updates where verified and a user-authorized,
targeted refresh at alignment-session start elsewhere. Keep method updates
separate from personal criteria and never promise universal background updates.

Suggest focused alignment after consequential judgment mismatches, repeated
corrections that reveal missing criteria, and when users are unsure of direction.
Before long autonomous runs, propose hypothetical scenarios for uncovered
trade-offs and stopping boundaries. Fix clear errors without an interview.
Make reflection an available habit, without imposing diaries or reminders.

Check the primary CLI at setup and whether it is the current client. Keep its
native instruction file canonical, safely linking other compatible entrypoints
when needed. Preserve distinct and nested instructions. Record the skill's
invocation and update policy in project ALIGNS.md documents.

## Choosing an alignment path

Offer numbered choices and a brief outline of the steps when the user invokes
align without a clear purpose. Accept numbers and natural-language requests.
When the purpose is already clear, begin that work without repeating the menu
or asking the user to choose again. Keep the detailed procedure in the skill.

## Optional personal scope

User-requested scope update: 2026-10-18 (Asia/Seoul). Partial confirmation only.

Offer personal defaults across projects as an optional sixth alignment path,
keeping existing menu numbers stable. Let users bring personal documents or notes they choose,
without requiring a filename or format, separating common criteria from workplace rules and
unneeded biographical details. Keep each agreement's scope and confirmation
independent. Never publish a user's profile as shared skill content or fixtures.

Support local storage and, only when requested, an existing or cloned personal
repository. Keep private agreements outside shared project repositories. A method
update or project correction must not silently change personal defaults or enable
remote synchronization. Preserve project-only use without recurring setup prompts.

## Conversation continuity

User-requested scope update: 2026-10-18 (Asia/Seoul). Partial confirmation only.

Carry setup answers and menu choices into the next authorized step. Ask to save a
concrete item when needed, reusing existing authorization. After completing an
alignment item, summarize completion and offer a next choice, excluding completed,
declined, or currently deferred topics. Recommend the best eligible next topic
with a reason, or recommend finishing when none remain. Include a finish option.
Use the client's supported structured-question UI when available in the active
mode, with numbered text as fallback. Track progress in the conversation, not a
new log. Continue already requested work; let the user choose before expanding
scope. Honor stopping and single-item-only requests. Use natural-language
invitations instead of requiring command syntax.

## Working with other skills

Make align useful alongside specialist skills for development, design, review,
and writing. Apply the relevant confirmed personal criteria to their work.
Keep a specialist's default style separate from the user's preferences, and
reuse decisions already settled in ALIGNS.md. Maintain a separate document of
recommended companion skills with sources and reasons to use them together.

## Loop and goal mismatches

Include incorrectly configured goals and unexpected loop stops among the
occasions for focused alignment. Compare the requested outcome with the
configured objective, stopping conditions, and actual result. Repair a known
execution error directly; ask only about unresolved judgment criteria.
The method must not imply that it can wake a stopped agent or that a review
alone authorizes restarting work or expanding its scope.

## Evidence and communication

Emphasize how carrying confirmed preferences forward reduces the user's effort
in explaining preferences and correcting work. Use accessible benefit-focused
copy in the README and landing page, with links to public benchmark evidence.
Keep experiment methods and results available for independent review. Distinguish
synthetic results from measured human effort and retain the original evidence.

## Landing page presentation

Maintain English, Korean, and Japanese versions, defaulting to the browser's
language and allowing manual language selection. Use the dark theme with a black,
paper-textured background. Use Pretendard with sufficient font weight, and apply
word-break and text-balance treatment across languages, including document examples.

Keep scrolling illustrations and text coordinated on desktop and mobile. Bound
hero image proportions on wide screens while using the available space well.
Keep the first screen's text readable without scroll-driven typing or focus;
apply those text effects after the first section. Keep scroll animation enabled
without an animation or theme toggle. Offer reusable project badges and use a
GitHub icon for GitHub calls to action.

## History-informed alignment

Support full paginated PR feedback collection and recent-first review. Offer
accessible project conversations, including supported Codex and Claude records,
as optional evidence. Show sources, scope and estimated retrieval/analysis time
before collection; reuse the user's choice and refine estimates as work proceeds.

Use taste invariants during self-alignment: scoped, revisable criteria supported
by the user's decisions across situations. Examine exceptions and conflicting
evidence. Do not infer immutable personality traits, treat team feedback as
personal consent, or promote repetition into an agreement. Keep the maintained
method in the skill and confirmed current criteria in ALIGNS.md.

## Revisit Alignment

Primary client: Codex. Canonical instruction file: AGENTS.md.
Ask “Help me review this project's ALIGNS.md,” or describe the criteria you want
to revisit in ordinary language. No command is required. A clear request skips the menu.
This development repository discovers its local skill through
`.agents/skills/align`, linked to `skills/align`. Method changes are maintained
in this repository's Git history; do not install a second plugin copy here or
automatically pull over local development changes.
Source and user installation guide: https://github.com/hmmhmmhm/aligns.md .

Last aligned: 2026-10-18 12:51 (Asia/Seoul).
