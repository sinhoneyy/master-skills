#!/usr/bin/env python3
"""Validate skills_index.json against the on-disk skills/ tree.

Standard-library only. Exits non-zero (failing CI) on any inconsistency.
"""

from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INDEX = os.path.join(ROOT, "skills_index.json")

errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def main() -> int:
    if not os.path.isfile(INDEX):
        print("FAIL: skills_index.json not found at repo root")
        return 1

    try:
        with open(INDEX, encoding="utf-8") as fh:
            manifest = json.load(fh)
    except json.JSONDecodeError as exc:
        print(f"FAIL: skills_index.json is not valid JSON: {exc}")
        return 1

    # 1. required top-level keys
    required = {"name", "schemaVersion", "skill_count", "categories", "skills"}
    missing = required - manifest.keys()
    if missing:
        err(f"manifest is missing top-level keys: {sorted(missing)}")

    skills = manifest.get("skills", [])
    if not isinstance(skills, list):
        print("FAIL: 'skills' must be a list")
        return 1

    # 2. skill_count matches
    if manifest.get("skill_count") != len(skills):
        err(f"skill_count ({manifest.get('skill_count')}) != len(skills) ({len(skills)})")

    # 3. categories sum matches and counts are correct
    cat_counts: dict[str, int] = {}
    seen_ids: set[str] = set()

    for i, s in enumerate(skills):
        for field in ("id", "category", "path"):
            if not s.get(field):
                err(f"skills[{i}] missing required field '{field}'")
        sid = s.get("id", f"<index {i}>")

        # 4. unique ids
        if sid in seen_ids:
            err(f"duplicate skill id: {sid}")
        seen_ids.add(sid)

        cat = s.get("category", "")
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

        # 5. path exists and contains a SKILL.md
        rel = s.get("path", "")
        full = os.path.join(ROOT, rel.replace("/", os.sep))
        if not os.path.isdir(full):
            err(f"{sid}: path does not exist: {rel}")
        elif not any(f.lower() == "skill.md" for f in os.listdir(full)):
            err(f"{sid}: no SKILL.md in {rel}")

        # 6. trigger sanity
        trig = s.get("trigger", "")
        if trig and not trig.startswith("/"):
            err(f"{sid}: trigger should start with '/': {trig!r}")

    # 7. declared categories map matches computed counts
    declared = manifest.get("categories", {})
    if declared != dict(sorted(cat_counts.items())) and dict(declared) != cat_counts:
        # compare key/value sets order-independently
        for k, v in cat_counts.items():
            if declared.get(k) != v:
                err(f"category '{k}': manifest says {declared.get(k)}, tree has {v}")
        for k in declared:
            if k not in cat_counts:
                err(f"category '{k}' in manifest but no skills on disk")

    if errors:
        print(f"FAIL: {len(errors)} validation error(s):")
        for e in errors[:50]:
            print(f"  - {e}")
        if len(errors) > 50:
            print(f"  … and {len(errors) - 50} more")
        return 1

    print(f"OK: {len(skills)} skills, {len(cat_counts)} categories — manifest matches tree.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
