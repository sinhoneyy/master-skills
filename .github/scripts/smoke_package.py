#!/usr/bin/env python3
"""Validate npm's pack file inventory, and install from an isolated local tarball."""
import json
import os
import pathlib
import subprocess
import tarfile
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
SKILL = "skills/product-design-harness/"
EXPECTED = 91


def run(*args, cwd=ROOT):
    return subprocess.run(args, cwd=cwd, check=True, text=True, stdout=subprocess.PIPE).stdout


def main():
    with tempfile.TemporaryDirectory(prefix="master-skills-package-") as temp:
        target = pathlib.Path(temp)
        manifest = json.loads(run("npm", "pack", "--dry-run", "--json"))
        files = {item["path"] for item in manifest[0]["files"]}
        assert {"bin/cli.mjs", "skills_index.json", "CREDITS.md"}.issubset(files)
        on_disk = ROOT / SKILL
        if on_disk.exists():
            expected = {SKILL + str(path.relative_to(on_disk)).replace(os.sep, "/") for path in on_disk.rglob("*") if path.is_file()}
            included = {p for p in files if p.startswith(SKILL)}
            assert expected == included, f"Missing from npm pack: {sorted(expected - included)}"
            assert SKILL + "LICENSE" in included
            assert len(included) == EXPECTED, f"Expected {EXPECTED} harness files, got {len(included)}"
        output = run("npm", "pack", "--json", "--pack-destination", str(target))
        archive = target / json.loads(output)[0]["filename"]
        with tarfile.open(archive, "r:gz") as tar:
            # Extract into isolated temporary destination; reject traversal.
            for m in tar.getmembers():
                dest = (target / m.name).resolve()
                if not dest.is_relative_to(target.resolve()) or m.issym() or m.islnk():
                    raise ValueError("Unsafe npm tar member " + m.name)
            tar.extractall(target, filter="data")
        packed = target / "package"
        index = json.loads((packed / "skills_index.json").read_text())
        install = target / "installed"
        if on_disk.exists():
            # Copies the general category as data; no skill executes.
            run("node", "bin/cli.mjs", "--path", str(install), "--category", "general", cwd=packed)
            copied = install / "product-design-harness"
            assert copied.is_dir()
            original = {str(x.relative_to(on_disk)): x.read_bytes() for x in on_disk.rglob("*") if x.is_file()}
            actual = {str(x.relative_to(copied)): x.read_bytes() for x in copied.rglob("*") if x.is_file()}
            assert original == actual, "Installed skill differs from repository source"
        print(f"PASS npm tarball inventory; manifest count {index['skill_count']}; isolated CLI install")


if __name__ == "__main__":
    main()
