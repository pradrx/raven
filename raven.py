"""raven — local LeetCode-style harness.

Usage: python raven.py questions/<name>.py

Pairs a question file with tests/<name>.json, imports it, calls
`solve(*case["args"])` for each case, and reports pass/fail.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import uuid
from pathlib import Path


def derive_test_path(question_path: Path) -> Path:
    parts = list(question_path.parts)
    try:
        i = len(parts) - 1 - parts[::-1].index("questions")
    except ValueError:
        raise SystemExit(
            f"error: question path must live under a 'questions/' directory: {question_path}"
        )
    parts[i] = "tests"
    return Path(*parts).with_suffix(".json")


def load_question_module(question_path: Path):
    mod_name = f"raven_q_{uuid.uuid4().hex}"
    spec = importlib.util.spec_from_file_location(mod_name, question_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"error: could not load question file: {question_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fmt(value) -> str:
    try:
        return repr(value)
    except Exception:
        return "<unrepr-able>"


def run(question_path: Path) -> int:
    if not question_path.is_file():
        raise SystemExit(f"error: no such question file: {question_path}")

    test_path = derive_test_path(question_path)
    if not test_path.is_file():
        raise SystemExit(f"error: no test file found at {test_path}")

    with test_path.open() as f:
        data = json.load(f)
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise SystemExit(f"error: {test_path} must contain a non-empty 'cases' list")

    module = load_question_module(question_path)
    solve = getattr(module, "solve", None)
    if not callable(solve):
        raise SystemExit(f"error: {question_path} must define a callable `solve`")

    print(f"running {len(cases)} case(s) for {question_path.name}")
    passed = 0
    for i, case in enumerate(cases, 1):
        args = case.get("args", [])
        expected = case.get("expected")
        try:
            actual = solve(*args)
        except Exception as e:
            print(f"  [{i}] FAIL  args={fmt(args)}  raised {type(e).__name__}: {e}")
            continue

        if actual == expected:
            print(f"  [{i}] PASS  args={fmt(args)}")
            passed += 1
        else:
            print(
                f"  [{i}] FAIL  args={fmt(args)}\n"
                f"        expected={fmt(expected)}\n"
                f"        actual  ={fmt(actual)}"
            )

    total = len(cases)
    print(f"\n{passed}/{total} passed")
    return 0 if passed == total else 1


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        raise SystemExit("usage: python raven.py <path/to/question.py>")
    return run(Path(argv[1]))


if __name__ == "__main__":
    sys.exit(main(sys.argv))
