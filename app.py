# app.py - Flask web service with Keylogger
import logging
from flask import Flask, request
import threading
from pynput.keyboard import Listener

# Configure logging
logging.basicConfig(filename="honeypot.log", level=logging.INFO,
                    format="%(asctime)s - %(message)s")

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def fake_web_service():
    ip = request.remote_addr
    logging.info(f"Web request from {ip}: {request.method} {request.path}")
    return "Honeypot Active!", 200  # Changed response to avoid 404 errors

# Keylogger function to capture attacker keystrokes


def log_keystroke(key):
    try:
        key = key.char if hasattr(key, 'char') else str(key)
    except AttributeError:
        key = str(key)
    logging.info(f"Keystroke captured: {key}")

# Start keylogger


def start_keylogger():
    with Listener(on_press=log_keystroke) as listener:
        listener.join()


if __name__ == "__main__":
    logging.info("Starting Honeypot...")

    # Start keylogger in a separate thread
    keylogger_thread = threading.Thread(target=start_keylogger, daemon=True)
    keylogger_thread.start()

    # Start the web service
    app.run(host="0.0.0.0", port=8080, debug=True, use_reloader=False)
