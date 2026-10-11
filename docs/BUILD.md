# Build from source

**English** | [Tiếng Việt](vi/BUILD.md)

[Home](../README.md)

Use x86-64 Linux, such as Ubuntu 24.04, with a regular user account. Allow at least 8 GiB RAM and 50 GiB free storage. A clean build may take several hours depending on your computer and network. In WSL2, build on the Linux filesystem rather than directly under `/mnt/c`.

```sh
sudo apt update
sudo apt install build-essential clang flex bison g++ gawk gcc-multilib \
  gettext git libncurses-dev libssl-dev python3 python3-setuptools \
  rsync unzip zlib1g-dev file wget curl subversion swig time
git clone https://github.com/An1910-05/openwrt-ax3000cv2.git
cd openwrt-ax3000cv2
python3 scripts/prepare-build.py --output "$HOME/ax3000cv2-build"
JOBS=4 sh scripts/build.sh "$HOME/ax3000cv2-build"
```

Output is in `bin/targets/qualcommax/ipq50xx/` within the build tree. The `wf810df-squashfs-sysupgrade.bin` image upgrades compatible OpenWrt; `wf810df-initramfs-uImage.itb` boots from RAM. Generate checksums with `sha256sum` and read the [installation guide](INSTALL.md) before using the images.

`sources.lock.json` pins the base commit, feeds and board data. The preparation script verifies the SHA-256 hashes of public board data and packages it using the device-tree IDs. Per-device calibration is read from the router's ART partition at boot. Do not place ART files, SSH keys, `/etc/shadow` or backups in the `files` directory.

The profile uses OpenWrt's internal toolchain and does not contain the publisher's local toolchain paths. The script omits the unused video feed and removes unused weechat/squeezelite package links with dependency cycles. It also removes a redundant conflict between the two SoC-specific nss-tools variants and restricts the NSS LuCI page to IPQ50xx. The profile selects `nss-tools-dwmac` separately to avoid a cycle in generated Kconfig.

To modify the profile, run `make menuconfig` in the build tree and review diffconfig. Changes to the kernel, NSS or feeds require rebuilding matching modules; do not copy kernel modules from another build.

The **Build firmware** workflow can be started manually in GitHub Actions. It uploads build artifacts for inspection and does not automatically publish a release or flash a router. Pinned sources do not guarantee identical binary output: tool timestamps and auxiliary firmware inputs need additional handling for fully reproducible binaries.
