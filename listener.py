import socket
import threading
import logging
from flask import Flask, request

# Configure logging
logging.basicConfig(filename="honeypot.log", level=logging.INFO,
                    format="%(asctime)s - %(message)s")

# Flask app to mimic a web service
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def fake_web_service():
    ip = request.remote_addr
    logging.info(f"Web request from {ip}: {request.method} {request.path}")
    return "404 Not Found", 404

# Function to start the Flask server


def run_flask():
    app.run(host="0.0.0.0", port=8080, debug=False, use_reloader=False)

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


if __name__ == "__main__":
    # Start the web honeypot
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Ports to listen on
    ports = [21, 22, 23, 80, 443, 3306, 3389]  # Common attack ports

    for port in ports:
        thread = threading.Thread(target=honeypot_listener, args=(port,))
        thread.start()

    logging.info("Honeypot is active.")
