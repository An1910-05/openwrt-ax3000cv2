<p align="center">
  <img src="docs/assets/openwrt-logo.png" alt="OpenWrt" width="480">
</p>

# OpenWrt AX3000CV2 — NSS Community

**English** | [Tiếng Việt](README.vi.md)

A community OpenWrt build for **AX3000CV2 / WF810DF**, with Qualcomm IPQ5018 + QCN6122 and a Motorcomm YT9215 switch. This repository provides patches, configuration, LuCI pages and build tools. It is not an official release from OpenWrt or the device manufacturer.

**Status: community preview.** The images have been built and their contents checked, but **have not been boot-tested on hardware**. The public firmware uses clean defaults and publicly sourced Wi-Fi board data.

## Download and install

- [Minimal firmware release](https://github.com/An1910-05/openwrt-ax3000cv2/releases/tag/v2026.10.11-minimal-preview): firmware, SHA-256 checksums and testing status.
- [Installation guide](docs/INSTALL.md): upgrading compatible OpenWrt or migrating from stock firmware.
- [UART / RAM recovery](docs/RECOVERY.md).
- [Build from source](docs/BUILD.md), [sources and licenses](docs/ATTRIBUTION.md).

Use these images only on compatible **WF810DF** hardware. An AX3000 product name alone does not establish compatibility. Do not upload a sysupgrade image through the stock firmware web interface.

## Features

| Component | Behavior |
|---|---|
| ath11k Wi-Fi + NSS | Wi-Fi offload; reads calibration from the router's own ART partition |
| WAN NSS | Accelerates the WAN path on IPQ5018 |
| YT9215 LAN | yt921x DSA driver, host LAN topology and software flow offload |
| LuCI | Standard OpenWrt administration and NSS status |
| Internet LED | White when Internet probes succeed; red when they fail |

Reliable LAN operation also depends on the bootloader's Ethernet initialization. The kernel patches do not replace this step; see the [bootloader notes](docs/INSTALL.md#bootloader-and-lan-after-reboot).

## Defaults after a clean installation or reset

- Administration: `http://192.168.1.1`, username `root`, password **`admin`**. Change the password after your first login.
- Wi-Fi is disabled. Open **Network → Wireless** to set your country, SSID and password.
- NSS is enabled. Firewall hardware flow offloading is disabled; software flow offloading is enabled.
- No personal backups, SSH keys, Wi-Fi passwords or another device's ART data are included.

## Contributing and reporting bugs

Open an [issue](https://github.com/An1910-05/openwrt-ax3000cv2/issues) with the firmware version, reproduction steps, port in use, `ubus call system board`, `dmesg` and link status. Remove passwords, MAC addresses, public IP addresses and private domain names from logs before posting. Do not upload ART or a full flash dump.

Thanks to [michioxd](https://github.com/michioxd/openwrt-wf810df), [kuncy7](https://github.com/kuncy7/openwrt-nss-edma), OpenWrt and the driver/NSS contributors. See [ATTRIBUTION.md](docs/ATTRIBUTION.md) for details.
