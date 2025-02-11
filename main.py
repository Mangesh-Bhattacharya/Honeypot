import threading
import logging
import listener
import app

# Configure logging
logging.basicConfig(filename="honeypot.log", level=logging.INFO, format="%(asctime)s - %(message)s")

if __name__ == "__main__":
    # Start the web honeypot
    flask_thread = threading.Thread(target=app.app.run, kwargs={"host": "0.0.0.0", "port": 8080, "debug": False, "use_reloader": False})
    flask_thread.start()

    # Start honeypot listeners
    listener.start_listeners()

    logging.info("Honeypot is active.")
