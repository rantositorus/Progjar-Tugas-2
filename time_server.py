from socket import *
import socket
import threading
import logging
from datetime import datetime

logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(message)s')

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        logging.warning(f"[Thread-{self.name}] Handling {self.address}")
        buffer = b""
        try:
            while True:
                data = self.connection.recv(32)
                if not data:
                    break
                buffer += data

                while b'\r\n' in buffer:
                    line, buffer = buffer.split(b'\r\n', 1)
                    request = line.decode().strip()

                    if request == "TIME":
                        current_time = datetime.now().strftime("%H:%M:%S")
                        response = f"JAM {current_time}\r\n"
                        self.connection.sendall(response.encode())
                        logging.warning(f"[Thread-{self.name}] Sent: {response.strip()}")
                    elif request == "QUIT":
                        logging.warning(f"[Thread-{self.name}] Client {self.address} disconnected.")
                        self.connection.close()
                        return
                    else:
                        logging.warning(f"[Thread-{self.name}] Invalid request: {request}")
        except Exception as e:
            logging.warning(f"[Thread-{self.name}] Error: {str(e)}")
        finally:
            self.connection.close()

class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.bind(('0.0.0.0', 45000))
        self.my_socket.listen(5)
        logging.warning("[*] Time Server is running on port 45000")

        while True:
            connection, client_address = self.my_socket.accept()
            logging.warning(f"[+] Connection from {client_address}")
            client_thread = ProcessTheClient(connection, client_address)
            client_thread.start()
            self.the_clients.append(client_thread)

def main():
    svr = Server()
    svr.start()

if __name__ == "__main__":
    main()
