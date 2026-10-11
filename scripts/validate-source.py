#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
"""Check publishable source files, shell syntax and local Markdown links."""
from pathlib import Path
import re
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
errors = []
count = 0
for path in root.rglob('*'):
    relative = path.relative_to(root)
    if any(part in ('.git', 'build', 'artifacts', '.cache', '__pycache__') for part in relative.parts):
        continue
    if not path.is_file():
        continue
    count += 1
    data = path.read_bytes()
    if path.name in ('shadow', 'authorized_keys', 'id_ed25519', 'id_rsa'):
        errors.append(f'Private file: {relative}')
    # Construct the marker so this scanner does not match itself.
    if re.search(b'-----BEGIN [A-Z ]*' + b'PRIVATE KEY-----', data):
        errors.append(f'Private key material: {relative}')
    is_png = path.suffix == '.png' and data.startswith(b'\x89PNG\r\n\x1a\n')
    if b'\r\n' in data and path.suffix != '.bin' and not is_png:
        errors.append(f'CRLF: {relative}')
    if data.startswith(b'#!/bin/sh') or path.suffix == '.sh':
        result = subprocess.run(['sh', '-n', str(path)], capture_output=True, text=True)
        if result.returncode:
            errors.append(f'Shell syntax: {relative}: {result.stderr.strip()}')
    if path.suffix == '.md':
        for link in re.findall(r'\]\(([^)]+)\)', data.decode('utf-8')):
            if '://' in link or link.startswith('#'):
                continue
            target = link.split('#', 1)[0]
            if target and not (path.parent / target).exists():
                errors.append(f'Broken link: {relative}: {target}')
if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f'Validated {count} source files: shell syntax, local links, LF and private-key scan.')
