#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
"""Collect only upgrade/RAM images and non-private source metadata."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

repo = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--tree', required=True)
parser.add_argument('--output', default=str(repo / 'artifacts'))
parser.add_argument('--compiler', default='OpenWrt internal toolchain')
args = parser.parse_args()
tree, out = Path(args.tree).resolve(), Path(args.output).resolve()
out.mkdir(parents=True, exist_ok=True)
if any(out.iterdir()):
    parser.error('Output must be empty')
images = tree / 'bin/targets/qualcommax/ipq50xx'
for pattern, name in (
    ('*wf810df*sysupgrade.bin', 'ax3000cv2-nss-sysupgrade.bin'),
    ('*wf810df*initramfs*.itb', 'ax3000cv2-nss-initramfs.itb'),
    ('*wf810df.manifest', 'packages.manifest'),
):
    matches = list(images.glob(pattern))
    if len(matches) != 1:
        raise RuntimeError(f'Expected exactly one {pattern}, got {len(matches)}')
    shutil.copyfile(matches[0], out / name)
shutil.copyfile(repo / 'sources.lock.json', out / 'sources.lock.json')
shutil.copyfile(repo / 'config/ax3000cv2.config', out / 'ax3000cv2.config')
commit = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD']).decode().strip()
manifest = {
    'device': 'AX3000CV2 / WF810DF', 'compatible': 'fpt,wf810df',
    'recipe_commit': commit, 'compiler': args.compiler,
    'hardware_boot_tested': False, 'status': 'community-preview',
    'warning': 'Public board data and clean defaults differ from the private reference image.',
    'images': {},
}
for path in sorted(out.iterdir()):
    manifest['images'][path.name] = {'size': path.stat().st_size,
                                    'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
(out / 'release-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
sums = ''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n'
               for p in sorted(out.iterdir()) if p.is_file())
(out / 'sha256sums').write_text(sums)
print(f'Collected {len(list(out.iterdir()))} files in {out}. Inspect images before uploading.')
