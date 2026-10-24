#!/usr/bin/env python3
"""Scan a clean source export using the upstream action runner, without policy overrides.

Run with the Python environment containing plugin-scanner==3.0.123.
Raw reports stay in ignored audit-input/. --revision scans a Git revision;
otherwise include tracked files plus nonignored new files from the worktree.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--revision')
    parser.add_argument('--output', default='audit-input/local-after.json')
    args = parser.parse_args()
    output = (ROOT / args.output).resolve()
    if not output.is_relative_to(ROOT / 'audit-input'):
        parser.error('Reports must stay inside audit-input/')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='master-skills-hol-') as temp:
        target = Path(temp)
        if args.revision:
            archive = subprocess.check_output(['git', 'archive', '--format=zip', args.revision], cwd=ROOT)
            with zipfile.ZipFile(io.BytesIO(archive)) as zipped:
                for entry in zipped.infolist():
                    if not (target / entry.filename).resolve().is_relative_to(target):
                        raise ValueError('Unsafe archive path')
                zipped.extractall(target)
        else:
            names = subprocess.check_output(
                ['git', 'ls-files', '-co', '--exclude-standard', '-z'], cwd=ROOT
            ).decode('utf-8').split('\0')
            for name in set(filter(None, names)):
                source = ROOT / name
                if source.is_symlink():
                    raise ValueError('Symlinks require explicit export review: ' + name)
                if not source.is_file():
                    continue
                destination = target / name
                if not destination.resolve().is_relative_to(target):
                    raise ValueError('Unsafe source path')
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, destination)
        env = dict(os.environ)
        env.update(MODE='scan', PLUGIN_DIR=str(target), FORMAT='json', OUTPUT='',
                   PROFILE='default', CONFIG='', BASELINE='', TRUST_REPOSITORY_POLICY='false',
                   ONLINE='false', MIN_SCORE='80', FAIL_ON='none', CISCO_SCAN='auto',
                   CISCO_POLICY='balanced', UPLOAD_SARIF='false', WRITE_STEP_SUMMARY='false',
                   SUBMISSION_ENABLED='false', PR_COMMENT='off', PYTHONNOUSERSITE='1',
                   PYTHONSAFEPATH='1', PYTHONDONTWRITEBYTECODE='1')
        inventory = {p.relative_to(target).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in target.rglob('*') if p.is_file()}
        output.with_suffix('.inventory.json').write_text(json.dumps(inventory, indent=2), encoding='utf-8')
        # Use the scanner's supported stdout report transport. Capturing it also
        # keeps possible credential matches out of terminal logs. This avoids
        # Windows directory-lock incompatibilities in the scanner's file writer.
        result = subprocess.run([sys.executable, '-P', '-m', 'codex_plugin_scanner.action_runner'],
                                cwd=target, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        report = json.loads(result.stdout.decode('utf-8'))
        output.write_text(json.dumps(report, indent=2), encoding='utf-8')
        print(f'Scanner exit {result.returncode}; report saved privately to {output.relative_to(ROOT)}')
        return result.returncode


if __name__ == '__main__':
    raise SystemExit(main())
