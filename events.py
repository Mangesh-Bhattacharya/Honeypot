# events.py
import json
import logging
import logging.handlers
import time
from collections import deque

_log = logging.getLogger("honeypot.events")
_log.setLevel(logging.INFO)
_log.propagate = False

# Newest events for the dashboard; the JSONL file is the durable record.
RECENT = deque(maxlen=500)


def setup(path):
    handler = logging.handlers.RotatingFileHandler(path, maxBytes=5_000_000, backupCount=3, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(message)s"))
    _log.handlers[:] = [handler]


def log_event(kind, **fields):
    event = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "kind": kind, **fields}
    RECENT.append(event)
    _log.info(json.dumps(event))
    print(f"[{event['ts']}] {kind} {fields}", flush=True)
