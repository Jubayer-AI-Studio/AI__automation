import yt_dlp

ydl_opts = {
    "format": "137+140/bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
    "outtmpl": "temp/movie_clips/iw_full_nanotech.%(ext)s",
    "quiet": False
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(["https://www.youtube.com/watch?v=yo3R0CAqWZE"])
