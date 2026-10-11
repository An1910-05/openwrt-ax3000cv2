# Installation

**English** | [Tiếng Việt](vi/INSTALL.md)

[Home](../README.md)

## Check your device

The target is `fpt,wf810df`, WF810DF / AX3000CV2 with 256 MiB NAND flash. The repository name omits the ISP name, while the device tree retains the actual compatible string to identify the hardware.

Prepare an Ethernet-connected computer and a **3.3 V UART** connection using GND/TX/RX at **115200 8N1**. Do not connect the USB-UART adapter's VCC to the router. If you use an ESP as a UART bridge, it needs separate bridge firmware matching your wiring; the router firmware in this repository is not for flashing onto an ESP.

Save configuration backups **to your computer**. Before migrating from stock firmware, also save partition dumps and the boot environment as required by the migration guide. Keep ART/calibration, account details and raw dumps private. Retain a known-working firmware image and UART access for recovery.

## Bootloader and LAN after reboot

On the reference device, the bootloader must run the vendor's Ethernet initializer before entering the kernel. Without this step, LAN links may disappear after reboot or a power cycle even when the driver detects all ports.

The reference device used:

```text
bootcmd=bootipq_owrt; go 0x4a9610b5; run bootowrt
```

The `go` address **depends on the exact bootloader version** and is not universal to AX3000CV2 devices. The verified `0:APPSBL_1` fingerprint is:

```text
57f426f8cbf49731e727f12bce5258facacd3b6007888fe1b1f0df1f1989735c
```

Copy the [preflight script](../scripts/preflight-router.sh) to `/tmp` on OpenWrt, then run `sh preflight-router.sh` from that directory. It only reads the board identity, partition layout and hash. If they differ, **stop** and do not use the `go` address above. A backup-slot hash does not prove which slot is executing; check UART logs and the bootloader procedure. This repository does not provide an automatic stock-firmware installer for every revision.

If compatible OpenWrt, `bootipq_owrt` and `bootowrt` are already present and `fw_printenv` reads a valid environment CRC, consider changing `bootcmd` only after identifying the running bootloader, saving the environment to your computer and understanding how to restore it. Do not copy another router's environment.

## Upgrading compatible OpenWrt

1. Read the release status. A preview that has not been boot-tested on hardware is not confirmed stable.
2. Download `*-sysupgrade.bin` and `sha256sums`; verify the SHA-256 checksum on your computer.
3. Run the preflight checks above. Confirm that UART and at least one LAN port work.
4. Create a configuration backup and download it to your computer. A clean installation is recommended when changing topology or NSS; do not restore the complete configuration from a different firmware.
5. Copy the correct image to `/tmp` and validate it:

   ```sh
   sysupgrade -T /tmp/ax3000cv2-nss-sysupgrade.bin
   ```

   Stop if validation fails. Do not force the upgrade with `-F`.

6. Perform a clean installation:

   ```sh
   sysupgrade -n /tmp/ax3000cv2-nss-sysupgrade.bin
   ```

7. Keep power connected while writing. Watch the boot process through UART. Once your computer receives a LAN DHCP address, open `192.168.1.1`, log in with `root/admin`, change the password and configure Wi-Fi.
8. Check all three LAN ports and WAN for Gigabit links, DHCP and bidirectional traffic. Test both reboot and a power cycle before relying on the installation.

Rename the downloaded file to match the examples or substitute its actual filename. If a build generates `factory.ubi`, that does not mean it can be flashed through the stock web interface. Releases provide sysupgrade and initramfs images only.

## Migrating from stock firmware

This repository has no verified direct upgrade path through the stock web interface. Follow the UART, bootloader and RAM procedure in the [original device project](https://github.com/michioxd/openwrt-wf810df), checking your hardware revision. Creating `bootipq_owrt` and changing the partition layout are separate steps; setting `bootcmd` alone does not create them.

After booting OpenWrt from RAM, preserve ART and the bootloader partitions, run preflight and check LAN, WAN and Wi-Fi. Flash sysupgrade only after confirming the layout. If your layout differs from `mtd20 rootfs` with size `0x0f300000`, this build's upgrade script is not suitable for it.
