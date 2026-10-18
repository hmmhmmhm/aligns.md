# Connect the user's environment

At setup, inspect relevant existing files before proposing a layout. Ask which
CLI is primary and whether it is the current one only if context does not answer.
For equally used clients, propose AGENTS.md as the neutral canonical file. Record
the choice in ALIGNS.md; do not ask again until the user changes tools or evidence
shows the mapping is broken. A client answer completes a setup question, not the
whole request. Resume the pending authorized connection or alignment step in the
same turn; do not send the user back to a command or the start menu.

## Inspect, propose, connect, verify

- Codex normally uses AGENTS.md. Check AGENTS.override.md, parent and nested
  instructions and configured fallback names; an override can shadow AGENTS.md.
- Claude Code uses CLAUDE.md and may also load .claude/CLAUDE.md and scoped rules.
  Preserve those scopes and any tool-specific syntax.
- For other clients, confirm their actual entrypoint from local configuration
  or current official documentation. Do not assume every client reads Markdown
  filenames, supports symlinks, or understands Claude's @ imports.

Prefer the primary CLI's native file as the one source of shared instructions.
Append the short [alignment block](../assets/instruction-block.md) there. Connect
only additional clients the user actually uses. For example, with Codex primary
and no existing CLAUDE.md, `CLAUDE.md -> AGENTS.md` can share the instructions.
The inverse can work for a Claude-primary project. Use relative links inside the
project so the checkout stays portable. Link instruction files, never link
ALIGNS.md to the upstream skill or the source repository's personal agreement.

If another entrypoint already has distinct content, show what would need merging
and preserve it until that concrete replacement is authorized. Do not use force
symlink options, delete files, or flatten nested policies. For incompatible
formats or systems without usable symlinks, use a supported import or a short
pointer requiring the agent to read the canonical file. Keep tool-specific
settings where the tool expects them. Report fallback instead of claiming a
single file is automatically loaded everywhere.

## Required skills and actual discovery

In the canonical instruction file, require align for explicit alignment requests
and focused reviews. Preserve other skills the user or project already requires,
with their task scope. For each, record its invocation or host-visible name and a
trusted source or installation route when known. Do not turn companion-skill
recommendations into mandatory dependencies. Keep this setup information in the
instruction file; personal decision criteria remain in ALIGNS.md.

At setup, workspace/client changes, or a discovery failure:

1. Compare the session's actual starting directory with the target repository.
   A repository skill can be outside the discovery roots when the session starts
   in a parent workspace or a sibling directory. Check the client's current rules.
2. Check the current skill catalog, selector, or supported discovery diagnostic,
   allowing host namespaces. Verify relevant instruction overrides, disabled skills,
   and broken links. A valid SKILL.md or symlink proves only that files are present.
3. Load the required method when its task scope applies. Read only its relevant
   references and verify any resources needed for that task. Do not infer use
   from a listing, UI label, or an instruction saying the skill is mandatory.
4. If native discovery fails but the trusted local method and needed resources
   are readable, use them as an explicitly disclosed manual fallback. Otherwise
   report the affected step and continue independent work. Do not claim that
   alignment was completed with the skill when the method was never loaded.
5. Repair within the authorized scope using the existing route. Prefer correcting
   the starting directory or a scoped link over a duplicate or global installation.
   Keep a parent-workspace instruction pointer limited to the intended project.
   Verify again from the actual workspace; if a fresh session is needed, distinguish
   that result from what the current session has loaded.

During ordinary work, check applicable requirements once per session and reuse
that evidence unless the environment changes or loading fails. Do not run an
installation check, update, interview, or approval question on every task.
Instructions guide the agent; they do not install skills or create runtime hooks.

## Optional deterministic helper

Requires Python 3. Run from a known project path. Default mode only reports a plan.
The helper connects instruction files; it does not verify the client's skill catalog
or prove that the current session loaded a skill:

```sh
python3 <installed-skill>/scripts/connect_project.py --project <project> --primary codex --also claude-code
```

After the user's setup request authorizes these changes, add `--apply`. Omit
`--also` if only one client is used. The helper appends or refreshes one managed
block and creates only absent relative links. It refuses conflicting files,
symlinked canonical files, and shadowing instruction files rather than guessing
how to merge them. These need contextual review, not repeated retries.

Verify file targets and preserved content. Then check the target client's loaded
instructions, using a new session if needed. A valid filesystem link is not proof
that a client actually loaded it. Report precisely which checks were performed.
Do not modify global client configuration or install persistent hooks as a side
effect of a project-file connection. Plugin hooks belong to the chosen explicit
plugin installation and its documented lifecycle.

## Optional personal scope

A personal agreement can be connected through user-level instructions when the
user chooses personal setup. Follow [personal alignment](personal.md) for source
review, storage, private connection, and separate confirmation. Global skill
installation alone does not enable personal criteria. The project helper remains
project-scoped and must not be repurposed to configure a home directory.
