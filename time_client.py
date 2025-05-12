import socket
import time

SERVER_IP = '172.16.16.101'  # Ganti dengan IP mesin server
PORT = 45000

def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SERVER_IP, PORT))

        sock.sendall("TIME\r\n".encode())
        response = sock.recv(1024).decode()
        print(f"[Client] Server responded: {response.strip()}")

        time.sleep(1)  # optional delay

        sock.sendall("QUIT\r\n".encode())
        sock.close()

    except Exception as e:
        print(f"[Client] Error: {str(e)}")

if __name__ == "__main__":
    main()
