# Sources and licenses

**English** | [Tiếng Việt](vi/ATTRIBUTION.md)

[Home](../README.md)

This repository contains patches and configuration for an OpenWrt build tree; it does not claim authorship of the entire firmware. Source commits are pinned in [sources.lock.json](../sources.lock.json).

- OpenWrt NSS/EDMA base: [kuncy7/openwrt-nss-edma](https://github.com/kuncy7/openwrt-nss-edma), GPL-2.0 and the licenses of individual components.
- Device support, bootloader information and public Wi-Fi data: [michioxd/openwrt-wf810df](https://github.com/michioxd/openwrt-wf810df), [michioxd/upstream-wifi-fw](https://github.com/michioxd/upstream-wifi-fw).
- NSS packages: [kuncy7/nss-packages](https://github.com/kuncy7/nss-packages), with QCA/Qualcomm sources identified in each package's Makefile.
- The Motorcomm YT921x driver and backports retain their author and license headers in the patches.
- OpenWrt packages and LuCI: [OpenWrt packages](https://github.com/openwrt/packages), [OpenWrt LuCI](https://github.com/openwrt/luci), under their upstream licenses.

[COPYING](../COPYING) contains the OpenWrt base's GPL-2.0 license. It does not assign one GPL license to every Wi-Fi, NSS or vendor binary. Firmware binaries have separate terms and NOTICE files in their source packages. Board data payloads come from public sources and are wrapped in an ath11k container; they are not extracted from a personal router's ART partition.

New scripts and configuration in this repository use GPL-2.0-or-later unless a different header is present. Third-party files retain their respective licenses. When distributing binaries, retain the corresponding source references, lockfile, patches, configuration and upstream notices. Source links do not replace any other license obligations for individual packages.
