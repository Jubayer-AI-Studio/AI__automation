import yt_dlp

ydl_opts = {"quiet": True, "extract_flat": True, "noplaylist": True}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    res = ydl.extract_info("ytsearch5:tony stark jarvis hologram lab 4k", download=False)
    for entry in res.get("entries", [])[:4]:
        print(f"{entry['id']} | {entry.get('duration')}s | {entry.get('title')}")
