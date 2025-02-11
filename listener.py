import socket
import threading
import logging

# Configure logging
logging.basicConfig(filename="honeypot.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Function to listen on arbitrary ports

def honeypot_listener(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)
    logging.info(f"Listening on port {port}...")

    while True:
        client, addr = server.accept()
        logging.info(
            f"Connection attempt from {addr[0]}:{addr[1]} on port {port}")
        client.send(b"Access Denied\n")
        client.close()


def start_listeners():
    ports = [21, 22, 23, 80, 443, 3306, 3389]  # Common attack ports
    for port in ports:
        thread = threading.Thread(target=honeypot_listener, args=(port,))
        thread.start()


if __name__ == "__main__":
    start_listeners()
