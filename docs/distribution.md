# Distribution

This page tracks distribution work, not changes to user alignment criteria.
Submission, acceptance, search visibility, and installation are distinct states.
Do not describe a pending or unverified listing as published.

## Source

- Website: https://aligns.md
- Repository: https://github.com/hmmhmmhm/aligns.md
- Skill: https://github.com/hmmhmmhm/aligns.md/tree/main/skills/align
- Name: `align`
- License: MIT
- Summary: Align an agent's decisions with a user's project expectations and keep the agreement current without repeated interviews.

## Service status

The repository was renamed to `ALIGNS.md` on 2026-10-17. Skills.sh, askill,
Agent Skill Hub, and Skillstore were checked again on 2026-11-02 against source
commit `43f2c30522085600883f4438ac2231ea076e87e2`, method version `0.11.0`.
Other rows retain their earlier evidence and are not newly verified.
The URLs below preserve actual receipts. A renamed listing or accepted refresh
does not prove that its downloadable files have changed.
The maintained source now includes native Codex and Claude Code marketplaces.
These custom marketplaces are separate from official platform directory listings.

| Service | Route | Current evidence |
| --- | --- | --- |
| GitHub | Public source and release | Public source and the installable skill are available. Release packages include a skill ZIP and SHA-256 checksum. See the [latest release](https://github.com/hmmhmmhm/aligns.md/releases/latest). |
| [skills.sh](https://skills.sh/docs/faq) | Installation telemetry and directory indexing | The [current page](https://skills.sh/hmmhmmhm/aligns.md/align) works, and the old URL redirects to it. On 2026-11-02, its [download snapshot](https://skills.sh/api/download/hmmhmmhm/aligns.md/align) still contained method `0.6.1` and 12 files, compared with `0.11.0` and 25 tracked files in the source. No supported publisher refresh endpoint was found. The directory snapshot remains stale. This is separate from direct installation from GitHub. |
| [askill](https://askill.sh/submit) | Submit GitHub URL | Reindexed the renamed source on 2026-11-02. The [current listing](https://askill.sh/skills/704733) shows method `0.11.0` and the eight alignment paths. The [legacy listing](https://askill.sh/skills/704509) was also submitted for reindexing, but its public page still showed the initial content at the follow-up check. Use the current listing. Supporting-file download completeness was not verified. |
| [OpenAgentSkill](https://www.openagentskill.com/submit) | Public submission queue | Submission accepted and marked public. [Listing](https://www.openagentskill.com/skills/hmmhmmhm-align-md-align) verified; static checks passed, not AI-reviewed. |
| [Agent Skill Hub](https://doc.agentskillhub.dev/guide/publishing) | Source refresh API | Refreshed the existing `hmmhmmhm/align` record on 2026-11-02 through the documented `refresh-from-source` endpoint. The [public record](https://agentskillhub.dev/api/v1/u/hmmhmmhm/skills/align) reports version `2026.11.02` and source commit `43f2c30`. Its SKILL.md matches the maintained source, and all 25 tracked skill paths are present in the manifest. Supporting-file contents were not individually compared. |
| [SkillsMP](https://skillsmp.com/about) | Public GitHub indexing | Public indexing documented; no self-service submission route found in the inspected site and documentation. A live search for the former `hmmhmmhm/align.md` returned no matches; listing is not yet verified. |
| [Skills Directory](https://skillsdir.dev/add) | GitHub issue submission | The site's linked repository and issue template both return 404. Submission currently unavailable. |
| [ClawHub](https://docs.openclaw.ai/clawhub) | Authenticated skill publication | CLI dry-run accepted `align-md` v0.1.0 with all three package files. The device authorization expired without login; a fresh owner authorization is required. Dry-run is not publication. |
| [Skillstore](https://skillstore.io/submit) | Submit GitHub URL for audit and review | The [existing listing](https://skillstore.io/skills/hmmhmmhm-align) is public, and [registration PR #3749](https://github.com/aiskillstore/marketplace/pull/3749) was merged on 2026-10-12. It still serves the initial snapshot. The [2026-11-02 refresh submission](https://skillstore.io/ko/submissions/220241ba-a49c-49ed-ae1b-f3eca9c223cb) failed before security review because the published source identity uses the former repository name. [Workflow evidence](https://github.com/aiskillstore/marketplace/actions/runs/41374403057). In [issue #4038](https://github.com/aiskillstore/marketplace/issues/4038#issuecomment-6576959897), the maintainer confirmed on 2026-11-02 that source migration is unsupported and closed the issue. The final instruction is to request removal of the old listing, wait for removal, then submit the renamed source. The 2026-11-05 attempt stopped at GitHub sign-in. No removal request or replacement submission was completed. Latest-version publication remains unconfirmed. |
| [Skills Directory](https://www.skillsdirectory.com/submit) | Authenticated submission | The submission route requires sign-in. The owner login request timed out with the sign-in page unchanged; no submission made. This is a different service from `skillsdir.dev`. |

## Platform directories

The [Claude directory documentation](https://support.claude.com/en/articles/14328846-browse-skills-connectors-and-plugins-in-one-directory)
describes installing directory skills and publishing within an organization.
It does not establish an open, public self-service listing route for this skill.
Do not treat a personal installation or an organization-only publication as
public distribution. No official Claude directory listing is claimed.

## Native installation and updates

Use the [installation guide](usage.md) for the Codex plugin, Claude Code plugin,
or portable skills CLI. A plugin version is the alignment method version, not
the project agreement version. Directory snapshots may lag behind GitHub.

## Maintaining distribution

Publish source changes first, then refresh services that snapshot the skill.
Keep actual receipt or listing URLs and distinguish delayed indexing from
confirmed search visibility. Do not create duplicate submissions to simulate
adoption or inflate installation counts. Expand this list as relevant, active
distribution services are discovered; universal coverage is not assumed.
