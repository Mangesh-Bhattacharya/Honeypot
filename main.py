# main.py
import threading
import logging
import app
import listener

# Configure logging
logging.basicConfig(filename="honeypot.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Start keylogger function
def start_keylogger():
    with listener(on_press=log_keystroke) as listener:
        listener.join()

if __name__ == "__main__":
    logging.info("Starting Honeypot...")

    # Start the web honeypot (Flask server)
    flask_thread = threading.Thread(target=app.app.run, kwargs={"host": "0.0.0.0", "port": 2222, "debug": False, "use_reloader": False})
    flask_thread.start()

    # Start honeypot listeners (for suspicious ports)
    listener_thread = threading.Thread(target=listener.start_listeners)
    listener_thread.start()

    # Start keylogger in a separate thread
    keylogger_thread = threading.Thread(target=start_keylogger)
    keylogger_thread.start()

    logging.info("Honeypot is fully operational.")
