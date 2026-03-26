# 🛡️ DoS/DDoS Attack Simulation & Defense Lab

**Author:** [@hien-cybers](https://github.com/hien-cybers)  
**Role:** Red Team (Attacker) & Blue Team (Defender)

> **⚠️ DISCLAIMER / MIỄN TRỪ TRÁCH NHIỆM:** > Dự án này được tạo ra ĐỘC QUYỀN cho mục đích học tập, giáo dục và nghiên cứu an toàn hệ thống (Educational Purposes Only). Mọi hành vi sử dụng mã nguồn trong kho chứa này để tấn công các hệ thống thực tế mà không có sự cho phép bằng văn bản là vi phạm pháp luật. Tác giả không chịu trách nhiệm cho bất kỳ sự lạm dụng nào.

---

## 📖 Tổng quan dự án (Project Overview)
Dự án Lab này mô phỏng lại các kịch bản tấn công Từ chối dịch vụ (DoS/DDoS) nhắm vào máy chủ Web Server, đồng thời triển khai các biện pháp phòng thủ hiệu quả bằng Tường lửa Linux. Dự án trải qua 2 vòng kiểm thử:
- **Red Team:** Viết script Python tấn công Tầng 4 (Transport) và Tầng 7 (Application).
- **Blue Team:** Cấu hình hệ thống phòng thủ Rate Limiting (Giới hạn tốc độ) để chặn đứng tấn công.

## 🏗️ Kiến trúc Hệ thống Lab (Topology)
- **Máy Tấn công (Attacker):** Kali Linux (Sử dụng Python3, Scapy, Socket đa luồng).
- **Máy Nạn nhân (Victim):** Ubuntu Server 24.04 (Chạy dịch vụ Apache2 Web Server).
- **Công cụ giám sát:** Wireshark, htop, netstat, iptables.

---

## ⚔️ Kịch bản 1: Tấn công SYN Flood (Layer 4)
**Nguyên lý:** Khai thác cơ chế bắt tay 3 bước (3-way handshake) của giao thức TCP. Kẻ tấn công gửi hàng loạt gói tin `SYN` với địa chỉ IP giả mạo (Spoofed IP) nhưng không bao giờ gửi lại gói `ACK`, khiến Server cạn kiệt bộ nhớ (RAM) do phải duy trì các kết nối ảo.
- **Công cụ sử dụng:** `syn_flood.py` (Custom script sử dụng thư viện Scapy).
- **Kết quả nghiệm thu:** Server ngập lụt trong trạng thái `SYN_RECV`.

*(Chèn ảnh chụp màn hình lệnh netstat tràn ngập SYN_RECV của bạn vào đây)*

---

## ⚔️ Kịch bản 2: Tấn công HTTP Flood (Layer 7)
**Nguyên lý:** Tấn công trực tiếp vào ứng dụng Web. Sử dụng cơ chế Đa luồng (Multi-threading) để tạo ra hàng ngàn kết nối hợp lệ, gửi liên tục các yêu cầu `HTTP GET` vô nghĩa, ép CPU của Server hoạt động 100% công suất để xử lý.
- **Công cụ sử dụng:** `http_flood.py` (Custom script Python Socket).
- **Kết quả nghiệm thu:** CPU Server đạt mức 100%, chỉ số Load Average tăng vọt, hệ thống tê liệt.

*(Chèn ảnh chụp màn hình bảng htop với CPU đỏ rực 100% vào đây)*

---

## 🛡️ Kịch bản 3: Phòng thủ Tường lửa (Blue Team)
**Giải pháp:** Triển khai cơ chế **Rate Limiting** (Giới hạn tốc độ kết nối) bằng Tường lửa `iptables` tích hợp sẵn trên nhân Linux. 
Hệ thống sẽ ghi nhận các IP kết nối mới, nếu một IP gửi vượt quá 20 yêu cầu trong vòng 1 giây, các gói tin tiếp theo sẽ bị hệ thống vứt bỏ (DROP) ngay lập tức trước khi chạm tới Web Server.

**Cấu hình Iptables (Ubuntu 24.04):**
```bash
# 1. Ghi nhận các kết nối mới vào cổng 80
sudo iptables -I INPUT -p tcp -m tcp --dport 80 -m conntrack --ctstate NEW -m recent --set --name HTTP_LIMIT

# 2. DROP các kết nối vượt quá 20 hits/giây
sudo iptables -I INPUT -p tcp -m tcp --dport 80 -m conntrack --ctstate NEW -m recent --update --seconds 1 --hitcount 20 --name HTTP_LIMIT -j DROP
