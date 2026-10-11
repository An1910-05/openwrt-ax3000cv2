<p align="center">
  <img src="docs/assets/openwrt-logo.png" alt="OpenWrt" width="480">
</p>

# OpenWrt AX3000CV2 — NSS Community

[English](README.md) | **Tiếng Việt**

Bản dựng OpenWrt cộng đồng cho **AX3000CV2 / WF810DF**, Qualcomm IPQ5018 + QCN6122, switch Motorcomm YT9215. Repo chứa bản vá, cấu hình, giao diện LuCI và công cụ tự build; không phải bản phát hành chính thức của OpenWrt hoặc nhà sản xuất.

**Trạng thái: community preview.** Image đã build và kiểm tra nội dung, **chưa boot thử trực tiếp trên phần cứng**. Bản firmware công khai dùng cấu hình sạch và dữ liệu Wi-Fi từ nguồn công khai.

## Tải và cài

- [Bản firmware gọn](https://github.com/An1910-05/openwrt-ax3000cv2/releases/tag/v2026.10.11-minimal-preview): firmware, SHA-256 và trạng thái kiểm thử.
- [Hướng dẫn cài](docs/vi/INSTALL.md): phân biệt nâng cấp OpenWrt với chuyển từ firmware gốc.
- [Cứu hộ UART / RAM](docs/vi/RECOVERY.md).
- [Tự build](docs/vi/BUILD.md), [nguồn và giấy phép](docs/vi/ATTRIBUTION.md).

Chỉ cài đúng thiết bị **WF810DF**, không suy ra tương thích từ tên AX3000 của router khác. Không nạp file sysupgrade bằng giao diện firmware gốc.

## Có gì trong bản này?

| Thành phần | Cách hoạt động |
|---|---|
| Wi-Fi ath11k + NSS | Offload Wi-Fi; đọc calibration từ ART của chính router |
| WAN NSS | Tăng tốc đường WAN trên IPQ5018 |
| LAN YT9215 | Driver DSA yt921x, topology LAN host, software flow offload |
| LuCI | Trang quản trị OpenWrt mặc định và trạng thái NSS |
| Đèn Internet | Trắng khi kiểm tra Internet thành công, đỏ khi thất bại |

LAN ổn định còn phụ thuộc bước khởi tạo Ethernet của bootloader. Bản vá kernel không thay thế bước này; xem [lưu ý bootloader](docs/vi/INSTALL.md#bootloader-và-lan-sau-khởi-động).

## Mặc định sau cài sạch / reset

- Quản trị: `http://192.168.1.1`, tài khoản `root`, mật khẩu **`admin`**. Đổi mật khẩu sau lần đăng nhập đầu tiên.
- Wi-Fi chưa bật; vào **Network → Wireless** chọn quốc gia, SSID và mật khẩu.
- NSS bật; hardware flow offloading của firewall tắt, software flow offloading bật.
- Không kèm backup, SSH key, mật khẩu Wi-Fi hoặc ART của người khác.

## Đóng góp và báo lỗi

Mở [Issue](https://github.com/An1910-05/openwrt-ax3000cv2/issues), ghi phiên bản, cách tái hiện, cổng đang dùng, `ubus call system board`, `dmesg` và trạng thái link. Xóa mật khẩu, địa chỉ MAC/IP công cộng và tên miền riêng khỏi log trước khi gửi. Không đăng ART hay bản dump flash đầy đủ.

Cảm ơn [michioxd](https://github.com/michioxd/openwrt-wf810df), [kuncy7](https://github.com/kuncy7/openwrt-nss-edma), OpenWrt và các tác giả driver/NSS. Chi tiết trong [ATTRIBUTION.md](docs/vi/ATTRIBUTION.md).
