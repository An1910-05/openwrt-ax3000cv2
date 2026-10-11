# Recovery

**English** | [Tiếng Việt](vi/RECOVERY.md)

[Home](../README.md)

Keep the UART console connected at 115200 8N1 and capture logs from power-on. Do not interrupt an ongoing flash write to attempt recovery.

## Kernel or configuration fails to boot

If the kernel still boots, try OpenWrt failsafe first: restore a known-working configuration or reset the overlay. A reset removes user settings; the community build's password after reset is `admin`.

To boot from RAM, interrupt autoboot and enter U-Boot following the procedure for your revision. Run a TFTP server on an Ethernet-connected computer at `192.168.1.2`, after confirming that bootloader Ethernet has been initialized correctly. Example for a verified compatible bootloader:

```text
setenv ipaddr 192.168.1.1
setenv serverip 192.168.1.2
tftpboot 0x44000000 ax3000cv2-nss-initramfs.itb
bootm 0x44000000#config@1
```

These commands boot from RAM without saving the environment or writing firmware. Check the FIT configuration name with `dumpimage -l` first; substitute the actual name if it differs. Do not add `saveenv`, `nand erase`, `nand write` or a `go` command that does not match your bootloader.

Once the RAM image boots, collect logs, verify the layout with preflight and reinstall a known-working sysupgrade image using the [installation guide](INSTALL.md). Never restore ART from another device.

## LAN disappears after reboot

Check switch/PHY messages in `dmesg`, `ip link` and `ethtool` for `lan1`, `lan2`, `lan3` and `wan`. If PHYs are detected but all LAN links remain down, check the [bootloader Ethernet initialization](INSTALL.md#bootloader-and-lan-after-reboot). Bridge state or port LEDs alone do not establish the cause.

If Wi-Fi still works, use it to retrieve logs. Change one part at a time so that driver, bootloader and network configuration problems can be distinguished. Do not rewrite the entire NAND to fix a network configuration issue.
