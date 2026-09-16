# -*- coding: utf-8 -*-
"""
Keep-Alive Pinger for Render Free Tier
Render free tier sleeps after 15 minutes of inactivity.
This script pings the server every time it runs to keep it awake.
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import requests
import datetime
import os

SERVER_URL = "https://facebook-hx1b.onrender.com/"
LOG_FILE = os.path.join(os.path.dirname(__file__), "data", "keep_alive.log")

def ping_server():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        r = requests.get(SERVER_URL, timeout=30)
        status = f"[{now}] [OK] Server ALIVE - Status: {r.status_code} (Response: {r.elapsed.total_seconds():.2f}s)"
    except requests.exceptions.Timeout:
        status = f"[{now}] [TIMEOUT] Server TIMEOUT - waking up"
    except Exception as e:
        status = f"[{now}] [ERROR] Server ERROR - {e}"

    print(status)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(status + "\n")
    except Exception:
        pass

if __name__ == "__main__":
    ping_server()
