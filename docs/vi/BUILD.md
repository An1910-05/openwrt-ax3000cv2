# Tự build

[English](../BUILD.md) | **Tiếng Việt**

[Trang chủ](../../README.vi.md)

Dùng Linux x86-64, ví dụ Ubuntu 24.04, tài khoản thường. Nên có ít nhất 8 GiB RAM, 50 GiB trống; build sạch có thể mất vài giờ tùy máy và mạng. WSL2 dùng filesystem Linux, tránh build trực tiếp trong `/mnt/c`.

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

Kết quả ở `bin/targets/qualcommax/ipq50xx/` trong cây build. File `wf810df-squashfs-sysupgrade.bin` dùng nâng cấp OpenWrt tương thích; `wf810df-initramfs-uImage.itb` dùng boot RAM. Tạo checksum bằng `sha256sum` và đọc INSTALL trước khi dùng.

`sources.lock.json` khóa commit nền, các feed và board data. Script xác minh SHA-256 board data công khai, đóng gói theo ID trong device-tree. Calibration riêng lấy từ ART trên router khi boot. Không đưa file ART, SSH key, `/etc/shadow` hoặc backup vào thư mục `files`.

Profile dùng toolchain nội bộ OpenWrt; không chứa đường dẫn toolchain của người phát hành. Script bỏ video feed và các liên kết gói weechat/squeezelite không dùng đang có vòng dependency. Nó cũng bỏ conflict thừa giữa hai nss-tools ràng buộc SoC riêng và giới hạn LuCI NSS cho IPQ50xx; profile chọn `nss-tools-dwmac` riêng để tránh vòng dependency khi sinh Kconfig.

Muốn sửa profile, chạy `make menuconfig` trong cây build và kiểm tra diffconfig. Thay phiên bản kernel/NSS/feed cần build lại module đồng bộ; không chép kmod từ bản khác.

Workflow **Build firmware** có thể chạy thủ công trong Actions. Nó xuất artifact để kiểm tra, không tự tạo release hoặc flash router. Commit nguồn được khóa không đồng nghĩa đầu ra bit-for-bit giống nhau: timestamp công cụ/firmware phụ trợ cần xử lý thêm nếu muốn reproducible binary tuyệt đối.
