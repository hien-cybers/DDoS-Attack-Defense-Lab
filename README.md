# 🛡️ DoS/DDoS Attack Simulation & Defense Lab

**Author:** [@hien-cybers](https://github.com/hien-cybers)  
**Role:** Red Team (Attacker) & Blue Team (Defender)

> **⚠️ DISCLAIMER / MIỄN TRỪ TRÁCH NHIỆM:** > Dự án này được tạo ra ĐỘC QUYỀN cho mục đích học tập, giáo dục và nghiên cứu an toàn hệ thống (Educational Purposes Only). Mọi hành vi sử dụng mã nguồn trong kho chứa này để tấn công các hệ thống thực tế mà không có sự cho phép bằng văn bản là vi phạm pháp luật. Tác giả không chịu trách nhiệm cho bất kỳ sự lạm dụng nào.

---

## 📖 Tổng quan dự án (Project Overview)
Dự án Lab này mô phỏng lại các kịch bản tấn công Từ chối dịch vụ (DoS/DDoS) nhắm vào máy chủ Web Server, đồng thời triển khai các biện pháp phòng thủ hiệu quả bằng Tường lửa và tinh chỉnh nhân Linux. Dự án trải qua 2 vòng kiểm thử:
- **Red Team:** Viết script Python tấn công Tầng 4 (Transport) và Tầng 7 (Application).
- **Blue Team:** Cấu hình hệ thống phòng thủ Kernel Tuning (TCP SYN Cookies) và Rate Limiting (Giới hạn tốc độ) để chặn đứng tấn công.

## 🏗️ Kiến trúc Hệ thống Lab (Topology)
- **Máy Tấn công (Attacker):** Kali Linux (Sử dụng Python3, Scapy, Socket đa luồng).
- **Máy Nạn nhân (Victim):** Ubuntu Server 24.04 (Chạy dịch vụ Apache2 Web Server).
- **Công cụ giám sát:** Wireshark, htop, netstat, iptables.

---

## ⚔️ Kịch bản 1: Tấn công SYN Flood (Layer 4)
**Nguyên lý:** Khai thác cơ chế bắt tay 3 bước (3-way handshake) của giao thức TCP. Kẻ tấn công gửi hàng loạt gói tin `SYN` với địa chỉ IP giả mạo (Spoofed IP) nhưng không bao giờ gửi lại gói `ACK`, khiến Server cạn kiệt bộ nhớ (RAM) do phải duy trì các kết nối ảo.
- **Công cụ sử dụng:** `syn_flood.py` (Custom script sử dụng thư viện Scapy).
- **Kết quả nghiệm thu:** Server ngập lụt trong trạng thái `SYN_RECV`.

<img width="1601" height="818" alt="6" src="https://github.com/user-attachments/assets/c9395be6-6e31-40eb-a53e-e0b0fbaae17e" />

---

## ⚔️ Kịch bản 2: Tấn công HTTP Flood (Layer 7)
**Nguyên lý:** Tấn công trực tiếp vào ứng dụng Web. Sử dụng cơ chế Đa luồng (Multi-threading) để tạo ra hàng ngàn kết nối hợp lệ, gửi liên tục các yêu cầu `HTTP GET` vô nghĩa, ép CPU của Server hoạt động 100% công suất để xử lý.
- **Công cụ sử dụng:** `http_flood.py` (Custom script Python Socket).
- **Kết quả nghiệm thu:** CPU Server đạt mức 100%, chỉ số Load Average tăng vọt, hệ thống tê liệt.

<img width="1698" height="920" alt="Screenshot 2026-03-26 124754" src="https://github.com/user-attachments/assets/0b656c5d-6017-47f4-b965-ec1aa44cd561" />

---

## 🛡️ Kịch bản 3: Phòng thủ Hệ thống (Blue Team)

### 3.1. Chống SYN Flood bằng Kernel Tuning (Layer 4)
**Giải pháp:** Can thiệp trực tiếp vào nhân hệ điều hành Linux để bật thuật toán `TCP SYN Cookies`. Thay vì cấp phát bộ nhớ RAM ngay lập tức khi nhận gói SYN, hệ thống sẽ băm thông tin thành một giá trị Cookie. Chỉ khi client trả về mã Cookie hợp lệ, kết nối mới được thiết lập. Điều này vô hiệu hóa hoàn toàn đám IP giả mạo.

**Cấu hình tham số hệ thống (sysctl):**
```bash
# Bắt buộc kích hoạt cơ chế bảo vệ bằng Cookies
sudo sysctl -w net.ipv4.tcp_syncookies=1

# Tăng kích thước hàng đợi chờ để chịu tải tốt hơn
sudo sysctl -w net.ipv4.tcp_max_syn_backlog=4096

# Giảm số lần Server cố gắng truyền lại gói SYN-ACK
sudo sysctl -w net.ipv4.tcp_synack_retries=2
