# Alignment session flow

Use this procedure for an active alignment conversation, including its initial
menu, intermediate questions, and completion choices. Routine project work,
installation-only requests, and a declined invitation do not open this flow.

## Remember progress in the conversation

Track the active purpose and scope, criteria already answered, authorized actions,
completed items and evidence, deferred or declined topics, and the pending question.
Use the existing conversation, not a new progress file, diary, or background job.
A resumed session reconstructs that state from available context. Clarify only a
material gap; do not reset the user to the first menu.

Track concrete work, not just menu numbers. Reviewing one set of PRs completes
that selected review, not all possible history forever. Mark an item done only
when the requested result and verification are complete. A failed write is blocked,
not saved. An item can also conclude that no criterion change is needed. Reopen
completed work only at the user's request or when relevant new evidence warrants
it, naming what changed instead of recommending the same task again.

Before choosing follow-ups, account for all six paths from available conversation:
completed, declined, deferred (with revisit condition), available, not yet explored,
or blocked by a known prerequisite. Keep a short reason for exclusions. Unknown
is not completed, declined, or inapplicable. A general project check does not
complete history review, mismatch review, rehearsal, or personal setup.

- Path 1: project criteria review completes only the agreed scope.
- Path 2: if no mismatch has been mentioned, offer “Review a decision that missed
  expectations, if you have an example.” Ask for the example only if selected;
  do not assert that a mismatch exists. If the user says there is none, exclude it.
- Path 3: an unchosen source is not a reason to omit history review. Offer source
  selection first; do not read logs or collect PRs before sources and scope are chosen.
- Path 4: completing a rehearsal does not complete the other paths.
- Path 5: mark starting-point guidance as used once it routes to a path. It is
  navigation, not another alignment exercise or evidence that all paths are done.
- Path 6: personal defaults remain an optional unexplored path until selected,
  declined, deferred, completed for the agreed scope, or excluded by a project-only
  request. Lack of a personal file or repository is not an exclusion reason.

At the first item completion and before recommending finish as the only option,
show a compact coverage summary using the stable path numbers. For example:
“Done: 1, 4. Still available: 2 (if you have an example), 3, 6. Starting-point
recommendation: 5 already used.” On later transitions show only changed status
unless the user asks for the full view. This is conversational state, not a file.

At meaningful transitions give a short progress cue, such as “Project criteria
saved and instruction connection verified. Next: choose another alignment topic.”
Do not repeat the entire checklist on every reply or invent progress percentages.

## Use the supported question interface

Inspect the tools actually available in this session and their active-mode rules.
Prefer a structured question or choice tool for unresolved selections. For example,
a Codex host may expose request_user_input_async, or a mode-restricted
request_user_input. These names are examples, not dependencies. Never call a
plan-only tool outside its supported mode, switch modes just to obtain a picker,
or pretend to have displayed buttons when only text was returned.

Keep question text self-contained. Put the recommended choice first and label it
as recommended, preserving the stable path number. Include a short reason in the
question or a supported description field. Keep ordinary-language answers valid.
Respect tool limits on option counts, headers, free text, and pending questions.
For the initial six-path menu, use text if the tool cannot show all choices; do
not silently drop paths or split one decision into several unrelated questions.
For follow-up choices, show every remaining available or unexplored path plus
“0. Finish here,” with one recommendation. Do not cap the menu at two topics.
If the tool cannot fit the full remaining set, use one numbered text question
instead; do not hide paths behind free text or make the user guess they exist.
Do not add a synthetic Other option when the tool already supplies free text.

Ask once. With an asynchronous tool, keep the choice pending while doing only
independent authorized work; do not duplicate it as another tool call or closing
question. With a blocking tool, use the returned answer. A timeout, empty result,
preselected default, or elapsed time is not a selection. If the tool is unavailable
or fails before presenting the question, use the same choices in numbered text.
Do not silently fall back to plain completion without a question.

Use an answer according to the latest pending question, not a stale menu. A “yes”
accepts a uniquely recommended next topic, not every offered action. If several
meanings remain plausible and change scope, clarify that ambiguity only. Once
answered, continue the chosen work without repeating the menu.

## Complete an item, then offer the next choice

First finish the current authorized work. Show the concrete criterion and target
scope before asking to save when authorization is missing. Reuse explicit save
permission. After confirmation, save and verify; do not pause again between a
save and its already authorized instruction connection. Preserve independent
confirmation dates and report errors rather than claiming success.

Then, unless the user said stop or “only this item”:

1. Summarize the item completed and the actual save/verification result, including
   the short return invitation once as specified in the skill. It does not replace
   the next-choice step.
2. Remove completed, declined, and currently deferred topics from next choices.
   Do not repeat a settled question under a different label. Reintroduce a deferred
   topic only when its agreed revisit condition occurs or the user requests it.
3. Include not-yet-explored paths in the remaining set. Rank topics using current
   context, dependencies and expected usefulness. Recommend one, explaining why now. Do not rank topics merely by
   their menu number. Do not perform extra history collection to choose a topic.
4. Present the recommendation, every other remaining path, and “0. Finish here,”
   using the supported question interface. Preserve path IDs 1-6; 0 always ends
   the session. Path 5 is a routing aid, not a recurring recommendation once a
   starting point has been selected.
5. Wait for a choice before opening a new scope. For already requested multi-item
   work, state the next item and proceed instead of adding a new permission gate.

Use the six paths as possible next directions, not mandatory stages. For example,
after path 1, path 4 may help test newly agreed criteria; path 3 may help when the
user has mentioned useful feedback; path 6 is an optional cross-project setup.
Do not claim a mismatch exists just to offer path 2. Do not recommend global setup
after it was declined, or imply that every user must complete all six paths.
History source selection and personal repository authorization still apply after
the user chooses those paths.

Only recommend finish as the sole option after accounting for all paths: each
substantive path must be completed for the agreed scope, explicitly declined or
deferred, outside the user's stated scope, or blocked by a known prerequisite.
Name any blocked or excluded paths and why; do not call them completed. Not having
seen a problem or source yet is not enough to hide an unexplored path. A user's
explicit stop still ends the flow immediately without a coverage interview.

If no topic remains after that check, say what is complete and recommend finishing.
Offer
“0. Finish here” with free text for a user-named topic, or an equivalent text
question. Do not fabricate another task. Once the user chooses finish, give a
brief outcome and the one-line invitation for a future session, then stop without
another next-topic recommendation or question. A stop or single-item-only
request permits direct closure without this finish picker. Completing an item
alone does not imply that the user chose to finish the session.

## Example: project criteria are saved

Context: path 1 is complete, no further items were authorized, and the user has
not reviewed history, reported a mismatch, or declined personal setup. The current
criteria include stopping boundaries that have not been tried in a scenario.

Completion: “The project criteria are saved, and the instruction link is verified.”

Question: “Testing a few hypothetical decisions would help check the stopping
boundaries we just agreed on. What would you like to do next?”

- 4. Rehearse decisions (recommended)
- 2. Review a decision that missed expectations, if you have an example
- 3. Choose PR or conversation history to review
- 6. Review personal defaults across projects
- 0. Finish here

Use the client's question tool for these choices when supported. If path 4 was
already completed or declined, exclude it and reassess the remaining topics.
The example does not prescribe these same choices after every project review.
