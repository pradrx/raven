# Raven

Local LeetCode-style practice tool with an agent-first authoring workflow. Coding agents (you) generate questions and hidden test cases; the human user solves the questions and runs them with `./raven run <slug>`.

**The contract is in [`AGENTS.md`](./AGENTS.md). Read it before invoking any `/raven-*` slash command.** It defines the file layout, JSON schema, slug rules, validation contract (especially: reference solutions are generated in-context and never written to disk), and the things you must not do.

Slash commands live in `.claude/commands/`:
- `/raven-spec <slug>` — scaffold `specs/<slug>.md` for richer multi-line problem specs
- `/raven-new <slug> [<description>]` — create a question + tests pair (uses `specs/<slug>.md` if present, else inline description)
- `/raven-revise <slug> <change>` — modify an existing pair
- `/raven-check <slug>` — re-validate a pair
- `/raven-hint <slug>` — tiered hint, no peeking at tests
- `/raven-grade <slug>` — critique the user's solve, no peeking at tests
