# 🛡️ DoS/DDoS Attack Simulation & Defense Lab

**Author:** [@hien-cybers](https://github.com/hien-cybers)  
**Role:** Red Team (Attacker) & Blue Team (Defender)

> **⚠️ DISCLAIMER / MIỄN TRỪ TRÁCH NHIỆM:** > Dự án này được tạo ra ĐỘC QUYỀN cho mục đích học tập, giáo dục và nghiên cứu an toàn hệ thống (Educational Purposes Only). Mọi hành vi sử dụng mã nguồn trong kho chứa này để tấn công các hệ thống thực tế mà không có sự cho phép bằng văn bản là vi phạm pháp luật. Tác giả không chịu trách nhiệm cho bất kỳ sự lạm dụng nào.

---

## 📖 Tổng quan dự án (Project Overview)
Dự án Lab này mô phỏng các kịch bản tấn công Từ chối dịch vụ (DoS/DDoS) nhắm vào máy chủ Web Server, đồng thời triển khai các biện pháp phòng thủ chuyên sâu bằng **Tường lửa Iptables**. 

Dự án kiểm thử thực tế khả năng chịu tải và phòng ngự của hệ thống qua hai tầng mạng trọng yếu:
- **Tầng 4 (Transport Layer):** Tấn công SYN Flood & Phòng thủ bằng cơ chế Rate Limiting.
- **Tầng 7 (Application Layer):** Tấn công HTTP Flood & Phòng thủ bằng cơ chế Connlimit.

## 🏗️ Kiến trúc Hệ thống Lab (Topology)
- **Máy Tấn công (Attacker):** Kali Linux (Sử dụng Python3, Scapy, Socket đa luồng).
- **Máy Nạn nhân (Victim):** Ubuntu Server 24.04 (Chạy dịch vụ Apache2 Web Server).
- **Công cụ giám sát & Phòng thủ:** Wireshark, htop, netstat, iptables.

---

## ⚔️ GIAI ĐOẠN 1: TẤN CÔNG & PHÒNG THỦ TẦNG 4 (LAYER 4)

### 🔴 Red Team: Tấn công SYN Flood
**Nguyên lý:** Khai thác lỗ hổng trong cơ chế bắt tay 3 bước (3-way handshake) của giao thức TCP. Kẻ tấn công gửi hàng loạt gói tin `SYN` với địa chỉ IP giả mạo (Spoofed IP) nhưng không bao giờ gửi lại gói `ACK`. Máy chủ bị đánh lừa, liên tục cấp phát bộ nhớ để chờ phản hồi, dẫn đến cạn kiệt tài nguyên.
- **Công cụ sử dụng:** `syn_flood.py` (Custom script Python + Scapy).
- **Kết quả kiểm thử:** Hàng đợi RAM của Server bị lấp đầy bởi các trạng thái `SYN_RECV`. Dịch vụ bị nghẽn mạch (DoS) hoàn toàn.

<img width="1601" height="818" alt="6" src="https://github.com/user-attachments/assets/c9395be6-6e31-40eb-a53e-e0b0fbaae17e" />

### 🔵 Blue Team: Phòng thủ bằng Iptables (Rate Limiting)
**Giải pháp:** Để bảo vệ hàng đợi TCP, Blue Team cấu hình Tường lửa Iptables thiết lập ngưỡng giới hạn tốc độ (Rate Limit) ngay tại cửa ngõ. Những gói tin vượt quá lưu lượng cho phép sẽ bị tiêu diệt trước khi chạm vào nhân hệ điều hành.

**Cấu hình Iptables:**
```bash
# Chỉ cho phép tối đa 5 gói tin SYN/giây lọt vào cổng 80 (Ngưỡng Burst = 10)
sudo iptables -A INPUT -p tcp --syn --dport 80 -m limit --limit 5/s --limit-burst 10 -j ACCEPT

# Vứt bỏ (DROP) toàn bộ các gói tin SYN vượt quá ngưỡng trên
sudo iptables -A INPUT -p tcp --syn --dport 80 -j DROP
