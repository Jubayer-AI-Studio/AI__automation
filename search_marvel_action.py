import yt_dlp
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ydl_opts = {"quiet": True, "extract_flat": True, "noplaylist": True}
queries = [
    "ytsearch5:iron man infinity war suit up 4k 60fps scene",
    "ytsearch5:iron man vs cull obsidian 4k scene",
    "ytsearch5:iron man vs thanos fight scene 4k",
    "ytsearch5:tony stark creating mark 85 holographic lab 4k"
]

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    for q in queries:
        print(f"=== {q} ===")
        res = ydl.extract_info(q, download=False)
        for entry in res.get("entries", [])[:3]:
            print(f"{entry['id']} | {entry.get('duration')}s | {entry.get('title')}")
