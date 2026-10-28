# listener.py
import socketserver
import sys
import threading

from events import log_event

# name: (standard port, unprivileged port, banner). Unprivileged ports work without admin/root on every OS.
SERVICES = {
    "ftp": (21, 2121, b"220 (vsFTPd 3.0.5)\r\n"),
    "ssh": (22, 2222, b"SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.6\r\n"),
    "telnet": (23, 2323, b"login: "),
    "mysql": (3306, 33306, b""),
    "rdp": (3389, 33389, b""),
}


class _Server(socketserver.ThreadingTCPServer):
    daemon_threads = True
    # On Windows SO_REUSEADDR lets another process bind the same port, so only set it elsewhere.
    allow_reuse_address = sys.platform != "win32"


def _handler_for(service, banner):
    class Handler(socketserver.BaseRequestHandler):
        def handle(self):
            data = b""
            self.request.settimeout(5)
            try:
                if banner:
                    self.request.sendall(banner)
                data = self.request.recv(1024)
            except OSError:
                pass
            log_event("connection", service=service, port=self.server.server_address[1],
                      src_ip=self.client_address[0], src_port=self.client_address[1],
                      data=data.decode("latin-1"))
    return Handler


def serve(service, banner, host, port):
    server = _Server((host, port), _handler_for(service, banner))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def start_listeners(real_ports=False, host="0.0.0.0"):  # nosec B104
    servers = []
    for name, (standard, unprivileged, banner) in SERVICES.items():
        port = standard if real_ports else unprivileged
        try:
            servers.append(serve(name, banner, host, port))
        except OSError as exc:  # port taken or no privilege: skip it, keep the rest alive
            log_event("error", service=name, port=port, msg=str(exc))
    return servers
