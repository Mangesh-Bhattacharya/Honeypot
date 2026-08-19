# listener.py
import socket
import threading
import logging
import datetime

# Configure logging for attack detections
logging.basicConfig(filename="honeypot.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Function to listen on arbitrary ports
def honeypot_listener(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # nosec B104 -- honeypot must listen on all interfaces to be reachable.
    server.bind(("0.0.0.0", port))  # nosec B104
    server.listen(5)
    logging.info(f"Listening on port {port}...")

    while True:
        client, addr = server.accept()
        # Capture attack details
        attack_details = f"Connection attempt from {addr[0]}:{addr[1]} on port {port}."
        logging.info(attack_details)
        print(f"Attack Detected: {attack_details}")

        client.send(b"Access Denied\n")
        client.close()

# Start Listener
def start_listeners():
    ports = [21, 22, 23, 80, 443, 3306, 3389]  # Common attack ports
    for port in ports:
        thread = threading.Thread(target=honeypot_listener, args=(port,))
        thread.start()

    # For verbose display
    print("Listeners started on common ports: 21, 22, 23, 80, 443, 3306, 3389")
