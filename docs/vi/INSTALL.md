# Cài đặt

[English](../INSTALL.md) | **Tiếng Việt**

[Trang chủ](../../README.vi.md)

## Kiểm tra thiết bị trước

Hỗ trợ mục tiêu `fpt,wf810df`, WF810DF / AX3000CV2, flash NAND 256 MiB. Tên repo không chứa chữ nhà mạng; device-tree vẫn giữ compatible thật để nhận đúng phần cứng.

Chuẩn bị máy tính Ethernet, UART mức **3.3 V**, dây GND/TX/RX, tốc độ **115200 8N1**. Không nối nguồn VCC của USB-UART vào router. Nếu dùng ESP làm cầu UART, cần firmware bridge riêng phù hợp chân đã nối; firmware router trong repo không nạp vào ESP.

Lưu backup cấu hình **ra máy tính**. Nếu đang dùng firmware gốc, lưu riêng dump các phân vùng và environment trước khi làm theo hướng dẫn chuyển đổi; không chia sẻ ART/calibration, thông tin tài khoản hoặc raw dump công khai. Giữ bản firmware đã chạy tốt và UART để cứu hộ.

## Bootloader và LAN sau khởi động

Trên thiết bị thử nghiệm, bootloader cần chạy bộ khởi tạo Ethernet của vendor trước khi vào kernel. Nếu bỏ bước này, LAN có thể mất link sau reboot/mất điện dù driver đã nhận đủ cổng.

Thiết bị thử nghiệm đã dùng:

```text
bootcmd=bootipq_owrt; go 0x4a9610b5; run bootowrt
```

Địa chỉ `go` **phụ thuộc đúng bản bootloader**, không phải lệnh dùng cho mọi AX3000CV2. Fingerprint `0:APPSBL_1` đã đối chiếu:

```text
57f426f8cbf49731e727f12bce5258facacd3b6007888fe1b1f0df1f1989735c
```

Chạy `sh preflight-router.sh` sau khi chép [script](../../scripts/preflight-router.sh) vào `/tmp` trên OpenWrt. Script chỉ đọc board, layout và hash. Nếu khác, **dừng**, không dùng địa chỉ `go` trên. Hash của slot dự phòng không tự chứng minh slot đang thực thi: phải đối chiếu log UART và quy trình bootloader. Repo chưa có trình cài stock tự động cho mọi revision.

Nếu đã có OpenWrt tương thích, `bootipq_owrt`, `bootowrt` và `fw_printenv` đọc environment đúng CRC, chỉ cân nhắc thay `bootcmd` sau khi xác minh chính xác bootloader đang chạy, lưu environment ra máy tính và hiểu cách khôi phục. Không chép environment của router khác.

## Đang dùng OpenWrt tương thích

1. Đọc trạng thái release. Bản preview chưa boot thử trên phần cứng không được xem là đã ổn định.
2. Tải `*-sysupgrade.bin` và `sha256sums`, đối chiếu SHA-256 trên máy tính.
3. Chạy preflight ở trên; kiểm tra đang có UART và một cổng LAN hoạt động.
4. Tạo backup cấu hình, tải xuống máy tính. Cài sạch được khuyến nghị khi đổi topology/NSS; không phục hồi toàn bộ cấu hình từ firmware khác.
5. Chép đúng file vào `/tmp` và kiểm tra:

   ```sh
   sysupgrade -T /tmp/ax3000cv2-nss-sysupgrade.bin
   ```

   Nếu kiểm tra thất bại, dừng. Không dùng `-F` để ép.

6. Cài sạch:

   ```sh
   sysupgrade -n /tmp/ax3000cv2-nss-sysupgrade.bin
   ```

7. Không ngắt điện trong lúc ghi. Chờ boot qua UART, PC nhận DHCP từ LAN rồi mở `192.168.1.1`, đăng nhập `root/admin`, đổi mật khẩu và thiết lập Wi-Fi.
8. Kiểm tra cả ba LAN và WAN, link Gigabit, DHCP, dữ liệu hai chiều. Thử reboot rồi tắt/bật nguồn trước khi dùng lâu dài.

Đổi tên file tải xuống thành tên trong ví dụ hoặc dùng tên thật tương ứng. File `factory.ubi` nếu build sinh ra không có nghĩa là có thể nạp từ giao diện firmware gốc; release chỉ cung cấp sysupgrade và initramfs.

## Đang dùng firmware gốc

Không có đường nâng cấp trực tiếp qua giao diện stock được xác nhận trong repo này. Thực hiện quy trình UART/bootloader và RAM của [dự án thiết bị gốc](https://github.com/michioxd/openwrt-wf810df), đối chiếu revision của mình. Việc tạo lệnh `bootipq_owrt`/chuyển layout là bước riêng, không được tạo chỉ bằng `setenv bootcmd`.

Sau khi đã vào OpenWrt từ RAM, giữ ART và các phân vùng bootloader nguyên vẹn, chạy preflight và kiểm tra LAN/WAN/Wi-Fi. Chỉ ghi sysupgrade khi layout được xác nhận. Nếu layout khác `mtd20 rootfs` kích thước `0x0f300000`, script upgrade của bản này không phải lựa chọn phù hợp.
