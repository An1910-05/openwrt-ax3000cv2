# Changelog

**English** | [Tiếng Việt](CHANGELOG.vi.md)

## Minimal community build

- Removed bundled AdBlock-Fast, Zapret2 and per-domain DNS additions.
- Kept standard LuCI, NSS and device support.

## Documentation

- English is the default language for the README and guides.
- Vietnamese versions are available through the language links on each page.

## Community preview

- Created a community build recipe from an NSS reference build tested on one device.
- Added the YT9215 driver, host LAN topology and a helper separating LAN from the NSS WAN path.
- Integrated ath11k/NSS and board IDs; calibration is read from the device's own ART partition.
- Bounded AdBlock-Fast sort memory and fixed compressed-cache handling.
- Added Zapret2/LuCI and per-domain DNS; keeps the initial packet window in NFQUEUE before offload.
- Added white/red Internet probe indication and corrected the LED GPIO mode.
- Set root/admin defaults, disabled Wi-Fi initially and left optional filtering services inactive.
- Pinned sources and documented bootloader requirements, installation, recovery and builds. Hardware boot testing of the public image remains unconfirmed.
- Fixed init-script guards so NSS/Zapret2 startup links can be created during image packaging.
- Preview 2026.10.11: built successfully and checked rootfs, initramfs and checksums. It was not flashed onto the working reference router.
