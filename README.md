# raven

A local LeetCode-style coding-prep harness with an **agent-first authoring workflow**. You ask a coding agent (Claude Code, etc.) for a problem; it generates a question file plus hidden test cases. You solve the question; raven's runner tells you which cases pass.

The split keeps the practice honest: the file you edit shows only the problem statement and a boilerplate function. The test data lives separately and you don't open it.

## Quickstart

```bash
git clone <this repo> raven && cd raven
./raven list
./raven run two_sum
```

The `raven` script is an executable Python file (no `.py` extension, shebang + `chmod +x`). For bare `raven` invocation anywhere, symlink it onto your `PATH`:

```bash
ln -s "$PWD/raven" /usr/local/bin/raven
```

Otherwise prefix with `./` when run from the repo root.

## Solving a question

```bash
./raven list                      # browse what's available, grouped by folder
./raven list --difficulty easy    # filter
./raven list --topic hash-map
./raven show two_sum              # problem statement + meta, no test cases
```

1. Open `questions/<rel>.py` (where `<rel>` is the slug, optionally prefixed by a folder path — see [Folders below](#folders)). The docstring describes the problem and gives a couple of illustrative examples (deliberately not the same as the hidden test inputs).
2. Fill in the body of `def solve(...)`.
3. Run `./raven run <slug>` to test. The runner finds the file by slug regardless of which folder it lives in.

```bash
./raven run two_sum
./raven run leetcode/easy/two_sum   # path-style also works
# → per-case PASS/FAIL with case names, summary, exit 0 on all-pass.
```

Exceptions in `solve` are reported as a failed case, not a crash, so a half-finished implementation still gives you useful output.

### Folders

Questions, tests, and specs can live at any depth under their respective roots — `questions/leetcode/easy/two_sum.py`, `questions/stripe/invoice_match_by_id.py`, etc. The three roots **mirror each other**: a question at `questions/<rel>.py` requires its test at `tests/<rel>.json` and (if present) spec at `specs/<rel>.md`.

Slugs are globally unique across the whole `questions/` tree, so the runner always finds a question by bare slug. Path-style is accepted as a typo guard.

## Authoring questions with a coding agent

The agent contract lives in [`AGENTS.md`](./AGENTS.md). Five slash commands under `.claude/commands/` operationalize it:

| Command | What it does |
| --- | --- |
| `/raven-spec <rel>` | Scaffold `specs/<rel>.md` from a structured template. `<rel>` is path-style (e.g. `leetcode/easy/two_sum`) or a bare slug for root-level questions. |
| `/raven-new <rel> [<description>]` | Generate a new question + tests pair at the mirrored path. Uses `specs/<rel>.md` if it exists, else the inline `<description>`. Validates inline (the agent writes a reference solution **in context**, runs it against every case, and **never writes it to disk**). Atomic rollback of the generated pair on failure (the spec file, if any, is left untouched). |
| `/raven-revise <locator> <change>` | Modify an existing pair (docstring, tests, or both). `<locator>` is bare slug or path-style. Re-validates; restores the originals if validation fails. |
| `/raven-check <locator>` | Re-validate an existing pair without changing it. Useful after a hand edit. |
| `/raven-hint <locator>` | Tiered hint (nudge → approach → partial code) escalating with each invocation. Forbidden from reading any file under `tests/`. |
| `/raven-grade <locator>` | Qualitative critique of your `solve` (style, complexity, edge cases). Also forbidden from reading any file under `tests/`. |

Example session in Claude Code, inline form (good for short asks):

```
/raven-new sliding_window_max a medium problem about the maximum
                              of every k-length window in an integer array
```

The agent reads `AGENTS.md`, writes `questions/sliding_window_max.py` and `tests/sliding_window_max.json`, generates a reference solution in its own context, runs it against every case, and only declares success when everything agrees. Then you edit `solve` and run `./raven run sliding_window_max`.

### Richer specs via a file

For problems where you want to be precise — listing constraints, naming specific edge cases the agent must cover, citing complexity targets — write the spec in your editor instead of the prompt:

```
/raven-spec sliding_window_max     # scaffolds specs/sliding_window_max.md
# edit the file in your editor — fill in Problem, Constraints,
# Edge cases to cover, Difficulty/topic hints, Notes
/raven-new sliding_window_max      # auto-detects the spec, generates the pair
```

Use the inline form for one-liners. Use the spec file when you'd otherwise be jamming three paragraphs into a chat prompt. The spec file is git-trackable as an audit trail of what you asked for; raven leaves it alone after generation, so you can commit it, gitignore the directory, or delete by hand.

If you get stuck:

```
/raven-hint sliding_window_max          # nudge first invocation
/raven-hint sliding_window_max          # approach next
/raven-hint sliding_window_max          # partial code last
```

When you've got something working:

```
/raven-grade sliding_window_max         # critique your solution, no peeking at tests
```

## Repo layout

```
raven/
├── raven                       # the runner CLI (run | list | show)
├── AGENTS.md                   # canonical contract for any agent generating problems
├── CLAUDE.md                   # thin pointer so Claude Code auto-loads the framing
├── questions/<rel>.py          # vanilla problem statement + boilerplate solve
├── tests/<rel>.json            # hidden cases + meta (difficulty, topics)
├── specs/<rel>.md              # optional: richer problem spec consumed by /raven-new
├── templates/                  # paste-able canonical shapes (question/tests/spec)
└── .claude/commands/*.md       # slash command definitions
```

`<rel>` is the relative path under each root, without extension. It's a bare slug for root-level questions (`two_sum`) or a folder/slug path for organized ones (`leetcode/easy/two_sum`, `stripe/invoice_match_by_id`). The three roots mirror each other on `<rel>`.

## Conventions worth knowing

- **Slugs are forever and globally unique.** Lowercase, `[a-z][a-z0-9_-]*`. Never reused, regardless of folder. `/raven-new` aborts on collision anywhere in the tree.
- **Mirror rule.** Question, test, and (if present) spec all live at the same `<rel>` under their respective roots.
- **`solve` is fixed.** Every question file defines a function called `solve` with positional arguments matching the JSON `args` order. No `kwargs`, no class wrappers (yet).
- **Strict equality.** A case passes iff `solve(*args) == expected`. No custom validators yet — problems with multiple valid outputs are out of scope for v1.
- **Reference solutions never live on disk.** Validation is agent-shaped: generate, run, discard. The repo stays clean and there's nothing to peek at.
- **`/raven-hint` and `/raven-grade` cannot read any file under `tests/`.** That's a hard rule in their command files. The hint and the grade come from the docstring and your `solve`, not from the test data.

The full agent contract — schema details, slug rules, case-coverage floor, validation rules, and don'ts — is in [`AGENTS.md`](./AGENTS.md). Read that before invoking any slash command.
