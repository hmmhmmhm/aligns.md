# Skills to use with ALIGNS.md

ALIGNS.md keeps the criteria you have agreed with your agent. Add a specialist
when the work needs a particular method: planning, design, performance review,
browser testing or editing. Start with the task you have, then choose one.

Reviewed on **2026-10-18**. These recommendations come from reading the upstream
instructions and checking current directory listings. They are not a combined
compatibility benchmark or a claim that every client supports every package.

## What is showing up now

The [skills.sh all-time list](https://skills.sh/) includes skill discovery,
browser automation, frontend design, React performance and development workflows.
Its [trending view](https://skills.sh/trending) also prominently lists image and
video tools. This is a snapshot of listed activity, not evidence of quality or
long-term growth. The selection below favors a clear role alongside align;
media-generation tools are useful when a project actually needs them.

## Choose by the work

| When you need | Suggested skill | What to carry from ALIGNS.md |
| --- | --- | --- |
| A development process from design through implementation and review | [Superpowers](https://github.com/obra/superpowers) | Scope, accepted decisions, autonomy limits and completion criteria. Reuse settled answers during planning. |
| Art direction and visual review for a public website | [Taste Skill: `design-taste-frontend`](https://github.com/Leonxlnx/taste-skill/blob/main/skills/taste-skill/SKILL.md) | Brand constraints, imagery preferences, motion boundaries and the desired reading experience. |
| A different approach to frontend design | [Anthropic: `frontend-design`](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) | Audience, visual references, tone and how much experimentation you want. Choose this or Taste as the lead design method. |
| React or Next.js performance work | [Vercel: `vercel-react-best-practices`](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/SKILL.md) | Performance priorities, maintenance constraints and the scope of acceptable changes. Use it for the relevant stack. |
| A review against web interface guidelines | [Vercel: `web-design-guidelines`](https://github.com/vercel-labs/agent-skills/blob/main/skills/web-design-guidelines/SKILL.md) | Intended interactions and project constraints. The skill checks source files against current guidelines; it does not replace browser testing. |
| Browser interaction and evidence from the running app | [Vercel: `agent-browser`](https://github.com/vercel-labs/agent-browser) | Which flows matter, what counts as success and which actions are authorized. It includes a CLI and browser requirements, not just an instruction file. |
| English prose that sounds like its author | [Humanizer: `humanizer`](https://github.com/blader/humanizer/blob/main/SKILL.md) | Voice samples, terminology, tone and wording to avoid. Preserve facts and use a suitable language-specific editor for other languages. |
| A specialist for a task missing from this list | [Vercel: `find-skills`](https://github.com/vercel-labs/skills/blob/main/skills/find-skills/SKILL.md) | The actual capability needed, client and installation scope. Discovery does not require installing everything it finds. |

## Combinations worth starting with

### Building software: align + Superpowers

Use align when personal criteria need clarification or revision. Give those
criteria to Superpowers for its design, planning, implementation and review work.
Both can ask about intent, so carry answers forward instead of running two fresh
interviews. Use the [upstream installation guide](https://github.com/obra/superpowers#installation)
for the full workflow and the client's supported setup.

### Building a landing page: align + one design skill + review

Choose Taste Skill when you want its direction-selection scripts, browser checks
and screenshot critique. Its current default targets public-facing pages rather
than dashboards or app screens. The scripts require Node 22+ and a supported
Chromium browser; finding images needs network access. See the
[Taste installation guide](https://github.com/Leonxlnx/taste-skill#install).

Anthropic's frontend-design is an alternative that develops a design plan from
the brief, reviews it and critiques the implementation. Give one skill ownership
of the visual direction. Their defaults differ, including how much motion to use;
loading both does not resolve that choice.

After implementation, use web-design-guidelines for source review and the
available browser tooling for visible behavior. Add agent-browser if you need
that capability and the environment supports its
[installation requirements](https://github.com/vercel-labs/agent-browser#installation).

### Improving React performance: align + Vercel React Best Practices

State the agreed priority, such as faster initial loading within the existing
stack. The skill then provides guidance on data-fetching waterfalls, bundles and
rendering. Judge any proposed complexity against the maintenance criteria already
in ALIGNS.md. Measure the result before claiming a speed improvement.

### Writing documentation: align + Humanizer

Keep the audience and confirmed voice in ALIGNS.md. Give Humanizer the draft and
relevant writing samples. A successful edit is evidence about that text; it does
not automatically turn every editorial choice into a permanent preference.

## Install only what you choose

For portable skills, use the upstream repository and the skill's exact `name`
from its frontmatter. For example, these are separate choices, not a setup script
to run in full:

```sh
npx skills add Leonxlnx/taste-skill --skill design-taste-frontend
npx skills add anthropics/skills --skill frontend-design
npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices
npx skills add vercel-labs/agent-skills --skill web-design-guidelines
npx skills add blader/humanizer --skill humanizer
npx skills add vercel-labs/skills --skill find-skills
```

The [skills CLI documentation](https://github.com/vercel-labs/skills) describes
client and scope selection. Check an existing installation before adding another
copy. For Superpowers and agent-browser, follow their own setup guides linked
above: copying a skill file alone may leave out required workflow or runtime
components. The commands here were source-checked, not installation-tested as a bundle.

## Keep one agreement across the tools

Give a specialist only the confirmed criteria relevant to its task. Keep its
house style and scores separate from your preferences. If ALIGNS.md already says
that opening text must be visible immediately, a design skill should work within
that constraint without asking the same question again.

If a specialist check disagrees with an authorized exception, report the actual
result and the exception. Do not change the agreement to manufacture a pass.
Ask only about important choices the current request and agreement leave open.
Permissions and the applicable instruction hierarchy still apply.

A request you can reuse:

> Use the relevant criteria in ALIGNS.md for this task, then apply the specialist
> skill we selected. Reuse decisions we have already made. Ask only about important
> unresolved conflicts, and report any exceptions to the specialist's checks.

See [using align with specialist skills](usage.md#use-align-with-specialist-skills)
for how the maintained method handles this handoff. These are independent projects;
being listed here does not imply an integration or endorsement by their authors.
