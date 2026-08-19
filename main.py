# main.py
import threading
import logging
import app
import listener
from pynput.keyboard import Listener as KeyListener  # Rename to avoid conflict

# Configure logging
logging.basicConfig(filename="honeypot.log", level=logging.INFO,
                    format="%(asctime)s - %(message)s")

# Keylogger function to capture attacker keystrokes


def log_keystroke(key):
    try:
        key = key.char if hasattr(key, 'char') else str(key)
    except AttributeError:
        key = str(key)
    logging.info(f"Keystroke captured: {key}")

# Start keylogger


def start_keylogger():
    with KeyListener(on_press=log_keystroke) as key_listener:  # Use a different name here
        key_listener.join()


if __name__ == "__main__":
    logging.info("Starting Honeypot...")

    # Start the web honeypot (Flask server)
    # nosec B104 -- honeypot must listen on all interfaces to be reachable.
    flask_thread = threading.Thread(target=app.app.run, kwargs={
                                    "host": "0.0.0.0", "port": 2222, "debug": False, "use_reloader": False})  # nosec B104
    flask_thread.start()

    # Start honeypot listeners (for suspicious ports)
    listener_thread = threading.Thread(target=listener.start_listeners)
    listener_thread.start()

    # Start keylogger in a separate thread
    keylogger_thread = threading.Thread(target=start_keylogger)
    keylogger_thread.start()

    logging.info("Honeypot is fully operational.")
