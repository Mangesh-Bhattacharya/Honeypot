# app.py
import logging
import threading
import sys
import tkinter as tk
import requests
import signal
from flask import Flask, request
from pynput.keyboard import Listener
from tkinter import scrolledtext

# Configure logging
logging.basicConfig(filename="honeypot.log", level=logging.INFO, format="%(asctime)s - %(message)s")

app = Flask(__name__)

# GUI Class to display logs and verbose info
class HoneypotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Honeypot Scanner")
        self.root.geometry("600x700")
        self.root.configure(bg="#1e1e2e")

        # Real-time logs display
        self.log_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=70, height=20, bg="#2e2e3e", fg="white")
        self.log_display.pack(padx=10, pady=10)

        # Update logs every 5 seconds
        self.update_logs()

    def update_logs(self):
        try:
            with open("honeypot.log", "r") as log_file:
                logs = log_file.read()
                self.log_display.delete(1.0, tk.END)
                self.log_display.insert(tk.END, logs)
        except FileNotFoundError:
            self.log_display.insert(tk.END, "No logs found.")
        self.root.after(5000, self.update_logs)


@app.route("/", methods=["GET", "POST"])
def fake_web_service():
    ip = request.remote_addr
    logging.info(f"Web request from {ip}: {request.method} {request.path}")

    # Detect if the IP belongs to a VPN or proxy
    if is_vpn_or_proxy(ip):
        logging.warning(f"VPN/Proxy Detected: {ip}")
    return "Honeypot Active!", 200

# Detect if an IP belongs to a VPN or proxy (placeholder example)
def is_vpn_or_proxy(ip):
    try:
        # For real VPN detection, integrate a service like IPinfo or ip-api
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        return data.get("org", "").startswith("AS")
    except requests.RequestException:
        return False

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

# Signal handler for clean exit
def signal_handler(sig, frame):
    logging.info("Shutting down Honeypot...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    logging.info("Starting Honeypot...")

    # Start keylogger in a separate thread
    keylogger_thread = threading.Thread(target=start_keylogger, daemon=True)
    keylogger_thread.start()

    # Start the web service in a separate thread
    flask_thread = threading.Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 2222, "debug": True, "use_reloader": False}, daemon=True)
    flask_thread.start()

    # Start GUI
    root = tk.Tk()
    gui = HoneypotGUI(root)
    root.mainloop()
