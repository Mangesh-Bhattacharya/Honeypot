# main.py
import argparse
import os
import secrets
import sys
import threading
from pathlib import Path

from werkzeug.serving import make_server

import app
import dashboard
import events
import listener


def main(argv=None):
    p = argparse.ArgumentParser(description="Multi-service honeypot with a web dashboard")
    p.add_argument("--data-dir", default="data", help="where events.jsonl is written")
    p.add_argument("--real-ports", action="store_true", help="use standard ports (21/22/23/80/...); needs admin/root")
    p.add_argument("--dashboard-host", default="127.0.0.1", help="use 0.0.0.0 to view from a phone (a token is then required)")
    p.add_argument("--dashboard-port", type=int, default=8081)
    args = p.parse_args(argv)

    Path(args.data_dir).mkdir(parents=True, exist_ok=True)
    events.setup(Path(args.data_dir) / "events.jsonl")

    token = os.environ.get("HONEYPOT_DASH_TOKEN", "")
    if not token and args.dashboard_host not in ("127.0.0.1", "localhost"):
        token = secrets.token_urlsafe(16)
        print(f"Dashboard token: {token}", flush=True)

    listener.start_listeners(args.real_ports)
    try:
        # the decoy site must be reachable on all interfaces
        web = make_server("0.0.0.0", 80 if args.real_ports else 8080, app.app, threaded=True)  # nosec B104
        dash = make_server(args.dashboard_host, args.dashboard_port, dashboard.make_app(token), threaded=True)
    except OSError as exc:
        sys.exit(f"Cannot bind a web port: {exc}")
    threading.Thread(target=web.serve_forever, daemon=True).start()
    events.log_event("started", dashboard=f"http://{args.dashboard_host}:{args.dashboard_port}/")
    try:
        dash.serve_forever()
    except KeyboardInterrupt:
        events.log_event("stopped")


if __name__ == "__main__":
    main()
