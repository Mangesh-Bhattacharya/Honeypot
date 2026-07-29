# Honeypot

A lightweight, multi-service honeypot for a homelab environment. It exposes fake services on common attack ports, logs every connection attempt, and serves a decoy web login page to lure and record credential-stuffing attempts.

> ⚠️ **For isolated lab/research use only.** Run this on a segmented VM or container with no access to real infrastructure — never on a production host or network.

## How It Works

- **`listener.py`** — TCP listeners on commonly targeted ports (21 FTP, 22 SSH, 23 Telnet, 80 HTTP, 443 HTTPS, 3306 MySQL, 3389 RDP). Any connection attempt is logged with source IP, port, and timestamp, then dropped with an `Access Denied` response.
- **`app.py`** — A Flask-based decoy web login page to capture credential-harvesting attempts against a fake HTTP service.
- **`main.py`** — Orchestrates the listeners and web decoy as background threads and writes structured logs to `honeypot.log` (gitignored — logs are runtime artifacts, not checked in).

## Setup

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
```

## Why This Matters

Honeypots are a core blue-team/deception-technology technique for early attack detection: instead of waiting for an alert on a real asset, you get a high-confidence signal the moment anyone touches a service that has no legitimate reason to be probed. This project demonstrates:

- Multi-port TCP service simulation
- Structured, timestamped attack logging
- Decoy web-service credential capture

## Roadmap

- [ ] Ship logs to a SIEM (OpenSearch/ELK) instead of a flat file
- [ ] Add banner-grabbing per service (SSH/FTP banners) for higher-fidelity deception
- [ ] Dockerize for one-command isolated deployment

## License

MIT
