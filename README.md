# 🛡️ DoS/DDoS Attack Simulation & Defense Lab

**Author:** [@hien-cybers](https://github.com/hien-cybers)
**Role:** Red Team (Attacker) & Blue Team (Defender)

---

## ⚠️ DISCLAIMER / MIỄN TRỪ TRÁCH NHIỆM

Dự án này được tạo ra **ĐỘC QUYỀN cho mục đích học tập, giáo dục và nghiên cứu an toàn hệ thống (Educational Purposes Only)**.

Mọi hành vi sử dụng mã nguồn trong kho chứa này để tấn công các hệ thống thực tế mà không có sự cho phép bằng văn bản là vi phạm pháp luật.

**Tác giả không chịu trách nhiệm cho bất kỳ sự lạm dụng nào.**

---

## 📖 Tổng quan dự án (Project Overview)

Dự án Lab này mô phỏng các kịch bản tấn công **Từ chối dịch vụ (DoS/DDoS)** nhắm vào Web Server, đồng thời triển khai các biện pháp phòng thủ hiệu quả bằng Tường lửa và tinh chỉnh nhân Linux.

### 🔁 Quy trình kiểm thử gồm 2 pha:

* **Red Team:**

  * Viết script Python tấn công:

    * Layer 4 (Transport)
    * Layer 7 (Application)

* **Blue Team:**

  * Triển khai các cơ chế phòng thủ:

    * Kernel Tuning (TCP SYN Cookies)
    * Rate Limiting (Giới hạn tốc độ kết nối)

---

## 🏗️ Kiến trúc Hệ thống Lab (Topology)

* **Máy Tấn công (Attacker):**

  * Kali Linux
  * Công cụ: Python3, Scapy, Multi-threading Socket

* **Máy Nạn nhân (Victim):**

  * Ubuntu Server 24.04
  * Dịch vụ: Apache2 Web Server

* **Công cụ giám sát:**

  * Wireshark
  * htop
  * netstat
  * iptables

---

## ⚔️ Kịch bản 1: Tấn công SYN Flood (Layer 4)

### 🧠 Nguyên lý

Khai thác cơ chế bắt tay 3 bước (3-way handshake) của TCP:

1. Attacker gửi hàng loạt gói `SYN`
2. Server phản hồi `SYN-ACK`
3. Attacker **không gửi ACK**

➡️ Server giữ kết nối ở trạng thái `SYN_RECV` → **cạn RAM**

### 🛠️ Công cụ sử dụng

```bash
syn_flood.py  # Script custom sử dụng Scapy
```

### 📊 Kết quả nghiệm thu

* Server bị ngập kết nối `SYN_RECV`
* Hàng đợi kết nối bị quá tải
* Tài nguyên hệ thống suy giảm mạnh

<img width="1601" height="818" alt="6" src="https://github.com/user-attachments/assets/c9395be6-6e31-40eb-a53e-e0b0fbaae17e" />

---

## ⚔️ Kịch bản 2: Tấn công HTTP Flood (Layer 7)

### 🧠 Nguyên lý

* Sử dụng **multi-threading**
* Tạo hàng nghìn request HTTP hợp lệ (`GET`)
* Ép Server xử lý liên tục → CPU 100%

### 🛠️ Công cụ sử dụng

```bash
http_flood.py  # Script Python sử dụng socket
```

### 📊 Kết quả nghiệm thu

* CPU đạt 100%
* Load Average tăng cao
* Web Server phản hồi chậm hoặc ngừng hoạt động

<img width="1698" height="920" alt="Screenshot 2026-03-26 124754" src="https://github.com/user-attachments/assets/0b656c5d-6017-47f4-b965-ec1aa44cd561" />

---

## 🛡️ Kịch bản 3: Phòng thủ Hệ thống (Blue Team)

---

### 🔐 3.1. Chống SYN Flood bằng Kernel Tuning (Layer 4)

### 💡 Giải pháp

Kích hoạt cơ chế **TCP SYN Cookies**:

* Không cấp phát RAM ngay khi nhận SYN
* Tạo cookie mã hóa
* Chỉ thiết lập kết nối khi client phản hồi hợp lệ

➡️ **Vô hiệu hóa IP spoofing**

### ⚙️ Cấu hình sysctl

```bash
# Bật SYN Cookies
sudo sysctl -w net.ipv4.tcp_syncookies=1

# Tăng backlog queue
sudo sysctl -w net.ipv4.tcp_max_syn_backlog=4096

# Giảm số lần retry SYN-ACK
sudo sysctl -w net.ipv4.tcp_synack_retries=2
```

---

### 🌐 3.2. Chống HTTP Flood bằng Iptables Connlimit (Layer 7)

### 💡 Giải pháp

HTTP Flood sử dụng kết nối hợp lệ → không chặn bằng SYN Cookies được.

➡️ Dùng:

* `iptables`
* `connlimit module`

👉 Giới hạn số kết nối đồng thời / IP

---

### ⚙️ Cấu hình Iptables

```bash
# Drop IP có hơn 20 kết nối đồng thời vào port 80
sudo iptables -A INPUT -p tcp --dport 80 -m connlimit --connlimit-above 20 -j DROP
```

---

### 📊 Kết quả nghiệm thu

* IP spam request bị chặn ngay lập tức
* Giảm tải hệ thống rõ rệt:

  * CPU từ 100% → ổn định
* Web Server hoạt động lại bình thường
* Quan sát qua `htop`:

  * Hệ thống mượt
  * Không còn nghẽn tài nguyên

---

## ✅ Tổng kết

| Kịch bản   | Loại tấn công | Giải pháp          |
| ---------- | ------------- | ------------------ |
| SYN Flood  | Layer 4       | SYN Cookies        |
| HTTP Flood | Layer 7       | Iptables Connlimit |

---

## 🚀 Gợi ý mở rộng

* Thêm `fail2ban` để tự động block IP
* Sử dụng `nginx rate limiting`
* Triển khai WAF (Web Application Firewall)
* Test với công cụ:

  * `hping3`
  * `ab (Apache Benchmark)`
  * `locust`

---

## 📌 Ghi chú

Lab này phù hợp cho:

* Sinh viên An toàn thông tin
* Pentester (Junior → Mid)
* DevOps / System Admin muốn hiểu sâu về bảo mật hệ thống

---
