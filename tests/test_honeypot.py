import socket
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import app  # noqa: E402
import dashboard  # noqa: E402
import events  # noqa: E402
import listener  # noqa: E402


def test_listener_sends_banner_and_logs_payload():
    events.RECENT.clear()
    srv = listener.serve("ssh", b"SSH-2.0-Test\r\n", "127.0.0.1", 0)
    port = srv.server_address[1]
    with socket.create_connection(("127.0.0.1", port), timeout=5) as c:
        assert c.recv(64) == b"SSH-2.0-Test\r\n"
        c.sendall(b"root:hunter2")
    for _ in range(50):  # handler logs after the client closes
        if events.RECENT:
            break
        time.sleep(0.1)
    srv.shutdown()
    ev = events.RECENT[-1]
    assert (ev["kind"], ev["service"], ev["port"], ev["data"]) == ("connection", "ssh", port, "root:hunter2")


def test_busy_port_is_skipped_not_fatal():
    blocker = socket.socket()
    blocker.bind(("127.0.0.1", 0))
    blocker.listen()
    port = blocker.getsockname()[1]
    events.RECENT.clear()
    saved = dict(listener.SERVICES)
    listener.SERVICES.clear()
    listener.SERVICES["busy"] = (port, port, b"")
    try:
        assert listener.start_listeners(host="127.0.0.1") == []
    finally:
        listener.SERVICES.update(saved)
        listener.SERVICES.pop("busy")
        blocker.close()
    assert events.RECENT[-1]["kind"] == "error"


def test_web_decoy_captures_credentials():
    events.RECENT.clear()
    r = app.app.test_client().post("/admin", data={"username": "root", "password": "toor"})
    assert r.status_code == 401
    ev = events.RECENT[-1]
    assert (ev["kind"], ev["path"], ev["username"], ev["password"]) == ("web", "/admin", "root", "toor")


def test_dashboard_requires_token():
    c = dashboard.make_app("s3cret").test_client()
    assert c.get("/api/events").status_code == 401
    assert c.get("/api/events?token=wrong").status_code == 401
    assert c.get("/api/events?token=s3cret").status_code == 200
    assert c.get("/healthz").status_code == 200
