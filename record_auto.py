import requests
import re
import json
import os
import subprocess

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
DURATION = os.getenv("DURATION", "1200")

HEADERS = {"User-Agent": "Mozilla/5.0"}
ID_FILE = "ids.json"

if not BOT_TOKEN or not CHAT_ID:
    raise SystemExit("BOT_TOKEN veya CHAT_ID eksik")

if os.path.exists(ID_FILE):
    with open(ID_FILE, "r") as f:
        ids = json.load(f)
else:
    ids = {"bigo": [], "tiktok": []}

def send_to_telegram(path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
    with open(path, "rb") as v:
        requests.post(url, data={"chat_id": CHAT_ID}, files={"video": v}, timeout=60)
    os.remove(path)

def record(m3u8, output):
    subprocess.call([
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", m3u8, "-t", DURATION, "-c", "copy", output
    ])

# BIGO
for uid in ids.get("bigo", []):
    try:
        html = requests.get(f"https://www.bigo.tv/{uid}", headers=HEADERS, timeout=10).text
        m = re.search(r'https://.*?\.m3u8', html)
        if not m:
            continue
        out = f"bigo_{uid}.mp4"
        record(m.group(), out)
        if os.path.exists(out):
            send_to_telegram(out)
    except:
        pass

# TIKTOK
for uid in ids.get("tiktok", []):
    try:
        html = requests.get(
            f"https://www.tiktok.com/@{uid}/live",
            headers=HEADERS,
            timeout=10
        ).text
        m = re.search(r'https://.*?\.m3u8', html)
        if not m:
            continue
        out = f"tiktok_{uid}.mp4"
        record(m.group(), out)
        if os.path.exists(out):
            send_to_telegram(out)
    except:
        pass
