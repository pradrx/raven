---
description: Scaffold a spec file for a new raven question
---

You are scaffolding a markdown spec file the user will edit before running `/raven-new`. This command does NOT generate a question — it only creates `specs/<rel>.md` from a template.

**Read `AGENTS.md`** if not already in context — slug rules, the file layout, and the path-style argument convention are defined there.

The user invoked: `/raven-spec $ARGUMENTS`

Parse `$ARGUMENTS` as a single path-style token (`<folder>/<...>/<slug>` or just `<slug>`). Strip surrounding whitespace. Strip a leading `/` if present. If there are extra arguments after the path-style token, ignore them with a brief note ("Extra arguments after the slug were ignored.").

The **last** segment is the slug. Any preceding segments form the folder path (call it `<folder>` below; it may be empty for root-level questions). Reassembling: `<rel> = (folder + "/" if folder else "") + slug`.

## Steps

1. **Validate every segment.** Each segment (folders + slug) must match `[a-z][a-z0-9_-]*` (lowercase letter then letters/digits/underscores/hyphens). Reject `..`, `.`, empty segments (`//`), and trailing `/`. If anything fails, abort with the rule and an example.

2. **Check for slug collision across the entire tree.** Recursively walk `questions/`, `tests/`, and `specs/`. If any file with stem == slug exists anywhere (even at a different folder), abort with the offending path and: "Slug `<slug>` is already used at `<offending-path>`. Pick a different slug, or use `/raven-revise <slug> ...` to modify the existing one." Slugs are globally unique.

3. **Create folder if needed.** `mkdir -p specs/<folder>` (no-op if folder is empty).

4. **Create the spec file.** Read `templates/spec.md.template` and write its contents (verbatim, replacing `<slug>` placeholders with the actual slug if present in the title) to `specs/<rel>.md`. Do NOT overwrite — if step 2 already errored on the spec, you wouldn't reach here.

5. **Report success.** Print exactly one line: `Created specs/<rel>.md. Edit it, then run /raven-new <rel>.`

## Don'ts

- Don't fill in the spec content yourself. The point is the user writes the spec; you only scaffold.
- Don't generate `questions/<rel>.py` or `tests/<rel>.json`. That's `/raven-new`'s job.
- Don't overwrite an existing spec, question, or test anywhere in the tree.
