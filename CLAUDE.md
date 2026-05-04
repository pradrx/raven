# Raven

Local LeetCode-style practice tool with an agent-first authoring workflow. Coding agents (you) generate questions and hidden test cases; the human user solves the questions and runs them with `./raven run <slug>`.

**The contract is in [`AGENTS.md`](./AGENTS.md). Read it before invoking any `/raven-*` slash command.** It defines the file layout, JSON schema, slug rules, validation contract (especially: reference solutions are generated in-context and never written to disk), and the things you must not do.

Slash commands live in `.claude/commands/`:
- `/raven-spec <rel>` — scaffold `specs/<rel>.md` for richer multi-line problem specs (`<rel>` is bare slug or path-style `<folder>/<slug>`)
- `/raven-new <rel> [<description>]` — create a question + tests pair at the mirrored path (uses `specs/<rel>.md` if present, else inline description)
- `/raven-revise <locator> <change>` — modify an existing pair
- `/raven-check <locator>` — re-validate a pair
- `/raven-hint <locator>` — tiered hint, no peeking at any file under `tests/`
- `/raven-grade <locator>` — critique the user's solve, no peeking at any file under `tests/`
