# Changelog

[English](CHANGELOG.md) | **Tiếng Việt**

## Bản cộng đồng gọn

- Bỏ AdBlock-Fast, Zapret2 và các thành phần DNS riêng khỏi bản cài.
- Giữ LuCI mặc định, NSS và hỗ trợ thiết bị.

## Tài liệu

- README và hướng dẫn mặc định dùng tiếng Anh.
- Chọn ngôn ngữ trên từng trang để mở bản tiếng Việt.

## Community preview

- Tách recipe cộng đồng từ bản NSS đã kiểm tra trên một thiết bị.
- Driver YT9215, topology host LAN và helper tách LAN khỏi đường NSS WAN.
- ath11k/NSS, board ID và calibration lấy từ ART của thiết bị.
- AdBlock-Fast giới hạn bộ nhớ sort và sửa nhánh cache nén.
- Zapret2/LuCI, DNS riêng theo tên miền, giữ NFQUEUE ở cửa sổ gói đầu trước offload.
- Đèn trắng khi probe Internet thành công, đỏ khi thất bại, sửa mode GPIO.
- Mặc định root/admin, Wi-Fi chưa bật, các dịch vụ lọc tùy chọn chưa chạy.
- Khóa nguồn và hướng dẫn bootloader/cài/cứu hộ/build; chưa xác nhận hardware boot cho image công khai.
- Sửa guard của script khởi động để tạo liên kết NSS/Zapret2 đúng khi đóng image trên máy build.
- Preview 2026.10.11: build thành công, kiểm tra rootfs/initramfs và checksum; không nạp bản này lên thiết bị thử nghiệm đang hoạt động.
