# Cứu hộ

[English](../RECOVERY.md) | **Tiếng Việt**

[Trang chủ](../../README.vi.md)

Giữ console UART 115200 8N1; thu log từ lúc cấp nguồn. Nếu đang ghi flash, không ngắt nguồn để thử cứu hộ.

## Kernel / cấu hình không lên

Ưu tiên failsafe của OpenWrt nếu kernel còn boot: khôi phục cấu hình đã biết tốt hoặc reset overlay. Reset xóa cấu hình người dùng; mật khẩu của bản community sau reset là `admin`.

Nếu cần boot RAM, ngắt autoboot vào U-Boot theo hướng dẫn revision tương ứng. Dùng TFTP trên PC Ethernet `192.168.1.2`, chỉ sau khi đường Ethernet bootloader đã được khởi tạo đúng. Ví dụ cho bootloader đã xác nhận tương thích:

```text
setenv ipaddr 192.168.1.1
setenv serverip 192.168.1.2
tftpboot 0x44000000 ax3000cv2-nss-initramfs.itb
bootm 0x44000000#config@1
```

Đây là boot RAM, không lưu environment và không ghi firmware. Kiểm tra tên config FIT bằng `dumpimage -l` trước; nếu khác, dùng tên thực tế. Không tự thêm `saveenv`, `nand erase`, `nand write` hoặc lệnh `go` không khớp bootloader.

Khi RAM đã lên, lấy log, xác minh layout bằng preflight rồi ghi lại sysupgrade đã biết tốt theo INSTALL. Không khôi phục ART của thiết bị khác.

## Mất LAN sau reboot

Xem log switch/PHY trong `dmesg`, trạng thái `ip link` và `ethtool lan1/lan2/lan3/wan`. Nếu PHY được nhận nhưng mọi LAN mất link, kiểm tra bước bootstrap Ethernet của bootloader trong INSTALL. Không kết luận chỉ từ trạng thái bridge hoặc đèn port.

Nếu còn Wi-Fi dùng nó để đọc log; không sửa hàng loạt driver, bootloader và cấu hình cùng lúc. Không ghi lại toàn bộ NAND để chữa một lỗi cấu hình mạng.
