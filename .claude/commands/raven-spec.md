---
description: Scaffold a spec file for a new raven question
---

You are scaffolding a markdown spec file the user will edit before running `/raven-new`. This command does NOT generate a question — it only creates `specs/<slug>.md` from a template.

**Read `AGENTS.md`** if not already in context — slug rules and the file layout are defined there.

The user invoked: `/raven-spec $ARGUMENTS`

Parse `$ARGUMENTS` as a single slug token. Strip surrounding whitespace. If there are extra arguments after the slug, ignore them with a brief note ("Extra arguments after the slug were ignored.").

## Steps

1. **Validate the slug.** Lowercase snake_case, ASCII letters/digits/underscore, starts with a letter. If it doesn't match, abort with the slug rules and an example.

2. **Check for question collision.** If `questions/<slug>.py` or `tests/<slug>.json` already exists, abort with: "Question `<slug>` already exists. Pick a different slug, or use `/raven-revise <slug> ...` to modify it." Do NOT scaffold over an existing question.

3. **Check for spec collision.** If `specs/<slug>.md` already exists, abort with: "Spec already exists at `specs/<slug>.md` — edit it directly, or delete it first." Do NOT overwrite.

4. **Create the spec file.** Read `templates/spec.md.tpl` and write its contents (verbatim, replacing `<slug>` placeholders with the actual slug if present in the title) to `specs/<slug>.md`. Create the `specs/` directory if it doesn't exist.

5. **Report success.** Print exactly one line: `Created specs/<slug>.md. Edit it, then run /raven-new <slug>.`

## Don'ts

- Don't fill in the spec content yourself. The point is the user writes the spec; you only scaffold.
- Don't generate `questions/<slug>.py` or `tests/<slug>.json`. That's `/raven-new`'s job.
- Don't overwrite an existing spec or question.
