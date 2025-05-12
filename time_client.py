import socket
import time
from datetime import datetime

SERVER_IP = '192.168.1.10'  # Ganti dengan IP mesin server
PORT = 45000

# Ganti waktu target (format: "HH:MM:SS") sesuai dengan waktu server
TARGET_TIME = "14:30:00"  # Contoh target waktu

def wait_until(target_time_str):
    target_time = datetime.strptime(target_time_str, "%H:%M:%S").time()
    while True:
        now = datetime.now().time()
        if now >= target_time:
            break
        remaining = (
            datetime.combine(datetime.today(), target_time) -
            datetime.combine(datetime.today(), now)
        ).total_seconds()
        print(f"[Client] Waiting for {remaining:.1f} seconds...")
        time.sleep(min(remaining, 1))

def main():
    print(f"[Client] Waiting until {TARGET_TIME} to send request...")
    wait_until(TARGET_TIME)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SERVER_IP, PORT))

        sock.sendall("TIME\r\n".encode())
        response = sock.recv(1024).decode()
        print(f"[Client] Server responded: {response.strip()}")

        sock.sendall("QUIT\r\n".encode())
        sock.close()

    except Exception as e:
        print(f"[Client] Error: {str(e)}")

if __name__ == "__main__":
    main()
