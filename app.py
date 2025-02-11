# app.py - Flask web service
import logging
from flask import Flask, request

# Configure logging
logging.basicConfig(filename="honeypot.log", level=logging.INFO, format="%(asctime)s - %(message)s")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def fake_web_service():
    ip = request.remote_addr
    logging.info(f"Web request from {ip}: {request.method} {request.path}")
    return "404 Not Found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False, use_reloader=False)
