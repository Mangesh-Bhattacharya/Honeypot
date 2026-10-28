# dashboard.py
import hmac

from flask import Flask, abort, jsonify, request

from events import RECENT

PAGE = """<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Honeypot</title><style>body{font:14px monospace;margin:8px}div{border-bottom:1px solid #8884;padding:4px;word-break:break-all}</style>
<h3>Honeypot events</h3><div id="e">loading...</div>
<script>
async function tick(){
  const r = await fetch('/api/events' + location.search);
  const box = document.getElementById('e'); box.textContent = '';
  for (const ev of (await r.json()).reverse()) {
    const d = document.createElement('div'); d.textContent = JSON.stringify(ev); box.appendChild(d);
  }
}
tick(); setInterval(tick, 5000);
</script>"""


def make_app(token=""):
    app = Flask(__name__)

    @app.before_request
    def auth():
        if request.path == "/healthz":
            return
        supplied = request.args.get("token") or request.headers.get("X-Token", "")
        if token and not hmac.compare_digest(supplied, token):
            abort(401)

    @app.get("/")
    def index():
        return PAGE

    @app.get("/api/events")
    def events():
        return jsonify(list(RECENT))

    @app.get("/healthz")
    def healthz():
        return "ok"

    return app
