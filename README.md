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

<img width="1601" height="818" alt="6" src="https://github.com/user-attachments/assets/86775578-349b-4e96-b27c-1f996007561f" />


---

## ⚔️ Kịch bản 2: Tấn công HTTP Flood (Layer 7)
**Nguyên lý:** Tấn công trực tiếp vào ứng dụng Web. Sử dụng cơ chế Đa luồng (Multi-threading) để tạo ra hàng ngàn kết nối hợp lệ, gửi liên tục các yêu cầu `HTTP GET` vô nghĩa, ép CPU của Server hoạt động 100% công suất để xử lý.
- **Công cụ sử dụng:** `http_flood.py` (Custom script Python Socket).
- **Kết quả nghiệm thu:** CPU Server đạt mức 100%, chỉ số Load Average tăng vọt, hệ thống tê liệt.

<img width="1695" height="928" alt="8" src="https://github.com/user-attachments/assets/31e96fcf-d2f1-4dda-a5f3-8a1ef7048aab" />

---

## 🛡️ Kịch bản 3: Phòng thủ Tường lửa (Blue Team)
**Giải pháp:** Triển khai cơ chế **Rate Limiting** (Giới hạn tốc độ kết nối) bằng Tường lửa `iptables` tích hợp sẵn trên nhân Linux. 
Hệ thống sẽ ghi nhận các IP kết nối mới, nếu một IP gửi vượt quá 20 yêu cầu trong vòng 1 giây, các gói tin tiếp theo sẽ bị hệ thống vứt bỏ (DROP) ngay lập tức trước khi chạm tới Web Server.


1. **Tấm khiên hoạt động (Nguyên nhân):** Lệnh `iptables -nL INPUT -v` xác nhận quy tắc Rate Limiting đã được kích hoạt. Nhìn vào cột `pkts DROP`, hệ thống đã bắt quả tang và âm thầm vứt bỏ hơn 13.000 gói tin tấn công vi phạm tốc độ (vượt ngưỡng 20 hits/s).

<img width="1698" height="920" alt="Screenshot 2026-03-26 124754" src="https://github.com/user-attachments/assets/6dd0a037-5c4e-4700-8c0d-6698db1b9955" />


2. **Hệ thống an toàn (Kết quả):** Nhờ Tường lửa chặn đứng "cơn lũ" từ vòng ngoài, bảng giám sát `htop` cho thấy CPU của Web Server lập tức được giải phóng. Mức ngốn CPU giảm mạnh từ 100% xuống chỉ còn 1-3%, chỉ số Load Average hạ nhiệt về mức cực kỳ an toàn (0.08). Web Server vẫn sống sót và phục vụ người dùng bình thường.
<img width="1682" height="908" alt="10" src="https://github.com/user-attachments/assets/20f4a3e4-12aa-45e3-9c3e-e11e656e5fbe" />

**Cấu hình Iptables (Ubuntu 24.04):**
```bash
# 1. Ghi nhận các kết nối mới vào cổng 80
sudo iptables -I INPUT -p tcp -m tcp --dport 80 -m conntrack --ctstate NEW -m recent --set --name HTTP_LIMIT

# 2. DROP các kết nối vượt quá 20 hits/giây
sudo iptables -I INPUT -p tcp -m tcp --dport 80 -m conntrack --ctstate NEW -m recent --update --seconds 1 --hitcount 20 --name HTTP_LIMIT -j DROP
