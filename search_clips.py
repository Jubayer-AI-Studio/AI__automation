import yt_dlp
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ydl_opts = {
    "quiet": True,
    "extract_flat": True,
    "noplaylist": True
}

queries = [
    "ytsearch6:iron man 4k edit shorts",
    "ytsearch6:iron man suit up 4k shorts",
    "ytsearch6:iron man nanotech 4k shorts",
    "ytsearch6:tony stark 4k shorts bad ass"
]

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    for q in queries:
        print(f"=== {q} ===")
        res = ydl.extract_info(q, download=False)
        for entry in res.get("entries", [])[:4]:
            print(f"{entry['id']} | {entry.get('duration')}s | {entry.get('title')}")
