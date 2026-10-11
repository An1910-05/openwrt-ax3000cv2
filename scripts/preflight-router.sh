#!/bin/sh
# Read-only. No flash, boot environment or configuration is changed.
set -eu
EXPECTED=57f426f8cbf49731e727f12bce5258facacd3b6007888fe1b1f0df1f1989735c
BOARD=$(cat /tmp/sysinfo/board_name)
[ "$BOARD" = 'fpt,wf810df' ] || { echo 'STOP: board mismatch'; exit 1; }
grep -q '^mtd20: 0f300000 .*"rootfs"' /proc/mtd || { echo 'STOP: rootfs layout mismatch'; exit 1; }
grep -q '^mtd12: .*"0:APPSBL_1"' /proc/mtd || { echo 'STOP: bootloader layout mismatch'; exit 1; }
ACTUAL=$(sha256sum /dev/mtd12 | cut -d ' ' -f1)
[ "$ACTUAL" = "$EXPECTED" ] || { echo 'STOP: bootloader differs from tested revision'; exit 1; }
echo 'Board, rootfs layout and tested APPSBL_1 fingerprint match.'
echo 'This does not verify which bootloader slot is active. Confirm it using UART.'
echo 'No changes made. Read docs/INSTALL.md before continuing.'
if command -v fw_printenv >/dev/null 2>&1; then
    fw_printenv bootcmd bootowrt bootargs
fi
