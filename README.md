# Honeypot

A lightweight, multi-service honeypot. It exposes fake SSH/FTP/Telnet/MySQL/RDP services plus a decoy admin login page, records every connection and every credential attempt as structured JSON, and shows them live on a mobile-friendly web dashboard.

> ⚠️ **For isolated lab/research use only.** Run it on a segmented VM or container with no access to real infrastructure — never on a production host or network. Captured credentials are attacker-supplied; treat `events.jsonl` as sensitive.

## Run it

| Platform | How |
|---|---|
| Windows / macOS / Linux binary | Download from [Releases](../../releases), run `honeypot-<OS>` |
| Docker (Linux, macOS, Windows, Raspberry Pi — amd64 + arm64) | `HONEYPOT_DASH_TOKEN=pick-a-secret docker compose up -d` |
| From source | `pip install -r requirements.txt && python main.py` |

By default it uses unprivileged ports (SSH 2222, FTP 2121, Telnet 2323, MySQL 33306, RDP 33389, web decoy 8080) so no admin rights are needed. `--real-ports` binds the standard ports (needs admin/root). A port that is busy or not permitted is logged and skipped; the rest keep running.

## Dashboard (Android, iOS, any browser)

`http://127.0.0.1:8081/` shows the latest 500 events, refreshing every 5 s. It listens on localhost only. To open it from a phone, start with `--dashboard-host 0.0.0.0`; a token is then required (`HONEYPOT_DASH_TOKEN`, or one is generated and printed) — open `http://<host>:8081/?token=<token>`. Use a VPN or HTTPS reverse proxy; the token travels in the URL.

Events are written to `data/events.jsonl` (rotated at 5 MB × 3), one JSON object per line, ready for Filebeat/OpenSearch.

## Test

```bash
pip install -r requirements.txt pytest
python -m pytest
```

CI runs the tests on Ubuntu, Windows and macOS (Python 3.10 and 3.12), plus Bandit, CodeQL and a Docker smoke test.

## Roadmap

- [ ] Ship events to a SIEM (OpenSearch/ELK) natively
- [ ] Per-IP rate limiting / connection caps
- [ ] Native mobile push alerts

## License

MIT
