#!/usr/bin/env python3
"""Prepare a fresh, pinned Linux build tree. Never imports a router backup."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import urllib.request

REPO = Path(__file__).resolve().parents[1]

def run(*args, cwd=None):
    subprocess.run(args, cwd=cwd, check=True)

def copy_tree(src, dst):
    shutil.copytree(src, dst, dirs_exist_ok=True)

def materialize_board_data(tree, lock):
    data = lock['board_data']
    base = data['url'].replace('https://github.com/', 'https://raw.githubusercontent.com/')
    def ie(tag, payload):
        return struct.pack('<II', tag, len(payload)) + payload + b'\0' * (-len(payload) % 4)
    magic = b'QCA-ATH11K-BOARD\0'
    for radio, spec in data['radios'].items():
        url = f"{base}/{data['commit']}/{data['prefix']}{spec['file']}"
        with urllib.request.urlopen(url, timeout=90) as response:
            payload = response.read()
        if len(payload) != 131072 or hashlib.sha256(payload).hexdigest() != spec['sha256']:
            raise RuntimeError(f'Board data verification failed: {radio}')
        # Both radios use the AHB naming convention in this multi-PD platform.
        bus = 'ahb'
        name = f"bus={bus},qmi-chip-id=0,qmi-board-id={spec['board_id']}".encode()
        board = magic + b'\0' * (-len(magic) % 4) + ie(0, ie(0, name) + ie(1, payload))
        target = tree / f'files/lib/firmware/ath11k/{radio}/hw1.0/board-2.bin'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(board)

def fix_feed_cycles(tree):
    # These upstream alternatives target mutually exclusive SoCs. The conflict
    # creates a Kconfig selection cycle via luci-app-nss, so omit that redundant edge.
    makefile = tree / 'package/nss/nss-tools/Makefile'
    text = makefile.read_text()
    needle = '  CONFLICTS:=nss-tools\n'
    if needle not in text:
        raise RuntimeError('Unexpected nss-tools Makefile; review dependency fix')
    text = text.replace(needle, '')
    needle = '  DEPENDS:=+luci-base +TARGET_qualcommax_ipq50xx:nss-tools-dwmac \\\n\t+!TARGET_qualcommax_ipq50xx:nss-tools\n'
    if needle not in text:
        raise RuntimeError('Unexpected luci-app-nss dependency definition')
    # The profile explicitly selects nss-tools-dwmac. Avoid OpenWrt's recursive
    # dependency expansion through both mutually exclusive runtime alternatives.
    text = text.replace(needle, '  DEPENDS:=+luci-base @(TARGET_qualcommax_ipq50xx)\n')
    makefile.write_text(text)
    # Unselected packages with existing feed Kconfig cycles are not part of this profile.
    for path in ('package/feeds/luci/luci-app-weechat',
                 'package/feeds/packages/weechat',
                 'package/feeds/packages/squeezelite'):
        link = tree / path
        if link.is_symlink():
            link.unlink()

def overlay_modes(tree):
    for root in ('files', 'source-overlay'):
        for src in (REPO / root).rglob('*'):
            if not src.is_file():
                continue
            dst = tree / (src.relative_to(REPO / 'source-overlay') if root == 'source-overlay'
                          else src.relative_to(REPO))
            if src.read_bytes().startswith(b'#!'):
                dst.chmod(0o755)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default=str(REPO / 'build/openwrt'))
    args = parser.parse_args()
    # WSL appends Windows paths containing spaces/parentheses; OpenWrt's
    # recursive make prerequisite commands cannot safely consume those entries.
    os.environ['PATH'] = ':'.join(p for p in os.environ.get('PATH', '').split(':')
                                  if p and not p.startswith('/mnt/') and ' ' not in p)
    tree = Path(args.output).resolve()
    if tree.exists():
        parser.error('Output already exists; use a new, empty location')
    lock = json.loads((REPO / 'sources.lock.json').read_text())
    tree.parent.mkdir(parents=True, exist_ok=True)
    run('git', 'init', str(tree))
    run('git', 'remote', 'add', 'origin', lock['openwrt']['url'], cwd=tree)
    run('git', 'fetch', '--depth', '1', 'origin', lock['openwrt']['commit'], cwd=tree)
    run('git', 'checkout', '--detach', 'FETCH_HEAD', cwd=tree)
    for patch in sorted((REPO / 'patches/openwrt').glob('*.patch')):
        run('git', 'apply', str(patch), cwd=tree)
    copy_tree(REPO / 'source-overlay', tree)
    # No video feed: it is unused by this device and has an upstream Qt dependency cycle.
    feeds = ''.join(f"src-git {name} {spec['url']}^{spec['commit']}\n"
                    for name, spec in lock['feeds'].items())
    (tree / 'feeds.conf').write_text(feeds)
    run('./scripts/feeds', 'update', '-a', cwd=tree)
    for name, spec in lock['feeds'].items():
        head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=tree / 'feeds' / name).decode().strip()
        if head != spec['commit']:
            raise RuntimeError(f'Feed pin mismatch: {name}')
    for patch in sorted((REPO / 'patches/packages').glob('*.patch')):
        run('git', 'apply', str(patch), cwd=tree / 'feeds/packages')
    copy_tree(REPO / 'feed-overlay', tree / 'feeds')
    run('./scripts/feeds', 'install', '-a', cwd=tree)
    fix_feed_cycles(tree)
    copy_tree(REPO / 'files', tree / 'files')
    materialize_board_data(tree, lock)
    overlay_modes(tree)
    shutil.copyfile(REPO / 'config/ax3000cv2.config', tree / '.config')
    run('make', 'defconfig', cwd=tree)
    print(f'Prepared {tree}. See docs/BUILD.md for build commands.')

if __name__ == '__main__':
    main()
