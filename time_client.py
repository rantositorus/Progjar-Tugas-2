import threading
import socket
import time
from datetime import datetime

SERVER_IP = '172.16.16.102'
PORT = 45000
JUMLAH_KLIEN_KONKUREN = 5

def client_task(client_id, target_time_str):
    print(f"[Client-{client_id}] Waiting until {target_time_str} to send request...")
    try:
        target_time_obj = datetime.strptime(target_time_str, "%H:%M:%S").time()
        while datetime.now().time() < target_time_obj:
            time.sleep(0.1)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SERVER_IP, PORT))
        print(f"[Client-{client_id}] Connected to server.")

        sock.sendall("TIME\r\n".encode())
        response = sock.recv(1024).decode()
        print(f"[Client-{client_id}] Server responded: {response.strip()}")

        sock.sendall("QUIT\r\n".encode())
        sock.close()
        print(f"[Client-{client_id}] Disconnected.")

    except Exception as e:
        print(f"[Client-{client_id}] Error: {str(e)}")

if __name__ == "__main__":
    threads = []
    WAKTU_TARGET_SERENTAK = "08:10:00"

    for i in range(JUMLAH_KLIEN_KONKUREN):
        thread = threading.Thread(target=client_task, args=(i, WAKTU_TARGET_SERENTAK))
        threads.append(thread)
        thread.start() 

    for thread in threads:
        thread.join()

    print("Semua klien konkuren telah selesai.")