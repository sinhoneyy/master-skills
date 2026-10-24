#!/usr/bin/env python3
"""Refresh existing role-bundle skills from their canonical skills/ source.

Bundle membership and manifests are maintained separately. Never add or remove
skills here. Use --check in CI; pass skill IDs to limit a local refresh.
"""
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def sync(check=False, ids=()):
    differences = []
    for bundled in sorted((ROOT / 'plugins').glob('*/skills/*')):
        if not bundled.is_dir() or (ids and bundled.name not in ids):
            continue
        source = ROOT / 'skills' / bundled.name
        if not source.is_dir():
            raise ValueError(f'Missing canonical skill: {bundled.name}')
        source_files = {p.relative_to(source): p for p in source.rglob('*')
                        if p.is_file() and '__pycache__' not in p.parts
                        and p.suffix not in ('.pyc', '.pyo')}
        bundled_files = {p.relative_to(bundled): p for p in bundled.rglob('*')
                         if p.is_file() and '__pycache__' not in p.parts
                         and p.suffix not in ('.pyc', '.pyo')}
        extra = bundled_files.keys() - source_files.keys()
        if extra:
            raise ValueError(f'Unexpected bundle-only files in {bundled}: {sorted(extra)}')
        for rel, original in source_files.items():
            target = bundled / rel
            if not target.exists() or original.read_bytes() != target.read_bytes():
                differences.append(str(target.relative_to(ROOT)))
                if not check:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(original.read_bytes())
    print(f'{len(differences)} bundle file(s) ' + ('differ' if check else 'refreshed'))
    return bool(differences) if check else False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('ids', nargs='*')
    args = parser.parse_args()
    raise SystemExit(sync(args.check, args.ids))
