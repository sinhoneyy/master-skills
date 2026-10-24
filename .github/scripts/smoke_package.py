#!/usr/bin/env python3
"""Validate npm's pack inventory and perform an isolated local CLI install."""
import json
import pathlib
import shutil
import subprocess
import tarfile
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
SKILL = "skills/product-design-harness/"
NPM = shutil.which("npm") or "npm"


def run(*args, cwd=ROOT):
    return subprocess.run(args, cwd=cwd, check=True, text=True, stdout=subprocess.PIPE).stdout


def main():
    with tempfile.TemporaryDirectory(prefix="master-skills-package-") as temp:
        target = pathlib.Path(temp)
        manifest = json.loads(run(NPM, "pack", "--dry-run", "--json"))
        files = {item["path"] for item in manifest[0]["files"]}
        assert {"bin/cli.mjs", "skills_index.json", "CREDITS.md", "LICENSE", "SECURITY.md"}.issubset(files)
        assert not any(p.startswith("audit-input/") or "__pycache__" in p.split("/")
                       or p.endswith((".pyc", ".pyo", ".zip")) for p in files)
        on_disk = ROOT / SKILL
        if on_disk.exists():
            # Expected source is Git-tracked content. Python validation may have
            # produced untracked __pycache__/ .pyc files in the working tree.
            tracked = run("git", "ls-files", "-z", "--", SKILL).split("\0")
            expected = set(filter(None, tracked))
            assert expected, "Harness directory exists but no files are Git-tracked"
            included = {p for p in files if p.startswith(SKILL)}
            assert expected == included, (
                f"Missing from npm package: {sorted(expected - included)}; "
                f"unexpected packaged files: {sorted(included - expected)}"
            )
            assert SKILL + "LICENSE" in included
            print(f"PASS npm package includes exactly {len(expected)} tracked harness files")
        output = run(NPM, "pack", "--json", "--pack-destination", str(target))
        archive = target / json.loads(output)[0]["filename"]
        with tarfile.open(archive, "r:gz") as tar:
            for member in tar.getmembers():
                dest = (target / member.name).resolve()
                if not dest.is_relative_to(target.resolve()) or member.issym() or member.islnk():
                    raise ValueError("Unsafe npm tar member " + member.name)
            tar.extractall(target, filter="data")
        packed = target / "package"
        index = json.loads((packed / "skills_index.json").read_text())
        # Every supported host uses the same copying interface. Keep the tests
        # isolated from the real user's host configuration and credentials.
        for host in ("claude", "cursor", "gemini", "codex", "antigravity", "agy", "kiro", "opencode", "adal"):
            run("node", "bin/cli.mjs", "--" + host, "--path", str(target / host),
                "--category", "mobile", "--dry-run", cwd=packed)
        installed = target / "mobile-installed"
        run("node", "bin/cli.mjs", "--path", str(installed), "--category", "mobile", cwd=packed)
        for skill in (s for s in index["skills"] if s["category"] == "mobile"):
            original = packed / "skills" / skill["id"]
            copied = installed / skill["id"]
            expected_files = {p.relative_to(original).as_posix(): p.read_bytes()
                              for p in original.rglob("*") if p.is_file()}
            actual_files = {p.relative_to(copied).as_posix(): p.read_bytes()
                            for p in copied.rglob("*") if p.is_file()}
            assert expected_files == actual_files, skill["id"]
        if on_disk.exists():
            install = target / "installed"
            run("node", "bin/cli.mjs", "--path", str(install), "--category", "general", cwd=packed)
            copied = install / "product-design-harness"
            assert copied.is_dir()
            original = {
                path.removeprefix(SKILL): (ROOT / path).read_bytes()
                for path in expected
            }
            actual = {
                path.relative_to(copied).as_posix(): path.read_bytes()
                for path in copied.rglob("*") if path.is_file()
            }
            assert original == actual, (
                f"Installed skill differs from tracked source; "
                f"missing={sorted(original.keys() - actual.keys())}; "
                f"extra={sorted(actual.keys() - original.keys())}"
            )
        print(f"PASS npm tarball inventory; manifest count {index['skill_count']}; isolated CLI install")


if __name__ == "__main__":
    main()
