#!/usr/bin/env python3
"""Lint SKILL.md files changed in a pull request.

Standard-library only. Pass SKILL.md paths as arguments (the CI computes the
changed set). Writes a markdown report to lint-report.md and exits non-zero if
any file has a blocking error.

Checks (blocking ❌):
  - file has YAML frontmatter delimited by leading and closing '---'
  - frontmatter contains non-empty 'name' and 'description'
  - frontmatter lines are well-formed (key: value, list item, or continuation)
  - there is skill body content after the frontmatter

Checks (warnings ⚠️, non-blocking):
  - 'name' longer than 64 chars
  - 'description' shorter than 20 chars
  - file larger than 1 MB
"""

from __future__ import annotations

import os
import sys

MAX_NAME = 64
MIN_DESC = 20
MAX_BYTES = 1_000_000


def lint_one(path: str) -> tuple[list[str], list[str]]:
    errs: list[str] = []
    warns: list[str] = []

    if not os.path.isfile(path):
        return [f"file not found: {path}"], warns

    size = os.path.getsize(path)
    if size > MAX_BYTES:
        warns.append(f"file is large ({size // 1024} KB)")

    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()

    if not text.lstrip().startswith("---"):
        errs.append("missing opening '---' frontmatter delimiter")
        return errs, warns

    # locate frontmatter block
    start = text.index("---")
    end = text.find("\n---", start + 3)
    if end == -1:
        errs.append("missing closing '---' frontmatter delimiter")
        return errs, warns

    block = text[start + 3:end]
    body = text[end + 4:].strip()

    meta: dict[str, str] = {}
    last_key: str | None = None
    for raw in block.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        # list item or continuation under the previous key
        if line.lstrip().startswith("- ") or (line.startswith((" ", "\t")) and last_key):
            continue
        if ":" not in line:
            errs.append(f"malformed frontmatter line (no ':'): {line.strip()[:60]!r}")
            continue
        key, _, val = line.partition(":")
        key = key.strip().lower()
        meta[key] = val.strip().strip('"').strip("'")
        last_key = key

    name = meta.get("name", "")
    desc = meta.get("description", "")

    if not name:
        errs.append("frontmatter missing non-empty 'name'")
    elif len(name) > MAX_NAME:
        warns.append(f"'name' is long ({len(name)} chars)")

    if not desc:
        errs.append("frontmatter missing non-empty 'description'")
    elif len(desc) < MIN_DESC:
        warns.append(f"'description' is very short ({len(desc)} chars)")

    if not body:
        errs.append("no skill body content after frontmatter")

    return errs, warns


def main(argv: list[str]) -> int:
    files = [a for a in argv if a.strip()]
    lines: list[str] = ["## 🤖 Skill lint report", ""]
    total_err = 0
    total_warn = 0

    if not files:
        lines.append("No `SKILL.md` files changed in this PR — nothing to lint. ✅")
        _write("\n".join(lines))
        print("No SKILL.md files changed.")
        return 0

    lines.append(f"Linted **{len(files)}** changed `SKILL.md` file(s).\n")

    for path in files:
        errs, warns = lint_one(path)
        total_err += len(errs)
        total_warn += len(warns)
        if not errs and not warns:
            lines.append(f"- ✅ `{path}`")
            continue
        status = "❌" if errs else "⚠️"
        lines.append(f"- {status} `{path}`")
        for e in errs:
            lines.append(f"  - ❌ {e}")
        for w in warns:
            lines.append(f"  - ⚠️ {w}")

    lines.append("")
    if total_err:
        lines.append(f"**Result: {total_err} blocking error(s), {total_warn} warning(s).** "
                     "Please fix the ❌ items before merging.")
    else:
        lines.append(f"**Result: passed** ✅ ({total_warn} warning(s)).")

    _write("\n".join(lines))
    print("\n".join(lines))
    return 1 if total_err else 0


def _write(content: str) -> None:
    with open(os.path.join(os.getcwd(), "lint-report.md"), "w", encoding="utf-8") as fh:
        fh.write(content + "\n")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
