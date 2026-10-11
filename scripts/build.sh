#!/bin/sh
set -eu
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
TREE=${1:-build/openwrt}
JOBS=${JOBS:-$(nproc)}
cd "$TREE"
make download -j"$JOBS"
make -j"$JOBS" V=s
