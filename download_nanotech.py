import yt_dlp

ydl_opts = {
    "format": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]",
    "outtmpl": "temp/movie_clips/infinity_war_nanotech.%(ext)s",
    "download_ranges": yt_dlp.utils.download_range_func(None, [(50, 115)]),
    "force_keyframes_at_cuts": True,
    "quiet": False
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(["https://www.youtube.com/watch?v=yo3R0CAqWZE"])
