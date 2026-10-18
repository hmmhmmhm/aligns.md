<p align="center">
  <img src="assets/aligns-header.png" alt="ALIGNS.md on a yellow and cyan background with a connected node diagram" width="100%">
</p>

<h1 align="center">ALIGNS.md</h1>

<p align="center">
  <strong lang="en">English</strong> · <a href="docs/translated-readme/ko.md" lang="ko">한국어</a> · <a href="docs/translated-readme/ja.md" lang="ja">日本語</a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
  <a href="https://github.com/hmmhmmhm/aligns.md/stargazers"><img src="assets/badges/github-star.svg" alt="GitHub stars"></a>
  <a href="#install-align"><img src="https://img.shields.io/badge/Format-Markdown-222222.svg?logo=markdown" alt="Format: Markdown"></a>
  <a href="https://skills.sh/hmmhmmhm/aligns.md/align"><img src="assets/badges/skills-sh.svg" alt="Available on skills.sh"></a>
</p>

## Define what good means

ALIGNS.md records the goals and trade-offs you want your agent to use. The **align** skill helps you agree on those criteria and revisit them as the work changes.

<p align="center">
  <img src="assets/define-what-good-means.png" alt="Several paths converge on a shared reference point" width="100%">
</p>

## Keep expectations separate

Keep personal criteria in ALIGNS.md and the reusable alignment method in the skill. Connect the agreement through your primary agent instruction file, such as AGENTS.md or CLAUDE.md. Use Git history when available. Updating the skill never rewrites your agreement.

Use specialist skills within those criteria. Their default style does not become your personal preference; choices already settled in ALIGNS.md do not need another question. See [recommended companion skills](docs/recommended-skills.md) for development, design, review and writing.

<p align="center">
  <img src="assets/keep-expectations-separate.png" alt="Three distinct connected panels represent execution, instructions, and expectations" width="100%">
</p>

## Spend less effort explaining your preferences

The criteria you agree on carry over to the next task. Your agent uses the preferences it already knows, so you spend less time explaining how you want things done or making each choice yourself.

When a result misses what you had in mind, revise the criteria together and use them in the next task.

[Results and method](RETENTION_BENCHMARK.md)

<p align="center">
  <a href="RETENTION_BENCHMARK.md"><img src="assets/benchmarks/retention-comparison.svg" alt="Synthetic benchmark: nine task replies with generic instructions versus zero with saved preferences and align; four assumed setup replies included separately; final fit 12 of 12 in both conditions" width="100%"></a>
</p>

## Continuous self-alignment

Self-alignment means clarifying your preferences and decision criteria with your agent, then checking its work against them.

Return to alignment when an important decision misses your intent, repeated corrections reveal a missing criterion, or you are unsure what to do next. You can also review selected PR feedback and accessible project conversations to find recurring criteria, called taste invariants, with their scope and exceptions. Choose recent or full history after seeing the estimated time. Before a long autonomous run, rehearse a few hypothetical choices. Clear errors get fixed directly; settled questions stay settled.

Brief requests work too. The agent checks existing context, then asks only about gaps that would materially change the result. You can agree on when it should ask and when it should proceed. Only confirmed lasting preferences go into ALIGNS.md.

<p align="center">
  <img src="assets/continuous-self-alignment.png" alt="A path gradually corrects its deviations from a steady reference line" width="100%">
</p>

## Install align

Paste this request into your agent:

```text
Set up the maintained align skill from https://github.com/hmmhmmhm/aligns.md using its current installation guide. Check my existing setup, use the supported route for my primary CLI, connect ALIGNS.md to this project, and configure supported method updates. Preserve existing instructions and my confirmed criteria; ask only about unresolved choices.
```

Or install it directly:

```sh
npx skills add hmmhmmhm/aligns.md --skill align
```

Then ask: **Let's do a self-alignment check for this project.** No command or exact phrase is required.

[Installation, updates and the eight starting points](docs/usage.md)

## For teams

Prepare reviewed decisions from code reviews and agent conversations as training data for your coding agent. Your team handles training and evaluation.

[MLOps and team adoption brief](docs/team-mlops-brief.md) · [Manual submission guide](docs/team-training-data.md)

## Add the badge to your project

Use this badge in your README if your project uses ALIGNS.md. Ask the agent to add it or choose option 7 when offered. The agent offers this option only when the badge is missing. You can also copy the Markdown below.

[![Uses ALIGNS.md](assets/badges/uses-aligns.svg)](https://github.com/hmmhmmhm/aligns.md)

```markdown
[![Uses ALIGNS.md](https://raw.githubusercontent.com/hmmhmmhm/aligns.md/main/assets/badges/uses-aligns.svg)](https://github.com/hmmhmmhm/aligns.md)
```

## License

[MIT](LICENSE). Copyright (c) 2026 hmmhmmhm.

<p align="center">
  <img src="assets/aligns-footer.png" alt="ALIGNS.md on a green background with overlapping coordinate grids" width="100%">
</p>
