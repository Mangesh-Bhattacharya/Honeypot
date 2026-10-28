# app.py
from flask import Flask, request

from events import log_event

app = Flask(__name__)

FORM = """<!doctype html><title>Admin Login</title>
<h2>Administration Console</h2>{msg}
<form method="post"><input name="username" placeholder="Username"><br>
<input name="password" type="password" placeholder="Password"><br><button>Sign in</button></form>"""

METHODS = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]


@app.route("/", defaults={"path": ""}, methods=METHODS)
@app.route("/<path:path>", methods=METHODS)
def decoy(path):
    creds = {}
    if request.method == "POST":
        creds = {"username": request.form.get("username", "")[:200],
                 "password": request.form.get("password", "")[:200]}
    log_event("web", src_ip=request.remote_addr, method=request.method, path=request.path[:200],
              user_agent=request.headers.get("User-Agent", "")[:200], **creds)
    if creds:
        return FORM.format(msg="<p>Invalid credentials.</p>"), 401
    return FORM.format(msg=""), 200
