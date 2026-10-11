# Nguồn và giấy phép

[English](../ATTRIBUTION.md) | **Tiếng Việt**

[Trang chủ](../../README.vi.md)

Repo này là bộ bản vá/cấu hình cho cây build OpenWrt, không nhận là tác giả toàn bộ firmware. Các commit được khóa trong [sources.lock.json](../../sources.lock.json).

- Nền OpenWrt NSS/EDMA: [kuncy7/openwrt-nss-edma](https://github.com/kuncy7/openwrt-nss-edma), GPL-2.0 và giấy phép từng thành phần.
- Hỗ trợ thiết bị, thông tin bootloader và dữ liệu Wi-Fi công khai: [michioxd/openwrt-wf810df](https://github.com/michioxd/openwrt-wf810df), [michioxd/upstream-wifi-fw](https://github.com/michioxd/upstream-wifi-fw).
- NSS packages: [kuncy7/nss-packages](https://github.com/kuncy7/nss-packages), cùng nguồn QCA/Qualcomm theo Makefile mỗi gói.
- Driver Motorcomm YT921x và các bản backport giữ header tác giả/giấy phép trong patch.
- OpenWrt packages và LuCI: [OpenWrt packages](https://github.com/openwrt/packages), [OpenWrt LuCI](https://github.com/openwrt/luci), giữ giấy phép upstream.

[COPYING](../../COPYING) là GPL-2.0 của nền OpenWrt; không áp dụng một giấy phép GPL duy nhất lên tất cả binary Wi-Fi/NSS/vendor. Các firmware binary có điều khoản/NOTICE riêng của nguồn gói. Board data được lấy nguyên payload từ nguồn công khai rồi thêm container ath11k; không trích ART của router cá nhân.

Script/cấu hình mới của repo theo GPL-2.0-or-later khi không có header khác. Các tệp bên thứ ba giữ giấy phép tương ứng. Khi phân phối binary, giữ đường dẫn nguồn tương ứng, lockfile, patch, cấu hình và các thông báo upstream; không coi đường dẫn nguồn là thay thế những nghĩa vụ giấy phép khác của từng gói.
